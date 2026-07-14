"""
Parse an API-Reference markdown file (04-API参考/**/*.md) that embeds a full
OpenAPI 3.0 spec in a ```json fenced block, and split it into RAG chunks.

Unlike the help-center chunker (hand-written by LLM agents reading prose),
this walks the actual OpenAPI JSON structure programmatically — hand-picking
chunks out of a dense generated schema is error-prone (easy to mis-transcribe
a field name, type, or required flag), so correctness here comes from parsing
the JSON directly rather than reading it and re-typing.

Produces three kinds of output for one endpoint file:
  1. One "endpoint overview" chunk — method, path, one-line purpose, any
     prose hints/warnings found before the JSON block.
  2. One chunk per request parameter GROUP (headers as one chunk, top-level
     request-body fields as one chunk — request bodies are usually small
     enough to keep as a single logical unit; see note below if this stops
     being true for some endpoint).
  3. One chunk per reusable response schema *component* (Routing, PriceItem,
     etc.), listing each field's name/type/required/description. Components
     are shared across endpoints, so grouping by component (not by endpoint)
     avoids duplicating the same field docs across every endpoint that
     references them — this script tags which endpoint(s) reference which
     components instead of inlining the fields per endpoint.
  4. If any enum-valued field's description is actually a disguised lookup
     table (a long string of "- CODE: meaning" lines, e.g. the `status`
     response code enum), extract it into a separate structured JSON file
     instead of a prose chunk — same rationale as the 退票时限表.

Usage:
    python chunk_api_reference.py "<path to markdown file>" --endpoint-id search
"""

import argparse
import html
import json
import re
from pathlib import Path


def extract_openapi_block(md_text: str) -> dict:
    m = re.search(r"```json\s*\n(.*?)\n```", md_text, re.DOTALL)
    if not m:
        raise ValueError("No ```json block found in file")
    return json.loads(m.group(1))


def extract_prose_before_json(md_text: str) -> str:
    idx = md_text.find("```json")
    prose = md_text[:idx] if idx >= 0 else md_text
    # strip gitbook hint/button boilerplate blocks
    prose = re.sub(r"\{% hint.*?%\}.*?\{% endhint %\}", "", prose, flags=re.DOTALL)
    # Other GitBook component tags wrap real content (unlike {% hint %},
    # whose content is a throwaway "ask Eva" callout) -- strip just the tags.
    prose = re.sub(r"\{%[^}]*%\}", "", prose)
    prose = re.sub(r"<a href.*?</a>", "", prose)
    prose = re.sub(r"\n{3,}", "\n\n", prose).strip()
    return prose


def looks_like_lookup_table(description: str) -> list[tuple[str, str]] | None:
    """Detect '- CODE: meaning' style enumerations disguised as a description string."""
    lines = [l.strip() for l in description.split("\n") if l.strip().startswith("-")]
    if len(lines) < 5:  # too short to bother extracting separately
        return None
    entries = []
    for line in lines:
        m = re.match(r"-\s*`?([^`:]+)`?\s*:\s*(.+)", line)
        if m:
            entries.append((m.group(1).strip(), m.group(2).strip()))
    return entries if len(entries) >= 5 else None


def resolve_ref(ref: str) -> str:
    return ref.split("/")[-1]


def clean_markdown_text(text: str) -> str:
    """Strip inline markdown formatting markers from otherwise-real prose,
    keeping the underlying text -- see chunk_disambiguation.py's function of
    the same name for the full rationale. The OpenAPI spec's own field
    `description` strings are hand-written prose and carry the same markdown
    noise (confirmed: 座位.md's endpoint description embeds "**Dependency:**"
    / "> Steps:" / backtick-quoted code verbatim). Applied inside
    describe_field() so it covers request/response/component fields
    uniformly via flatten_fields(), plus separately to the endpoint overview
    prose/description and param descriptions below."""
    text = html.unescape(text)  # decode &#x624D; etc -- confirmed leaking into 资讯 chunks otherwise
    text = re.sub(r"\{%[^}]*%\}", "", text)  # stray GitBook component tags ({% stepper %} etc.) that reached here unstripped
    text = re.sub(r"(?m)^```\w*\s*$", "", text)  # fenced-code-block delimiters -- keep the code content, drop the ``` markers
    text = re.sub(r"(?m)^[ \t]*(?:\*[ \t]*){3,}$", "", text)  # *** horizontal rule
    text = re.sub(r"(?m)^[ \t]*(?:-[ \t]*){3,}$", "", text)   # --- horizontal rule
    text = re.sub(r"(?m)^[ \t]*(?:_[ \t]*){3,}$", "", text)   # ___ horizontal rule
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)    # [text](url) and ![alt](url), incl. bare ![]() -> ""
    text = re.sub(r"<(https?://[^>\s]+)>", r"\1", text)
    text = re.sub(r"\*\*((?:[^*\n]|\\\*)+)\*\*", r"\1", text)
    text = re.sub(r"__([^_\n]+)__", r"\1", text)
    text = re.sub(r"(?<!\w)\*((?:[^*\n]|\\\*)+)\*(?!\w)", r"\1", text)
    text = re.sub(r"(?<!\w)_([^_\n]+)_(?!\w)", r"\1", text)
    text = re.sub(r"`([^`\n]+)`", r"\1", text)
    text = re.sub(r"(?m)^(?:>\s?)?#{1,6}\s+", "", text)  # handles "### h" and blockquoted "> ### h"
    text = re.sub(r"(?m)^>\s?", "", text)
    text = re.sub(r"\\\n", "\n", text)
    text = re.sub(r"\\([*_`\[\]()#>\\])", r"\1", text)
    return text


def describe_field(name: str, schema: dict, required: bool, components: dict) -> dict:
    field = {"name": name, "required": required}
    if "$ref" in schema:
        field["type"] = f"ref:{resolve_ref(schema['$ref'])}"
    elif schema.get("type") == "array":
        items = schema.get("items", {})
        if "$ref" in items:
            field["type"] = f"array<ref:{resolve_ref(items['$ref'])}>"
        else:
            field["type"] = f"array<{items.get('type', 'unknown')}>"
    else:
        field["type"] = schema.get("type", "unknown")
    if "enum" in schema:
        field["enum"] = schema["enum"]
    if schema.get("description"):
        field["description"] = clean_markdown_text(schema["description"])
    if schema.get("deprecated"):
        field["deprecated"] = True
    if schema.get("nullable"):
        field["nullable"] = True
    return field


def flatten_fields(name: str, schema: dict, required: bool, components: dict,
                    prefix: str = "", depth: int = 0, max_depth: int = 6) -> list[dict]:
    """describe_field() only documents ONE field's own description — for a
    field that's an inline object/array-of-objects (no $ref, so nothing else
    documents its shape), that silently drops every sub-field underneath it.
    Confirmed for real on 座位.md's `cabins` response field: deck/cabinClass/
    cabinLayout/columns/rows/exitRowPositions and the seat-status/seat-
    characteristics enum meanings were all inline and had no chunk anywhere.

    Recurses into inline object properties and inline array-of-object items,
    building a dotted/bracketed path (`cabins[].cabin.cabinLayout.rows`) so
    each nested field is still traceable to where it lives. Stops recursing
    at a `$ref`: that schema's fields are already covered by its own
    component chunk (see chunk_endpoint's "component" chunks below) —
    recursing there too would just duplicate them and blow up chunk size for
    types shared across many endpoints. `max_depth` is a defensive guard
    against pathological/self-referential schemas, not expected to bite on
    this corpus.
    """
    path = f"{prefix}{name}"
    field = describe_field(name, schema, required, components)
    field["name"] = path
    out = [field]
    if depth >= max_depth or "$ref" in schema:
        return out
    if schema.get("type") == "object" and schema.get("properties"):
        sub_required = set(schema.get("required", []))
        for sub_name, sub_schema in schema["properties"].items():
            out.extend(flatten_fields(sub_name, sub_schema, sub_name in sub_required, components,
                                       prefix=f"{path}.", depth=depth + 1, max_depth=max_depth))
    elif schema.get("type") == "array":
        items = schema.get("items", {})
        if "$ref" not in items and items.get("type") == "object" and items.get("properties"):
            sub_required = set(items.get("required", []))
            for sub_name, sub_schema in items["properties"].items():
                out.extend(flatten_fields(sub_name, sub_schema, sub_name in sub_required, components,
                                           prefix=f"{path}[].", depth=depth + 1, max_depth=max_depth))
    return out


def format_fields(fields: list[dict]) -> list[str]:
    lines = []
    for f in fields:
        bits = [f"- {f['name']} ({f['type']}{'，必填' if f['required'] else '，可选'})"]
        if f.get("deprecated"):
            bits.append(" [deprecated]")
        bits.append(f": {f.get('description', '')}")
        if f.get("enum"):
            bits.append(f"（枚举值：{f['enum']}）")
        lines.append("".join(bits))
    return lines


def group_by_top_level(fields: list[dict]) -> list[list[dict]]:
    """flatten_fields() returns one flat list mixing a top-level field with
    all of its recursively-flattened descendants (paths like 'cabins',
    'cabins[].cabin', 'cabins[].cabin.rows', ...) in order. Regroup them by
    which top-level field they belong to, so format_fields_for_text() can
    decide per-field whether its subtree is small enough to show inline."""
    groups: list[list[dict]] = []
    for f in fields:
        top = f["name"].split(".")[0].split("[]")[0]
        if not groups or groups[-1][0]["name"].split(".")[0].split("[]")[0] != top:
            groups.append([])
        groups[-1].append(f)
    return groups


def format_fields_for_text(fields: list[dict], collapse_threshold: int = 6) -> list[str]:
    """Same content as format_fields(), except a top-level field whose own
    flattened subtree is deeper than `collapse_threshold` entries collapses
    to ONE line (its own description + a pointer), instead of dumping the
    whole subtree into the embedded text.

    Why: BGE (max_seq_length=512 tokens) silently truncates anything past
    that when computing the embedding. A handful of fields in this corpus
    (e.g. 座位.md's `cabins`) recurse into 30+ nested fields once
    flatten_fields() stopped silently dropping them -- inlining all of that
    into `text` produced single chunks over 16,000 characters, most of which
    the embedding model never actually sees, so it stopped meaningfully
    influencing *whether* the chunk gets retrieved at all.

    The full uncollapsed subtree is never dropped: the caller stores the
    complete `fields` list (unfiltered) alongside `text` in both
    children.jsonl and Chroma metadata (see ingest_api_docs.py) -- it's
    simply not embedded, so it can't be truncated out of the match
    computation while remaining fully retrievable on every hit. Same
    pattern as 帮助中心's parent/child split: short text for matching,
    full detail attached for whatever reads the hit afterward.
    """
    lines = []
    for group in group_by_top_level(fields):
        if len(group) > collapse_threshold:
            head = group[0]
            req = "必填" if head["required"] else "可选"
            desc = f": {head.get('description', '')}" if head.get("description") else ""
            lines.append(
                f"- {head['name']} ({head['type']}，{req}){desc}"
                f"（还有 {len(group) - 1} 个嵌套子字段，完整字段名/类型/含义见该 chunk 的 fields 元数据，不在此列出）"
            )
        else:
            lines.extend(format_fields(group))
    return lines


def chunk_endpoint(spec: dict, prose: str, endpoint_id: str, level2_category: str, source_path: str):
    paths = spec.get("paths", {})
    if not paths:
        raise ValueError("No paths in spec")
    path, methods = next(iter(paths.items()))
    method, op = next(iter(methods.items()))
    components = spec.get("components", {}).get("schemas", {})

    chunks = []
    lookup_tables = []

    # 1. Endpoint overview chunk
    summary = op.get("summary", "")
    description = clean_markdown_text(op.get("description", ""))
    chunks.append({
        "chunk_id": f"{endpoint_id}-overview",
        "endpoint_id": endpoint_id,
        "doc_type": "端点概览",
        "endpoint": path,
        "http_method": method.upper(),
        "level1_category": "API参考",
        "level2_category": level2_category,
        "source_path": source_path,
        "text": (clean_markdown_text(prose) + "\n\n" + description).strip() or summary,
    })

    # 2. Request parameters (headers) — usually short & uniform, keep as one chunk
    params = op.get("parameters", [])
    if params:
        param_lines = [f"{p['name']} ({p.get('in','header')}, required={p.get('required', False)}): {clean_markdown_text(p.get('description',''))}" for p in params]
        chunks.append({
            "chunk_id": f"{endpoint_id}-request-headers",
            "endpoint_id": endpoint_id,
            "doc_type": "请求参数",
            "endpoint": path,
            "level1_category": "API参考",
            "level2_category": level2_category,
            "source_path": source_path,
            "text": "请求头参数：\n" + "\n".join(param_lines),
        })

    # 3. Request body top-level fields
    req_schema = (
        op.get("requestBody", {})
        .get("content", {})
        .get("application/json", {})
        .get("schema", {})
    )
    if req_schema.get("properties"):
        required_set = set(req_schema.get("required", []))
        fields = []
        for name, sub in req_schema["properties"].items():
            fields.extend(flatten_fields(name, sub, name in required_set, components))
        chunks.append({
            "chunk_id": f"{endpoint_id}-request-body",
            "endpoint_id": endpoint_id,
            "doc_type": "请求参数",
            "endpoint": path,
            "level1_category": "API参考",
            "level2_category": level2_category,
            "source_path": source_path,
            "fields": fields,
            "text": "请求体字段：\n" + "\n".join(format_fields_for_text(fields)),
        })

    # 4. Response top-level status/shape (non-component fields), and detect lookup tables
    resp_schema = (
        op.get("responses", {})
        .get("200", {})
        .get("content", {})
        .get("application/json", {})
        .get("schema", {})
    )
    if resp_schema.get("properties"):
        for name, sub in resp_schema["properties"].items():
            resolved = sub
            # OpenAPI spec says sibling keys next to $ref should be ignored, but this
            # generator puts the *real* human-readable description (sometimes a whole
            # disguised lookup table, e.g. `status`) on the property alongside $ref
            # anyway. So: always check description for a lookup table first, and only
            # skip emitting a plain prose chunk (not the lookup-table check) when the
            # field is a bare $ref with nothing beyond what its component chunk covers.
            desc = resolved.get("description", "")
            table = looks_like_lookup_table(desc)
            if table:
                lookup_tables.append({
                    "field": name,
                    "endpoint": path,
                    "source_path": source_path,
                    "ref": resolve_ref(sub["$ref"]) if "$ref" in sub else None,
                    "entries": [{"code": c, "meaning": m} for c, m in table],
                })
                continue
            if "$ref" in sub:
                continue  # handled as its own component chunk below, no separate description to keep
            else:
                # flatten_fields recurses into inline nested objects/arrays so a
                # field like `cabins` (array of an inline, non-$ref object with
                # its own deeply nested sub-fields) doesn't lose everything
                # below its own one-line description -- see flatten_fields'
                # docstring for the 座位.md case this was missing.
                fields = flatten_fields(name, sub, False, components)
                chunks.append({
                    "chunk_id": f"{endpoint_id}-response-{name}",
                    "endpoint_id": endpoint_id,
                    "doc_type": "响应字段",
                    "endpoint": path,
                    "level1_category": "API参考",
                    "level2_category": level2_category,
                    "source_path": source_path,
                    "fields": fields,
                    "text": f"响应字段 {name}：\n" + "\n".join(format_fields_for_text(fields)),
                })

    # 5. One chunk per reusable component schema
    for comp_name, comp_schema in components.items():
        if comp_schema.get("type") != "object" or not comp_schema.get("properties"):
            continue  # skip bare enums, handled inline where referenced
        required_set = set(comp_schema.get("required", []))
        fields = []
        for name, sub in comp_schema["properties"].items():
            fields.extend(flatten_fields(name, sub, name in required_set, components))
        chunks.append({
            "chunk_id": f"{endpoint_id}-component-{comp_name}",
            "endpoint_id": endpoint_id,
            "doc_type": "响应组件",
            "endpoint": path,
            "component": comp_name,
            "level1_category": "API参考",
            "level2_category": level2_category,
            "source_path": source_path,
            "fields": fields,
            "text": f"响应组件 {comp_name} 字段列表：\n" + "\n".join(format_fields_for_text(fields)),
        })

    return chunks, lookup_tables


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("md_file")
    parser.add_argument("--endpoint-id", required=True)
    parser.add_argument("--level2-category", default="预订API")
    args = parser.parse_args()

    md_path = Path(args.md_file)
    md_text = md_path.read_text(encoding="utf-8")
    spec = extract_openapi_block(md_text)
    prose = extract_prose_before_json(md_text)

    # Same normalization as chunk_disambiguation.py/chunk_faq_api.py — this
    # script used str(md_path) verbatim (whatever the CLI arg looked like,
    # backslashes and all on Windows, still including the "API文档/" corpus
    # root since it was never relativized), which get_full_article can't
    # resolve: it joins source_path onto API_DOCS_ROOT, which already ends
    # in .../doc/API文档, so a source_path that still starts with "API文档/"
    # doubles that segment. Confirmed broken for real via a production trace
    # (order.do's get_full_article call 404'd twice, once per slash style).
    source_path = str(md_path).split("API文档", 1)[1].lstrip("\\/").replace("\\", "/")

    chunks, lookup_tables = chunk_endpoint(spec, prose, args.endpoint_id, args.level2_category, source_path)

    print(f"=== {len(chunks)} chunks ===")
    for c in chunks:
        preview = c["text"][:100].replace("\n", " ")
        print(f"[{c['doc_type']}] {c['chunk_id']}: {preview}...")

    print(f"\n=== {len(lookup_tables)} lookup table(s) extracted ===")
    for t in lookup_tables:
        print(f"field={t['field']}, {len(t['entries'])} entries, first 3: {t['entries'][:3]}")

    out_dir = md_path.parent / "_rag-chunks"
    out_dir.mkdir(exist_ok=True)

    # Merge into existing children.jsonl rather than overwrite: multiple endpoint
    # files (e.g. all 12 booking-apis) share one output folder. Overwriting here
    # previously destroyed every earlier endpoint's chunks except the last one run.
    out_file = out_dir / "children.jsonl"
    existing = []
    if out_file.exists():
        existing = [json.loads(l) for l in out_file.read_text(encoding="utf-8").splitlines() if l.strip()]
        # Exact match on endpoint_id, NOT a chunk_id prefix string check — endpoint
        # ids like "get-offer" are literal prefixes of others like "get-offer-price",
        # so a startswith("get-offer-") filter would also delete get-offer-price's
        # chunks. This bit it for real once already; don't regress it.
        existing = [c for c in existing if c.get("endpoint_id") != args.endpoint_id]
    with open(out_file, "w", encoding="utf-8") as f:
        for c in existing + chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    # Lookup-table filenames must include endpoint_id too — multiple endpoints
    # commonly share a field name like `status`, which would otherwise collide.
    for t in lookup_tables:
        with open(out_dir / f"lookup-table-{args.endpoint_id}-{t['field']}.json", "w", encoding="utf-8") as f:
            json.dump(t, f, ensure_ascii=False, indent=2)
    print(f"\nWritten to {out_dir}")


if __name__ == "__main__":
    main()
