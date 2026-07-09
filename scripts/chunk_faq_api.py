"""
Parse a troubleshooting-faqs/*.md file into Q&A chunks.

These files are messier than the 帮助中心 FAQ format: many questions appear
TWICE — once as #### (short teaser answer) and again as ### with the exact
same question text (longer/more complete answer) — a GitBook artifact, not
intentional duplication. We dedupe by question text and keep the longer
answer. Some files also embed a large reference table (e.g. payment card
requirements by airline) mid-document; that gets extracted as structured
JSON, not folded into a QA chunk.

Usage:
    python chunk_faq_api.py "<path>" --level2-category "支付"
"""
import argparse
import json
import re
from pathlib import Path


def strip_boilerplate(text: str) -> str:
    text = re.sub(r"\{% hint.*?%\}.*?\{% endhint %\}", "", text, flags=re.DOTALL)
    text = re.sub(r"<a href.*?</a>", "", text)
    return text


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
    source_path = str(md_path).split("API文档")[-1].lstrip("\\/").replace("\\", "/")

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
    non_qa_headings = {"常见问题", "相关页面"}
    parts = re.split(r"\n(#{3,4}) (.+?)\n", text)
    # parts[0] = intro text before first heading; then triples of (marker, heading, body)
    qa = {}  # question -> answer, keep longer answer on duplicate
    order = []
    i = 1
    while i < len(parts) - 2:
        heading = parts[i + 1].strip()
        body_start = i + 2
        body = parts[body_start] if body_start < len(parts) else ""
        i += 3
        if heading in non_qa_headings:
            continue
        if "？" not in heading and "?" not in heading:
            continue  # not phrased as a question, skip (e.g. stray subheadings)
        body = re.sub(r"\\\n", " ", body).strip()
        body = re.sub(r"\n{2,}", " ", body).strip()
        if heading not in qa or len(body) > len(qa[heading]):
            if heading not in qa:
                order.append(heading)
            qa[heading] = body

    chunks = []
    for idx, q in enumerate(order, 1):
        chunks.append({
            "chunk_id": f"{md_path.stem}-q{idx:02d}",
            "doc_type": "FAQ",
            "level1_category": args.level1_category,
            "level2_category": args.level2_category,
            "topic": title,
            "source_path": source_path,
            "question": q,
            "answer": qa[q],
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
