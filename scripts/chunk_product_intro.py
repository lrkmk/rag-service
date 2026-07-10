"""
Chunk 产品总览 pages (doc/产品介绍/产品总览/*.md) plus the two standalone
concept pages that sit directly under doc/产品介绍/ (Atlas Pay.md, Smart
Search.md — same H3/H4 heading convention, just not filed under a
subfolder). Evergreen concept prose, not time-stamped news (see
chunk_product_news.py for Atlas资讯), so no recency handling needed here.

All pages share one heading convention: H3 (###) sections, with H4 (####)
sub-items nested inside. Splits by H3, same as chunk_disambiguation.py's
split_h3_sections — H4s get folded into inline 【label】 markers rather than
becoming their own chunks, since each H4 here is a short facet of its parent
H3's point (e.g. "### 支付方式" / "#### VCC 透传"), not independently
retrievable content.

Usage:
    python chunk_product_intro.py  # processes 产品总览/ + the 2 standalone pages
"""
import argparse
import glob
import json
import os
import re


def strip_boilerplate(text: str) -> str:
    text = re.sub(r"\{% hint.*?%\}.*?\{% endhint %\}", "", text, flags=re.DOTALL)
    text = re.sub(r"<a href.*?</a>", "", text)
    text = re.sub(r"&#x20;", " ", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    return text


def split_h3_sections(body: str) -> list[tuple[str, str]]:
    parts = re.split(r"\n### ", body)
    sections = []
    for chunk in parts[1:]:
        lines = chunk.split("\n", 1)
        heading = lines[0].strip()
        content = lines[1] if len(lines) > 1 else ""
        # Substitute BEFORE strip(): if this section's first line after the
        # heading is itself an H4 (no lead-in prose), strip() would eat the
        # leading \n that (?:^|\n) needs to anchor on, silently leaving that
        # one #### line unconverted while later ones in the same section
        # still matched (this bit chunk_disambiguation.py for real — the
        # first H4 of any section with no lead-in prose stayed literal
        # "#### heading" text instead of becoming inline 【heading】).
        content = re.sub(r"(?:^|\n)#### (.+?)(?:\n|$)", r"\n【\1】", content)
        content = re.sub(r"\n+", " ", content).strip()
        sections.append((heading, content))
    return sections


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    product_intro_root = os.path.join(repo_root, "doc", "产品介绍")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--intro-dir",
        default=os.path.join(product_intro_root, "产品总览"),
        help="Output directory (and primary source folder) for the combined children.jsonl.",
    )
    args = parser.parse_args()

    # 产品总览/*.md (the 11 subfolder pages) + the 2 standalone top-level pages
    # (Atlas Pay.md, Smart Search.md) — same H3/H4 convention, just not filed
    # under a subfolder, so they'd otherwise never get chunked at all (this
    # was a real gap: both sat with zero coverage until this was added).
    files = sorted(glob.glob(os.path.join(args.intro_dir, "*.md")))
    files += sorted(glob.glob(os.path.join(product_intro_root, "*.md")))
    all_chunks = []
    for fpath in files:
        text = strip_boilerplate(open(fpath, encoding="utf-8").read())
        title_m = re.search(r"^# (.+)$", text, re.MULTILINE)
        title = title_m.group(1).strip() if title_m else os.path.basename(fpath)[:-3]
        # maxsplit=1, take [1] not [-1]: split(marker) with no limit splits on
        # EVERY occurrence, and [-1] grabs everything after the LAST one — this
        # silently broke on "Atlas 产品介绍.md" (the corpus root name "产品介绍"
        # also appears inside that file's own title), producing source_path
        # "产品介绍/.md" instead of the real path. Only split on the first
        # occurrence (the folder name) so a title containing the corpus name
        # can't shift where the path gets cut.
        source_path = fpath.split("产品介绍", 1)[1].lstrip("\\/").replace("\\", "/")
        source_path = "产品介绍/" + source_path

        sections = split_h3_sections(text)
        slug = re.sub(r"[^a-zA-Z0-9]+", "", title.lower())[:16] or re.sub(r"\W+", "", os.path.basename(fpath))[:16]
        if not sections:
            # no H3 headings (e.g. 按角色快速开始 pages use a flatter structure) —
            # keep the whole page as one chunk rather than dropping it.
            body = re.sub(r"\n+", " ", text[title_m.end():] if title_m else text).strip()
            all_chunks.append({
                "chunk_id": f"intro-{slug}-c01",
                "doc_type": "产品总览",
                "level1_category": "产品介绍",
                "level2_category": "产品总览",
                "title": title,
                "source_path": source_path,
                "text": f"{title}：{body}",
            })
            continue
        for i, (heading, content) in enumerate(sections, 1):
            if not content:
                continue
            all_chunks.append({
                "chunk_id": f"intro-{slug}-c{i:02d}",
                "doc_type": "产品总览",
                "level1_category": "产品介绍",
                "level2_category": "产品总览",
                "title": title,
                "section": heading,
                "source_path": source_path,
                "text": f"{title}：{heading}。{content}",
            })

    out_dir = os.path.join(args.intro_dir, "_rag-chunks")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "children.jsonl")
    with open(out_file, "w", encoding="utf-8") as f:
        for c in all_chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"{len(all_chunks)} intro chunks from {len(files)} files -> {out_file}")


if __name__ == "__main__":
    main()
