"""
Parse a GitBook '{% tab title="模式" %} ... {% endtab %}' field-schema block
embedded inside an otherwise-prose (A类) markdown doc, and split it into one
RAG chunk per field.

Why this exists: this markdown convention (one field per **bold header**,
followed by `* **类型:**` / `* **必填:**` / `* **描述:**` / `* **有效值:**`
/ `* **默认值:**` / `* **示例:**` bullets) is the hand-written analog of the
OpenAPI JSON that chunk_api_reference.py parses for 04-API参考 endpoints --
same information shape (name/type/required/description/enum/example), just
authored as markdown instead of generated JSON. Docs under 03-产品指南
(e.g. webhook-overview/*.md) were previously chunked as plain A类 prose,
which collapsed this entire field list into ONE chunk per doc (confirmed on
4 files: 航变通知.md, 航司状态更新通知.md, 出票完成通知.md, 作废通知.md) --
the same failure mode chunk_api_reference.py's docstring describes for
hand-transcribed OpenAPI: burying one field's meaning (e.g. schedule-change
notification's `status`: 0=未确认/1=已确认) inside a dozen unrelated
fields' descriptions dilutes that field's embedding into irrelevance for a
query about it specifically -- confirmed via direct embedding distance
measurement 2026-07-16 (natural queries about "确认/未确认状态" landed at
cosine distance ~0.47-0.70 against the merged chunk vs ~0.34 achievable
against a field-focused chunk).

This does NOT replace A类 chunking for the rest of the document (概述,
注意事项, 您应该做什么, 示例负载, etc.) -- those stay hand/subagent-chunked
as before. This script only takes over the "模式" tab block specifically,
same division of labor as chunk_api_reference.py handling just the ```json
block while prose around it is chunked separately.

Usage:
    python chunk_field_pattern_block.py "<path to markdown file>" --id-prefix whschedulenotify --level2-category Webhook通知
"""
import argparse
import json
import re
from pathlib import Path


def extract_mode_tab_block(md_text: str) -> str:
    m = re.search(r'\{%\s*tab title="模式"\s*%\}(.*?)\{%\s*endtab\s*%\}', md_text, re.DOTALL)
    if not m:
        raise ValueError('No {% tab title="模式" %} ... {% endtab %} block found in file')
    return m.group(1)


def parse_fields(block: str) -> list[dict]:
    """Split the tab block into per-field sections at each **bold header**
    line, then pull out type/required/description/enum/default/example from
    the bullet list underneath it."""
    # A field header is a **name** on its own line (not nested under a bullet).
    parts = re.split(r"(?m)^\*\*([^\n*]+)\*\*\s*$", block)
    # re.split with a capturing group interleaves: [preamble, name1, body1, name2, body2, ...]
    fields = []
    for i in range(1, len(parts), 2):
        name = parts[i].strip().replace("\\[", "[").replace("\\]", "]")  # GitBook escapes [] in field names like previousSegs\[]
        body = parts[i + 1].replace("\\[", "[").replace("\\]", "]")
        field = {"name": name}

        m = re.search(r"\*\s*\*\*类型:\*\*\s*(.+)", body)
        if m:
            field["type"] = m.group(1).strip()

        m = re.search(r"\*\s*\*\*必填:\*\*\s*(.+)", body)
        if m:
            field["required"] = m.group(1).strip().startswith("是")

        # 描述 can be a single line, or a line followed by an indented
        # "有效值：\n  * 0: xxx\n  * 1: xxx" enum block (航变通知.md's `status`).
        m = re.search(r"\*\s*\*\*描述:\*\*\s*(.+?)(?=\n\*\s*\*\*(?:默认值|示例|有效值):|\n\*\*[^\n*]+\*\*\s*$|\Z)", body, re.DOTALL)
        if m:
            desc_block = m.group(1).strip()
            enum_m = re.search(r"有效值[：:]\s*\n((?:\s*\*\s*.+\n?)+)", desc_block)
            if enum_m:
                desc_line = desc_block[:enum_m.start()].strip().rstrip("。").strip()
                entries = re.findall(r"\*\s*(.+)", enum_m.group(1))
                field["description"] = desc_line
                field["enum"] = [e.strip() for e in entries]
            else:
                field["description"] = " ".join(l.strip() for l in desc_block.splitlines() if l.strip())

        # 有效值 as its OWN top-level bullet, separate from 描述 (航司状态更新通知.md's
        # `airlineStatus`/`type` fields use this layout instead of nesting it under 描述).
        if "enum" not in field:
            m = re.search(r"\*\s*\*\*有效值:\*\*\s*\n((?:\s*\*\s*.+\n?)+)", body)
            if m:
                entries = re.findall(r"\*\s*(.+)", m.group(1))
                field["enum"] = [e.strip() for e in entries]

        m = re.search(r"\*\s*\*\*示例:\*\*\s*`?([^\n`]+)`?", body)
        if m:
            field["example"] = m.group(1).strip()

        fields.append(field)
    return fields


def field_to_text(field: dict, doc_topic: str = "") -> str:
    """Natural-sentence phrasing, not a colon-separated attribute list --
    AND prefixed with the document's own topic, not just the bare field.

    Confirmed via direct embedding distance test 2026-07-16: a telegram-style
    dump ("字段 status：类型整数，必填，描述：事件状态，有效值：0: 未确认；
    1: 已确认，示例：0") scored WORSE (cosine dist ~0.50-0.54) against the
    natural production question "航变通知未确认和已确认有什么区别" than even
    the OLD merged-blob chunk did (~0.47) -- splitting per field alone isn't
    enough if the field's own text still reads like a spec sheet instead of
    an answer. Rephrasing as a bare sentence with no topic ("status 字段类型
    为整数...表示事件状态。取值含义：0 表示未确认；1 表示已确认。") helped
    only against a topic-word-stripped query ("未确认 已确认 区别", dist
    ~0.45) -- real customer questions AND the agent's own actual rewrites
    almost always keep a topic word ("航变通知未确认已确认...", "航变通知
    未确认 已确认 确认状态") since stripping it takes deliberate, unreliable
    prompt-following the agent doesn't consistently do (confirmed via two
    separate live traces where the "strip the topic word" guidance in
    AGENTS.md was written down but not actually applied). Against those
    topic-inclusive phrasings, the bare-field chunk scored ~0.48-0.51 --
    outside top-10 in the live corpus both times.

    Prefixing the field sentence with its OWN document's topic ("航变通知
    （order.schedulechange webhook）的 status 字段...") flips this: same
    topic-inclusive queries dropped to ~0.28-0.33 (a ~0.18-0.20 improvement,
    would rank top of the corpus), at the cost of only ~0.03 on the
    topic-stripped query (0.45 -> 0.48, still fine). This is a better trade
    than relying on the agent to strip the topic word at query time -- fix
    it once at ingest time instead of hoping every future query rewrite
    happens to omit the topic. C类's OpenAPI-derived chunks don't need this
    because API integration questions already tend to name the field/
    endpoint verbatim; a support question asking what a status code "means"
    usually names the topic (the notification type), not the field."""
    req = "必填" if field.get("required") else "可选"
    type_ = field.get("type", "未知")
    desc = field.get("description", "").rstrip("。").rstrip(".")
    prefix = f"{doc_topic}的 " if doc_topic else ""
    sentence = f"{prefix}{field['name']} 字段类型为{type_}，{req}"
    if desc:
        sentence += f"，表示{desc}"
    sentence += "。"
    if field.get("enum"):
        pairs = []
        for e in field["enum"]:
            m = re.match(r"[`]?([^`\s:：=]+)[`]?\s*[:：=]\s*(.+)", e)
            if m:
                pairs.append(f"{m.group(1)} 表示{m.group(2)}")
            else:
                pairs.append(e)
        sentence += f"取值含义：{'；'.join(pairs)}。"
    if field.get("example"):
        sentence += f"示例值为 {field['example']}。"
    return sentence


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("md_file")
    parser.add_argument("--id-prefix", required=True,
                         help='chunk_id prefix already used for this doc\'s other (A类, hand-chunked) '
                              'chunks in the same children.jsonl, e.g. "whschedulenotify" for '
                              'whschedulenotify-c01..c07 -- produces "<prefix>-field-<name>" per field, '
                              'never colliding with the existing "<prefix>-cNN" ids.')
    parser.add_argument("--level2-category", default="Webhook通知")
    parser.add_argument("--doc-type", default="字段说明")
    parser.add_argument("--doc-topic", default="",
                         help='Short topic anchor prefixed onto every field\'s embedded text, e.g. '
                              '"航变通知（order.schedulechange webhook）" -- see field_to_text() '
                              'docstring for why this matters: real customer questions almost always '
                              'name the topic (the notification/event type), not just the bare field, '
                              'and a bare-field chunk with no topic anchor scores much worse against '
                              'those topic-inclusive queries than one that carries its own topic. '
                              'Leave unset only for a doc with no natural short topic name.')
    parser.add_argument("--replace-chunk-id", nargs="*", default=[],
                         help="chunk_id(s) of the old merged-blob chunk(s) this replaces (e.g. the old "
                              "whschedulenotify-c06) -- removed from children.jsonl before writing the "
                              "new per-field chunks so the diluted chunk doesn't linger alongside them.")
    args = parser.parse_args()

    md_path = Path(args.md_file).resolve()
    md_text = md_path.read_text(encoding="utf-8")
    block = extract_mode_tab_block(md_text)
    fields = parse_fields(block)
    if not fields:
        raise SystemExit("Parsed 0 fields out of the 模式 tab block -- check the block's markup didn't drift "
                          "from the **name** + bullet-list convention this script expects.")

    source_path = str(md_path).split("API文档", 1)[1].lstrip("\\/").replace("\\", "/")
    chunks = []
    for f in fields:
        safe_name = f["name"].replace("[]", "-arr").replace(".", "-")
        chunks.append({
            "chunk_id": f"{args.id_prefix}-field-{safe_name}",
            "doc_type": args.doc_type,
            "level1_category": "产品指南",
            "level2_category": args.level2_category,
            "applicable_carrier": "通用",
            "section": f"字段：{f['name']}",
            "source_path": source_path,
            "text": field_to_text(f, args.doc_topic),
        })

    print(f"=== {len(chunks)} field chunks ===")
    for c in chunks:
        print(f"{c['chunk_id']}: {c['text']}")

    out_dir = md_path.parent / "_rag-chunks"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "children.jsonl"
    existing = []
    if out_file.exists():
        existing = [json.loads(l) for l in out_file.read_text(encoding="utf-8").splitlines() if l.strip()]
        drop_ids = set(args.replace_chunk_id)
        existing = [c for c in existing if c.get("chunk_id") not in drop_ids]

    with open(out_file, "w", encoding="utf-8") as f:
        for c in existing + chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"\nWritten to {out_file} ({len(existing)} kept + {len(chunks)} new = {len(existing) + len(chunks)} total)")


if __name__ == "__main__":
    main()
