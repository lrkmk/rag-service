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
import html
import json
import os
import re


def strip_boilerplate(text: str) -> str:
    text = re.sub(r"\{% hint.*?%\}.*?\{% endhint %\}", "", text, flags=re.DOTALL)
    # Other GitBook component tags wrap real content (unlike {% hint %},
    # whose content is a throwaway "ask Eva" callout) -- strip just the tags.
    text = re.sub(r"\{%[^}]*%\}", "", text)
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
        # NOT collapsed to spaces here -- see extract_intro()'s comment below.
        # clean_markdown_text() is scoped to a single line on purpose (so a
        # bullet list's lone "* " markers can't pair up across items and get
        # stripped as if they were an *italic span* -- confirmed for real on
        # "Atlas 产品介绍.md"'s "按角色快速开始" bullet-of-links section);
        # collapsing "\n" to " " before that cleaning runs erases the
        # boundary that prevents it. The caller (main()) cleans first, then
        # collapses newlines.
        content = content.strip()
        sections.append((heading, content))
    return sections


def clean_markdown_text(text: str) -> str:
    """Strip inline markdown formatting markers from otherwise-real prose,
    keeping the underlying text -- see chunk_disambiguation.py's function of
    the same name for the full rationale."""
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


def extract_intro(text: str) -> str:
    """Text between the H1 title and the first H3 heading -- split_h3_sections()
    only returns parts[1:], so this was silently dropped whenever a page HAD
    H3 sections (the no-H3 fallback branch in main() already keeps the whole
    page, so it wasn't affected)."""
    body = re.sub(r"^# .+?\n", "", text, count=1)
    first_h3 = re.search(r"\n### ", body)
    intro = body[: first_h3.start()] if first_h3 else body
    # Newlines collapsed by the caller AFTER clean_markdown_text() runs --
    # see split_h3_sections()'s comment for why.
    return intro.strip()


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
        if sections:
            intro = extract_intro(text)
            intro_visible = re.sub(r"[*_`>#\-\s]", "", re.sub(r"\[[^\]]*\]\([^)]*\)", "", intro))
            if intro and len(intro_visible) >= 6:
                intro_clean = re.sub(r"\n+", " ", clean_markdown_text(intro)).strip()
                all_chunks.append({
                    "chunk_id": f"intro-{slug}-c00",
                    "doc_type": "产品总览",
                    "level1_category": "产品介绍",
                    "level2_category": "产品总览",
                    "title": title,
                    "section": "简介",
                    "source_path": source_path,
                    "text": f"{title}：{intro_clean}",
                })
        if not sections:
            # no H3 headings (e.g. 按角色快速开始 pages use a flatter structure) —
            # keep the whole page as one chunk rather than dropping it. Clean
            # BEFORE collapsing newlines (not after) -- same ordering fix as
            # split_h3_sections()/extract_intro() above.
            raw_body = text[title_m.end():] if title_m else text
            body = re.sub(r"\n+", " ", clean_markdown_text(raw_body)).strip()
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
            heading = clean_markdown_text(heading)
            content = re.sub(r"\n+", " ", clean_markdown_text(content)).strip()
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
