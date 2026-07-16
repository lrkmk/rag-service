"""
Parse a 帮助中心/10-常见问题/*.md file into Q&A chunks.

Different source format from chunk_faq_api.py's GitBook heading-based FAQs:
these pages have no ###/#### headings at all. Each Q&A pair is a bold
"**问题N：...？**" marker followed by an answer starting with 答：/答案：/回答：
-- and both the marker wording AND whether the colon sits inside or outside
the bold span vary within a single file (e.g. 功能和内容相关.md alternates
between "**问题2：**&#x41;tlas**提供...**" -- bold interrupted mid-question by
an HTML-entity-encoded "A", "**答案**：..." -- colon outside the bold, and
"**答案：**..." -- colon inside). Rather than parsing those bold boundaries to
find the split points, clean_markdown_text() runs over the WHOLE file first
(collapsing every one of those variants down to plain text with entities
decoded), and splitting into 问题N/答案 pairs happens afterward against the
now-uniform plain text -- much less fragile than trying to match the several
different original markup shapes directly.

Unlike chunk_faq_api.py, answers here are NOT collapsed to a single line --
matches the existing (hand-authored) 帮助中心 FAQ jsonl convention of keeping
paragraph breaks and bullet sub-lists intact within one answer.

Usage:
    python chunk_faq_bangzhu.py "<path>" --slug pay
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
    the same name for the full rationale (shared across all six chunk_*.py
    scripts; kept as a duplicated copy per script rather than a shared
    import, matching this codebase's existing convention of standalone,
    independently-runnable chunking scripts)."""
    text = html.unescape(text)  # decode &#x624D; / &#x41; etc -- this corpus uses both
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


QUESTION_MARKER = re.compile(r"问题\s*\d+\s*[：:]\s*")
# Longest/most-specific alternatives first: at a given "答" position, try
# "答案" then "回答" before falling back to bare "答" so "答案：" doesn't get
# mis-split as bare "答" leaving a stray "案：" glued onto the answer text.
ANSWER_MARKER = re.compile(r"答案[：:]|回答[：:]|答[：:]")


def parse_qa_pairs(body: str) -> list[tuple[str, str]]:
    """`body` must already be clean_markdown_text()-processed. Splits on
    "问题N：" markers first, then for each resulting block finds the first
    答/答案/回答 marker to separate the question text from the answer text."""
    parts = QUESTION_MARKER.split(body)
    # parts[0] is whatever precedes the first "问题N：" -- on this page type
    # that's just the (already-stripped) H1 title's trailing whitespace, not
    # a real intro paragraph (confirmed on all 4 existing files: title is
    # immediately followed by "**问题1：..."). Nothing dropped here in
    # practice, unlike chunk_disambiguation.py/chunk_faq_api.py's intro-loss
    # bug, since there IS no intro on this format.
    pairs = []
    for chunk in parts[1:]:
        m = ANSWER_MARKER.search(chunk)
        if not m:
            continue  # no answer marker found in this block -- skip rather than guess at a split point
        question = chunk[: m.start()].strip()
        answer = re.sub(r"\n{3,}", "\n\n", chunk[m.end() :]).strip()
        if question and answer:
            pairs.append((question, answer))
    return pairs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("md_file")
    parser.add_argument("--slug", required=True, help="short id used for chunk_id/parent_id, e.g. 'pay'")
    args = parser.parse_args()

    md_path = Path(args.md_file)
    text = strip_boilerplate(md_path.read_text(encoding="utf-8"))

    title_m = re.search(r"^# (.+)$", text, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else md_path.stem
    body = clean_markdown_text(text[title_m.end() :] if title_m else text)

    source_path = "10-常见问题/" + md_path.name
    parent_id = f"faq-{args.slug}"

    chunks = []
    for idx, (question, answer) in enumerate(parse_qa_pairs(body), 1):
        chunks.append({
            "chunk_id": f"{parent_id}-q{idx:02d}",
            "parent_id": parent_id,
            "topic": title,
            "level1_category": "常见问题",
            "level2_category": title,
            "question": question,
            "answer": answer,
            "source_path": source_path,
        })

    out_dir = md_path.parent / "_rag-chunks"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"{md_path.stem}.jsonl"
    with open(out_file, "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    print(f"{md_path.name}: {len(chunks)} QA chunks -> {out_file}")
    for c in chunks[:3]:
        print(f"  Q: {c['question']}")


if __name__ == "__main__":
    main()
