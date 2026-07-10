"""
Parse a "对比消歧" (disambiguation) doc — the fixed GitBook template used
throughout API文档 for comparing 2-4 similar concepts/codes/endpoints
(### 简要回答 / ### 常见问题 / ### 核心区别 / ... / ### 相关页面).

Chunking rule: split by H3 section, but NEVER split the compared items apart
within a section — each chunk still covers all sides of the comparison,
because the entire point of these docs is contrast (see the API文档 chunking
design note from 04-售后票务/退票/_rag-chunks/README.md, principle 2, applied
here to comparisons instead of policy rule units).

`compares` metadata is auto-extracted from the title when it matches an
"A vs B (vs C...)" pattern; otherwise falls back to scanning for backtick-
quoted or bold-quoted short tokens mentioned in the "简要回答" section (e.g.
重启点.md has no "vs" in its title but is still a 3-way comparison).

Usage:
    python chunk_disambiguation.py "<path to markdown file>" --level2-category "错误码"
"""

import argparse
import hashlib
import json
import re
from pathlib import Path


def strip_boilerplate(text: str) -> str:
    text = re.sub(r"\{% hint.*?%\}.*?\{% endhint %\}", "", text, flags=re.DOTALL)
    text = re.sub(r"<a href.*?</a>", "", text)
    return text


def extract_compares_from_title(title: str) -> list[str] | None:
    if " vs " not in title:
        return None
    parts = [p.strip(" `") for p in title.split(" vs ")]
    return parts if len(parts) >= 2 else None


def extract_compares_fallback(brief_answer_text: str) -> list[str]:
    # pull backtick-quoted tokens (`search.do`, `429`, etc.) mentioned in the brief-answer section
    tokens = re.findall(r"`([^`]+)`", brief_answer_text)
    seen = []
    for t in tokens:
        if t not in seen:
            seen.append(t)
    return seen[:5]  # cap — this is a fallback heuristic, not authoritative


def split_h3_sections(body: str) -> list[tuple[str, str]]:
    parts = re.split(r"\n### ", body)
    sections = []
    if parts and not parts[0].strip().startswith("###"):
        pass  # parts[0] is pre-first-H3 content, handled by caller separately
    for chunk in parts[1:]:
        lines = chunk.split("\n", 1)
        heading = lines[0].strip()
        content = lines[1] if len(lines) > 1 else ""
        # strip nested #### subheadings down to plain text but keep them as inline
        # labels. Substitute BEFORE strip(): stripping first eats the leading \n
        # that (?:^|\n) needs when a section's first line is itself an H4 (no
        # lead-in prose) — that silently left the first #### of a section as
        # literal "#### heading" text while later ones in the same section still
        # converted fine. Caught via the same bug in chunk_product_intro.py.
        content = re.sub(r"(?:^|\n)#### (.+?)(?:\n|$)", r"\n【\1】", content)
        content = re.sub(r"\n+", " ", content).strip()
        sections.append((heading, content))
    return sections


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("md_file")
    parser.add_argument("--level2-category", required=True)
    parser.add_argument("--level1-category", default="支持与参考")
    args = parser.parse_args()

    md_path = Path(args.md_file)
    text = md_path.read_text(encoding="utf-8")
    text = strip_boilerplate(text)

    title_m = re.search(r"^# (.+)$", text, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else md_path.stem

    compares = extract_compares_from_title(title)

    sections = split_h3_sections(text)
    if not compares:
        brief = next((c for h, c in sections if "简要回答" in h), "")
        compares = extract_compares_fallback(brief)

    # Slug must be unique per source file regardless of language. Stripping to
    # ASCII-only (as an earlier version did) silently collapsed distinct
    # Chinese titles like "获取报价 vs 获取报价价格" and "验证 vs 下单" to the
    # same slug ("vs"), which then clobbered each other via the merge/dedup
    # logic below. Use a short content hash of the full path instead — not
    # pretty, but guaranteed unique.
    path_hash = hashlib.md5(str(md_path).encode("utf-8")).hexdigest()[:8]
    ascii_hint = re.sub(r"[^a-zA-Z0-9]+", "", title.lower())[:8]
    slug = f"{ascii_hint}{path_hash}" if ascii_hint else path_hash
    chunks = []
    skip_headings = {"相关页面"}  # pure link lists, no retrievable content
    for i, (heading, content) in enumerate(sections, 1):
        if heading in skip_headings or not content:
            continue
        chunks.append({
            "chunk_id": f"{slug}-c{i:02d}",
            "doc_type": "对比消歧",
            "compares": compares,
            "level1_category": args.level1_category,
            "level2_category": args.level2_category,
            "source_path": str(md_path).split("API文档")[-1].lstrip("\\/").replace("\\", "/"),
            "section": heading,
            "text": f"{'/'.join(compares) if compares else title}：{heading}。{content}",
        })

    out_dir = md_path.parent / "_rag-chunks"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "children.jsonl"
    # merge into existing children.jsonl for this folder rather than overwrite, since
    # multiple disambiguation docs can live in the same folder (e.g. errors-handing)
    existing = []
    if out_file.exists():
        existing = [json.loads(l) for l in out_file.read_text(encoding="utf-8").splitlines() if l.strip()]
        existing = [c for c in existing if not c["chunk_id"].startswith(slug + "-c")]
    with open(out_file, "w", encoding="utf-8") as f:
        for c in existing + chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    print(f"{md_path.name}: compares={compares}, {len(chunks)} chunks -> {out_file}")


if __name__ == "__main__":
    main()
