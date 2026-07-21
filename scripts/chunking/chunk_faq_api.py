"""
Parse a troubleshooting-faqs/*.md file into Q&A chunks.

These files are messier than the 帮助中心 FAQ format: headings sometimes
repeat verbatim -- either the same question restated as a short ####
teaser and a longer ### answer (a GitBook export artifact), or a generic
label like "需要解决的问题"/"重要规则" reused once per numbered section
with different content each time. Rather than guessing which case applies
(a prior version tried, and silently dropped 8 real answers on
启动检查清单.md by merging reused-label repeats it shouldn't have), every
occurrence is kept as its own chunk; repeats past the first are
disambiguated with their enclosing ### section in the question text so
they stay meaningful and searchable on their own. Some files also embed a
large reference table (e.g. payment card requirements by airline)
mid-document; that gets extracted as structured JSON, not folded into a
QA chunk.

Usage:
    python chunk_faq_api.py "<path>" --level2-category "支付"
"""
import argparse
import html
import json
import re
from pathlib import Path


def strip_boilerplate(text: str) -> str:
    # Strip GitBook wrapper tags and retain the visible content they enclose.
    text = re.sub(r"\{%[^}]*%\}", "", text)
    text = re.sub(r"<a href.*?</a>", "", text)
    return text


def clean_markdown_text(text: str) -> str:
    """Strip inline markdown formatting markers from otherwise-real prose,
    keeping the underlying text -- see chunk_disambiguation.py's function of
    the same name for the full rationale. Safe to apply anywhere here (unlike
    chunk_disambiguation.py, nothing downstream re-parses backticks out of
    already-cleaned text)."""
    text = html.unescape(text)  # decode &#x624D; etc -- confirmed leaking into 资讯 chunks otherwise
    text = re.sub(r"\\\n", "\n", text)  # hard line break
    text = re.sub(r"\\([*_`\[\]()#>\\])", r"\1", text)  # un-escape markdown escapes FIRST -- GitBook exports widely escape ** and ` inside blockquotes (e.g. "\*\*Dependency:\*\*"), which otherwise survive every regex below untouched since they no longer look like real markdown syntax
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
    text = re.sub(r"(?m)^(?:>\s?)*#{1,6}\s+", "", text)  # handles "### h" and repeated-blockquoted "> > ### h"
    text = re.sub(r"(?m)^(?:>\s?)+", "", text)  # strip one or more leading blockquote markers (nested quotes leave a second one otherwise)
    return text


def _visible_after_stripping_links(text: str) -> str:
    """Text with markdown links removed entirely (label included) and
    formatting markers stripped -- distinguishes a pure link-list/navigation
    block (e.g. "使用：" + bullet links to other pages, safe to drop like
    "相关页面") from a section that has real prose/checklist content of its
    own, even though neither is phrased as a "### heading?" question."""
    stripped = re.sub(r"\[[^\]]*\]\([^)]*\)", "", text)
    stripped = re.sub(r"[*_`>#\-\s]", "", stripped)
    return stripped


def extract_markdown_table(text: str) -> tuple[str, list[dict]] | None:
    m = re.search(r"(\|[^\n]+\|\n\|[-: ]+\|[^\n]+\n(?:\|[^\n]+\|\n?)+)", text)
    if not m:
        return None
    block = m.group(1)
    lines = [l for l in block.splitlines() if l.strip().startswith("|")]
    header = [c.strip() for c in lines[0].strip("|").split("|")]
    rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells)))
    return block, rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("md_file")
    parser.add_argument("--level2-category", required=True)
    parser.add_argument("--level1-category", default="支持与参考")
    args = parser.parse_args()

    md_path = Path(args.md_file)
    text = strip_boilerplate(md_path.read_text(encoding="utf-8"))

    title_m = re.search(r"^# (.+)$", text, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else md_path.stem
    # maxsplit=1, take [1] not [-1] — same dormant-bug fix as chunk_disambiguation.py.
    source_path = str(md_path).split("API文档", 1)[1].lstrip("\\/").replace("\\", "/")

    # pull out the reference table (if any) before splitting into Q&A, so its
    # pipe characters don't get mistaken for section content
    table_info = extract_markdown_table(text)
    if table_info:
        block, rows = table_info
        text = text.replace(block, "")
        if rows:
            out_dir = md_path.parent / "_rag-chunks"
            out_dir.mkdir(exist_ok=True)
            with open(out_dir / f"table-{md_path.stem}.json", "w", encoding="utf-8") as f:
                json.dump({"source_path": source_path, "rows": rows}, f, ensure_ascii=False, indent=2)

    # split on any ### or #### heading that isn't a known non-QA section
    non_qa_headings = {"常见问题", "相关页面"}  # structural group wrappers, always pure nav
    parts = re.split(r"\n(#{3,4}) (.+?)\n", text)
    # parts[0] = intro text before first heading; then triples of (marker, heading, body)
    qa = {}  # heading (possibly disambiguated) -> (answer, is_question)
    order = []
    current_section = None    # nearest preceding ### heading, for disambiguation labels only

    # parts[0]: text between the H1 title and the first ###/#### heading was
    # previously dropped entirely (nothing here ever read it) -- confirmed
    # real content on 入门指南.md:9-15, a purpose statement + bullet list of
    # what the page covers, not boilerplate. Given chunk_id "q00" directly
    # (not folded into `order`/the enumerate() below) so adding/removing it
    # never renumbers every other question's chunk_id on this page --
    # chunk_id churn on an unrelated re-run defeats ingest_*.py's reconcile()
    # (stale-id cleanup keyed on chunk_id) and any external references.
    intro = re.sub(r"\n+", " ", parts[0]).strip() if parts else ""
    intro_chunk = None
    if intro and len(_visible_after_stripping_links(intro)) >= 6:
        intro_chunk = {
            "chunk_id": f"{md_path.stem}-q00",
            "doc_type": "FAQ补充说明",
            "level1_category": args.level1_category,
            "level2_category": args.level2_category,
            "topic": title,
            "source_path": source_path,
            "question": title,
            "answer": clean_markdown_text(intro),
        }

    i = 1
    while i < len(parts) - 2:
        marker = parts[i]
        heading = parts[i + 1].strip()
        body_start = i + 2
        body = parts[body_start] if body_start < len(parts) else ""
        i += 3
        if heading in non_qa_headings:
            continue
        body = re.sub(r"\\\n", " ", body).strip()
        body = re.sub(r"\n{2,}", " ", body).strip()
        is_question = "？" in heading or "?" in heading
        if not is_question and len(_visible_after_stripping_links(body)) < 6:
            continue  # not a question AND not much more than a link list (e.g. "使用：" + links) -- same rationale as 相关页面
        heading_clean, body_clean = clean_markdown_text(heading), clean_markdown_text(body)

        if marker == "###":
            current_section = heading_clean

        if heading_clean not in qa:
            key = heading_clean
        else:
            # Repeated heading text. This used to merge-by-longest-body on
            # the assumption every repeat is the same GitBook artifact
            # (a short #### teaser immediately followed by the full ###
            # answer for one question) -- but a heading can also be a
            # reused generic label (e.g. "需要解决的问题"/"重要规则"
            # repeating once per numbered part in a checklist doc) with
            # genuinely different content each time. Telling the two
            # apart reliably (adjacency alone missed a real teaser/full
            # pair separated by unrelated Q&A in between; content
            # similarity adds its own threshold-tuning risk) isn't worth
            # it: keeping one harmless near-duplicate chunk costs nothing,
            # silently dropping a real answer does (confirmed: 8 real Q&A
            # entries lost this way on 启动检查清单.md). Always keep every
            # occurrence, disambiguated with the enclosing ### section so
            # each is still a meaningful, searchable question on its own.
            # Guard against self-reference: if THIS repeat is itself the
            # ### heading that just became current_section (a flat file
            # with no distinct subsection grouping around the repeat,
            # e.g. 入门指南.md), labelling it with itself is meaningless --
            # fall through to the plain numeric suffix instead.
            section_label = current_section if current_section != heading_clean else None
            key = f"{heading_clean}（{section_label}）" if section_label else heading_clean
            base_key, n = key, 2
            while key in qa:
                key = f"{base_key}·{n}"
                n += 1

        order.append(key)
        qa[key] = (body_clean, is_question)

    chunks = [intro_chunk] if intro_chunk else []
    for idx, q in enumerate(order, 1):
        answer, is_question = qa[q]
        chunks.append({
            "chunk_id": f"{md_path.stem}-q{idx:02d}",
            "doc_type": "FAQ" if is_question else "FAQ补充说明",
            "level1_category": args.level1_category,
            "level2_category": args.level2_category,
            "topic": title,
            "source_path": source_path,
            "question": q,
            "answer": answer,
        })

    out_dir = md_path.parent / "_rag-chunks"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "faq-chunks.jsonl"
    existing = []
    if out_file.exists():
        existing = [json.loads(l) for l in out_file.read_text(encoding="utf-8").splitlines() if l.strip()]
        existing = [c for c in existing if c.get("source_path") != source_path]
    with open(out_file, "w", encoding="utf-8") as f:
        for c in existing + chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    print(f"{md_path.name}: {len(chunks)} QA chunks" + (f", table with {len(table_info[1])} rows" if table_info else ""))
    for c in chunks[:3]:
        print(f"  Q: {c['question']}")


if __name__ == "__main__":
    main()
