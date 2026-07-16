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
import html
import json
import re
from pathlib import Path


def strip_boilerplate(text: str) -> str:
    # Retain visible hint text; remove only GitBook component tags below.
    # Other GitBook component tags ({% stepper %}/{% step %}/{% endstep %}/
    # {% endstepper %}/{% file ... %}) wrap real content (unlike {% hint %},
    # whose content is a throwaway "ask Eva" callout) -- strip just the tags,
    # not what's between them. Confirmed leaking into 34 chunks across
    # C类/产品总览/资讯 before this fix.
    text = re.sub(r"\{%[^}]*%\}", "", text)
    text = re.sub(r"<a href.*?</a>", "", text)
    return text


def clean_markdown_text(text: str) -> str:
    """Strip inline markdown formatting markers from otherwise-real prose,
    keeping the underlying text. strip_boilerplate() above removes GitBook
    structural noise ({% hint %}, <a> tags); this handles the separate,
    previously-unaddressed problem of **/`/[]()/#/> syntax leaking verbatim
    into embedded chunk text (confirmed for real, e.g. a chunk's text
    containing literal "`search.do`" backticks) -- noise tokens the
    embedding model tokenizes like any other character without conveying
    the formatting they were meant to signal.

    Must run AFTER extract_compares_fallback() has scanned the raw
    "简要回答" section for backtick-quoted tokens -- that regex needs the
    literal backticks intact, so this is applied at chunk-build time in
    main(), not inside split_h3_sections()/extract_intro().
    """
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


def _visible_after_stripping_links(text: str) -> str:
    """Text with markdown links removed entirely (label included, not just
    the URL) and formatting markers stripped -- used to tell a section with
    real prose apart from one that's just a nav stub ("使用：" + a bullet
    list of links), so the intro-recovery fix below doesn't also start
    keeping pure link lists that were correctly being skipped before."""
    stripped = re.sub(r"\[[^\]]*\]\([^)]*\)", "", text)
    stripped = re.sub(r"[*_`>#\-]", "", stripped)
    return re.sub(r"\s+", "", stripped)


def extract_intro(text: str) -> str:
    """Text between the H1 title and the first H3 heading. split_h3_sections()
    below only returns parts[1:] -- this part (parts[0]) was previously
    silently dropped by every caller, even though it's often a real,
    non-boilerplate purpose statement (confirmed on 搜索 vs 报价.md:9,
    "当您需要在 search.do 和 getOffers.do 之间做选择时，使用此页面。", which
    had no chunk anywhere in the corpus before this fix)."""
    body = re.sub(r"^# .+?\n", "", text, count=1)
    first_h3 = re.search(r"\n### ", body)
    intro = body[: first_h3.start()] if first_h3 else body
    # Newlines are collapsed to spaces by the CALLER in main(), AFTER
    # clean_markdown_text() has run -- not here. clean_markdown_text()'s
    # bold/italic regexes are deliberately scoped to a single line (so a
    # bullet list's lone "* " markers can't pair up with each other across
    # items and get stripped as if they were an *italic span*); collapsing
    # "\n" to " " before cleaning erases that boundary and lets exactly that
    # happen. See split_h3_sections() below for the same fix.
    return intro.strip()


def split_h3_sections(body: str) -> list[tuple[str, str]]:
    parts = re.split(r"\n### ", body)
    sections = []
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
        # NOT collapsed to spaces here -- see extract_intro()'s comment above;
        # the caller (main()) cleans markdown first, then collapses newlines.
        content = content.strip()
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
    # logic below. Use a short content hash instead — not pretty, but
    # guaranteed unique.
    #
    # Hash source_path (the canonical, invocation-independent relative path),
    # NOT str(md_path) -- md_path is whatever the caller happened to pass on
    # the command line (absolute vs relative, forward vs back slashes), so
    # hashing it directly made the slug -- and therefore which existing
    # chunk_ids get recognized as "already written by this file" below --
    # depend on invocation style. Two runs of the same file with differently
    # -formed paths produced two different slugs, so the merge/dedup filter
    # never matched the old chunks and silently left duplicates instead of
    # replacing them (confirmed for real: 搜索 vs 报价.md ended up with both
    # an absolute-path-hashed and a relative-path-hashed copy of every chunk
    # after two reruns with different path forms).
    source_path = str(md_path).split("API文档", 1)[1].lstrip("\\/").replace("\\", "/")
    path_hash = hashlib.md5(source_path.encode("utf-8")).hexdigest()[:8]
    ascii_hint = re.sub(r"[^a-zA-Z0-9]+", "", title.lower())[:8]
    slug = f"{ascii_hint}{path_hash}" if ascii_hint else path_hash
    chunks = []

    intro = extract_intro(text)
    if intro and len(_visible_after_stripping_links(intro)) >= 6:
        intro_clean = re.sub(r"\n+", " ", clean_markdown_text(intro)).strip()
        chunks.append({
            "chunk_id": f"{slug}-c00",
            "doc_type": "对比消歧",
            "compares": compares,
            "level1_category": args.level1_category,
            "level2_category": args.level2_category,
            "source_path": source_path,
            "section": "简介",
            "text": f"{'/'.join(compares) if compares else title}：{intro_clean}",
        })

    skip_headings = {"相关页面"}  # pure link lists, no retrievable content
    for i, (heading, content) in enumerate(sections, 1):
        if heading in skip_headings or not content:
            continue
        heading = clean_markdown_text(heading)
        content = re.sub(r"\n+", " ", clean_markdown_text(content)).strip()
        chunks.append({
            "chunk_id": f"{slug}-c{i:02d}",
            "doc_type": "对比消歧",
            "compares": compares,
            "level1_category": args.level1_category,
            "level2_category": args.level2_category,
            # maxsplit=1, take [1] not [-1]: dormant version of the bug fixed in
            # chunk_product_intro.py — no current API文档 filename contains
            # "API文档" itself, but split(marker)[-1] would silently break the
            # moment one did, so fix the pattern defensively here too.
            "source_path": source_path,
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
