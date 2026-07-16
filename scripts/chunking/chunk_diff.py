"""
Generate a visual diff between a source .md article and its produced RAG
chunks — pairs each source paragraph with the chunk that covers it, and
flags paragraphs that don't match any chunk (coverage gaps).

Chunk `text` is required to be verbatim source wording (see
.claude/skills/doc-chunking/references/manual-chunking.md's "find
boundaries, don't rewrite" rule — this applies to every content type in this
pipeline, not just the manually-chunked ones: the scripted chunkers extract
programmatically too, none of them paraphrase). That makes exact matching
the right primary check: a paragraph is COVERED only if it's a normalized
substring of some chunk's text, matching the skill doc's own rationale for
requiring verbatim text ("a coverage check can confirm a chunk's text is an
exact substring of the source instead of a fuzzy-similarity guess").

A paragraph that fails exact containment but still scores above threshold on
the old Jaccard character-shingle measure is reported as a SUSPECT, not
folded into "covered" — under the verbatim rule this should essentially
never happen for a genuinely-covered paragraph, so when it does it's a
signal worth a human look (paraphrasing, drift, or two source occurrences of
the same fact that were intentionally folded into one chunk per the skill
doc's dedup allowance) rather than something to silently wave through.
Everything else is a GAP: no chunk contains it, exactly or approximately.

Usage:
    python chunk_diff.py "<path to source .md>" [-o out.html] [--threshold 0.1]

    If --chunks isn't given, looks for children.jsonl in a sibling
    _rag-chunks/ folder (in the same directory as the source file) and
    filters to entries whose source_path matches the given doc.
"""

import argparse
import difflib
import html
import json
import re
from pathlib import Path

from clean_markdown_text import clean_markdown_text


def strip_boilerplate(text: str) -> str:
    # Retain visible hint text while removing GitBook's wrapper tags.
    text = re.sub(r"\{%[^}]*%\}", "", text)
    text = re.sub(r"<a href.*?</a>", "", text)
    text = re.sub(r"> For the complete documentation index.*?\n", "", text)
    return text


def html_table_to_text(match: re.Match) -> str:
    """Collapse an embedded HTML <table> into a flat text block so it still
    participates in paragraph splitting/matching, instead of vanishing."""
    cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", match.group(0), flags=re.DOTALL)
    cells = [re.sub(r"<[^>]+>", "", c).strip() for c in cells]
    return " / ".join(c for c in cells if c)


_LABEL_LINE = re.compile(r"^[\*_]*\s*\(?\d{1,2}[.）\)]\s*[\*_]*.{0,20}[\*_]*$")


def _is_label_like(text: str) -> bool:
    """Short pseudo-heading lines (bold numbering like '**1）航前申请**',
    '1.履约原则', '4.紧急退票', or a numbered link line like
    '**1.**[**自愿退票**](/very/long/url.md)') that these source docs use as
    informal sub-headers without real markdown '#' syntax. They carry no
    matchable content on their own and should attach to the paragraph that
    follows, not stand as their own block. Length is checked on the
    markdown-link-stripped text — a link line reads as short once its URL
    is removed, even though the raw line (with URL) is long.

    Terminal punctuation is NOT treated as proof of a complete thought —
    these docs routinely split one logical statement across a blank line,
    e.g. "不要这样做。" (6 chars, its own sentence, its own punctuation) is
    immediately followed by "会话已过期。" as the reason clause. A period
    doesn't mean "this line stands alone" here, so a short-enough block
    merges forward regardless of how it ends.
    """
    stripped = text.strip()
    visible = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", stripped)  # [label](url) -> label
    visible = re.sub(r"[*_]", "", visible).strip()
    if len(visible) <= 8:
        return True
    if len(visible) <= 20 and not visible.endswith(("。", "！", "？", ".", "!", "?", "：", ":")):
        return True
    return bool(_LABEL_LINE.match(stripped))


def split_paragraphs(text: str) -> list[dict]:
    """Returns a list of {heading_path, text} blocks. Headings (# through
    ####) update the running heading_path context; blank-line-separated
    text between headings becomes paragraph blocks tagged with that path.

    Two merge passes fix real fragmentation seen on these docs:
      1. A short label-like line (informal sub-heading with no '#' syntax,
         e.g. "**1）航前申请**") merges FORWARD into the next block instead
         of standing alone — alone it's just a few characters with nothing
         to match against.
      2. A block ending in "："/":" immediately followed by a block whose
         first line starts with "*"/"-" (a bullet list) merges together —
         these are one logical unit (intro sentence + its bullets) that a
         blank line between them would otherwise split apart.
    """
    text = re.sub(r"<table.*?</table>", html_table_to_text, text, flags=re.DOTALL)
    lines = text.split("\n")
    blocks = []
    heading_stack: list[str] = []
    buf: list[str] = []

    def flush():
        joined = "\n".join(buf).strip()
        buf.clear()
        if joined:
            blocks.append({"heading": heading_stack[-1] if heading_stack else "", "text": joined})

    for line in lines:
        m = re.match(r"^(#{1,4})\s+(.+)$", line)
        if m:
            flush()
            level = len(m.group(1))
            title = re.sub(r"[*_]", "", m.group(2)).strip()
            heading_stack = heading_stack[: level - 1] + [title]
            continue
        if line.strip() == "":
            flush()
        else:
            buf.append(line)
    flush()
    # Non-prose blocks carry no matchable text and showed up as false-
    # positive "gaps" in practice: bare image links (either markdown
    # ![](...) or an HTML <figure><img>... embed) never resemble any
    # chunk's prose, and a fenced code block (```json ... ```) is code, not
    # natural language — character-shingle matching against prose chunk
    # text is meaningless for it either way.
    _non_prose = re.compile(
        r"^!\[[^\]]*\]\([^)]*\)$"           # ![](url)
        r"|^<figure>.*</figure>$"            # <figure><img ...></figure>
        r"|^```.*```$",                      # fenced code block, single block after join
        re.DOTALL,
    )
    blocks = [b for b in blocks if len(b["text"]) > 1 and not _non_prose.match(b["text"].strip())]

    merged: list[dict] = []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        while _is_label_like(b["text"]) and i + 1 < len(blocks) and blocks[i + 1]["heading"] == b["heading"]:
            i += 1
            b = {"heading": b["heading"], "text": b["text"] + "\n" + blocks[i]["text"]}
        # A colon-ending line introduces whatever follows it (a bullet list,
        # a table-derived text block, another paragraph) — same fragmentation
        # pattern as the label-line case above, just triggered by punctuation
        # instead of line length. Not limited to bullets: the 受理范围 table
        # in this doc is introduced by a colon sentence with a blank line
        # before the <table>, which the html_table_to_text flattening turns
        # into an ordinary-looking next block with no special marker.
        while (
            b["text"].rstrip().endswith(("：", ":"))
            and i + 1 < len(blocks)
            and blocks[i + 1]["heading"] == b["heading"]
        ):
            i += 1
            b = {"heading": b["heading"], "text": b["text"] + "\n" + blocks[i]["text"]}
        merged.append(b)
        i += 1
    return merged


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8-sig").splitlines() if l.strip()]


def find_chunks_file(doc_path: Path) -> Path | None:
    candidates = list((doc_path.parent / "_rag-chunks").glob("*.jsonl"))
    return candidates[0] if candidates else None


def load_matching_chunks(chunks_path: Path, doc_path: Path) -> list[dict]:
    all_records = load_jsonl(chunks_path)
    target_name = doc_path.name

    # 帮助中心-style two-tier schema: children only carry parent_id, not
    # source_path directly — that lives on the sibling parents.jsonl record.
    # API文档-style flat schema: children already carry source_path. Handle
    # both by building a parent_id -> source_path map when a parents.jsonl
    # exists next to the children file, and falling back to it per-record.
    parent_source_path = {}
    parents_path = chunks_path.parent / "parents.jsonl"
    if parents_path.exists() and parents_path != chunks_path:
        for p in load_jsonl(parents_path):
            if p.get("article_id") and p.get("source_path"):
                parent_source_path[p["article_id"]] = p["source_path"]

    matched = []
    for r in all_records:
        sp = r.get("source_path") or parent_source_path.get(r.get("parent_id"), "")
        if sp.endswith(target_name):
            matched.append(r)
    return matched


def _shingles(text: str, n: int = 3) -> set[str]:
    """Character n-grams, whitespace/markdown-noise stripped. Used only for
    the SUSPECT tier (see best_match) after exact containment has already
    failed — Jaccard similarity over character shingles is tolerant of
    word-order/particle changes, which is what lets it flag "this looks like
    the same fact, but isn't a literal substring" (drift/paraphrase/an
    intentionally-folded duplicate) instead of just going quiet.
    """
    cleaned = re.sub(r"\s+", "", clean_markdown_text(text))
    if len(cleaned) < n:
        return {cleaned} if cleaned else set()
    return {cleaned[i : i + n] for i in range(len(cleaned) - n + 1)}


def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _normalized(text: str) -> str:
    # Use the SAME clean_markdown_text() the chunkers themselves run on field
    # text before it becomes `text`/`answer` (html.unescape, backslash-escape
    # un-escaping, GitBook {% %} tags, nested blockquotes, horizontal rules,
    # and -- unlike this module's old ad hoc noise regex -- markdown links
    # keep their visible label and drop the URL rather than concatenating
    # both into the comparison string). Comparing source and chunk text
    # through the exact same cleaner is what makes "normalized substring"
    # mean the same thing on both sides; a second, slightly different noise
    # regex here was a source of spurious SUSPECT/GAP flags on otherwise
    # verbatim-covered paragraphs (confirmed for real on 如何申请废票？.md's
    # "废票路径：&#x41;TRIP -> ..." paragraph, which only started matching
    # once entity-unescaping ran before the noise-strip -- clean_markdown_text
    # already does that as step 1).
    return re.sub(r"\s+", "", clean_markdown_text(text))


def best_match(paragraph: str, chunks: list[dict], threshold: float) -> tuple[str | None, float, str]:
    """Returns (chunk_id, ratio, status). status is one of:
      - "exact":  paragraph is a normalized substring of some chunk (or vice
                  versa) -- the real coverage signal now that chunk text is
                  required to be verbatim (see module docstring). ratio=1.0.
      - "fuzzy":  no exact containment, but Jaccard shingle similarity clears
                  `threshold` -- under the verbatim rule this shouldn't
                  happen for genuinely-covered content, so it's surfaced as
                  a SUSPECT needing a human look, not counted as covered.
      - "none":   no chunk resembles this paragraph at all -- a real gap.
    """
    # Containment check first: Jaccard alone under-scores a paragraph that
    # appears verbatim inside a much longer chunk (or vice versa), because
    # Jaccard's denominator is the *union* size — if one side is 3-4x the
    # other, even a 100%-precise overlap can land well under a reasonable
    # threshold. A paragraph that's a substring (or near-substring) of a
    # chunk's text — or contains the chunk's text — is unambiguously
    # covered regardless of the size ratio.
    # Minimum length matters here: a short generic phrase (e.g. "不要这样做",
    # 6 chars) is a substring of practically any chunk that happens to
    # contain it, so a low floor turns the containment check into a false-
    # positive machine on terse, repetitive phrasing. 10 chars is enough to
    # rule out one-clause boilerplate while still catching genuinely short
    # but distinctive sentences. A genuinely-covered paragraph shorter than
    # that still gets a fair shot via the Jaccard tier below (as "fuzzy",
    # not "exact" -- a labeling nuisance, not a missed gap).
    # A source paragraph can start with an inline pseudo-heading line ("1.
    # **什么是多币种账户？**") glued directly onto the body with no blank line
    # between them -- split_paragraphs() has no reason to split them into
    # separate blocks, so they arrive here as one unit. But the chunker
    # commonly folds that kind of numbered/bold label into the chunk's
    # `section` metadata rather than repeating it inline in `text` -- so the
    # label's own wording ("1什么是多币种账户") becomes a prefix the paragraph
    # has that the chunk doesn't, and containment fails even though the
    # actual body sentence that follows is 100% verbatim-covered. Retry
    # containment with that leading label line stripped before giving up.
    lines = paragraph.split("\n", 1)
    candidates = [paragraph]
    if len(lines) == 2 and _is_label_like(lines[0]):
        candidates.append(lines[1])

    for cand_paragraph in candidates:
        para_norm = _normalized(cand_paragraph)
        if len(para_norm) >= 10:
            for c in chunks:
                candidate_text = c.get("text") or (c.get("question", "") + " " + c.get("answer", ""))
                cand_norm = _normalized(candidate_text)
                if para_norm in cand_norm or cand_norm in para_norm:
                    return c.get("chunk_id"), 1.0, "exact"

    para_shingles = _shingles(paragraph)
    best_id, best_ratio = None, 0.0
    for c in chunks:
        candidate_text = c.get("text") or (c.get("question", "") + " " + c.get("answer", ""))
        ratio = _jaccard(para_shingles, _shingles(candidate_text))
        if ratio > best_ratio:
            best_ratio, best_id = ratio, c.get("chunk_id")
    if best_ratio >= threshold:
        return best_id, best_ratio, "fuzzy"
    return None, best_ratio, "none"


def render_html(doc_path: Path, pairs: list[dict], suspects: list[dict], gaps: list[dict], chunk_count: int) -> str:
    def esc(s):
        return html.escape(s or "")

    rows = []
    for p in pairs:
        rows.append(f"""
<div style="border:1px solid #ddd;border-radius:10px;margin-bottom:10px;overflow:hidden;">
  <div style="display:flex;justify-content:space-between;padding:8px 14px;background:#f5f5f5;font-size:13px;">
    <span style="font-weight:600;">{esc(p['heading'])}</span>
    <span style="color:#888;font-family:monospace;">{esc(p['chunk_id'])} · exact match</span>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;">
    <div style="padding:10px 14px;border-right:1px solid #eee;">
      <p style="font-size:11px;color:#999;margin:0 0 4px;text-transform:uppercase;">原文</p>
      <p style="font-size:13px;line-height:1.6;margin:0;white-space:pre-wrap;">{esc(p['src_text'])}</p>
    </div>
    <div style="padding:10px 14px;">
      <p style="font-size:11px;color:#999;margin:0 0 4px;text-transform:uppercase;">切片结果</p>
      <p style="font-size:13px;line-height:1.6;margin:0;white-space:pre-wrap;">{esc(p['chunk_text'])}</p>
    </div>
  </div>
</div>""")

    for s in suspects:
        rows.append(f"""
<div style="border:1px solid #d9b95c;border-radius:10px;margin-bottom:10px;overflow:hidden;background:#fffbea;">
  <div style="display:flex;justify-content:space-between;padding:8px 14px;background:#fdf3d0;font-size:13px;">
    <span style="font-weight:600;">{esc(s['heading'])}</span>
    <span style="color:#8a6d1a;font-weight:600;">◐ 疑似改写/需复核 — {esc(s['chunk_id'])} · 相似度 {s['ratio']:.2f}（非精确匹配）</span>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;">
    <div style="padding:10px 14px;border-right:1px solid #f0e4b8;">
      <p style="font-size:11px;color:#999;margin:0 0 4px;text-transform:uppercase;">原文</p>
      <p style="font-size:13px;line-height:1.6;margin:0;white-space:pre-wrap;">{esc(s['src_text'])}</p>
    </div>
    <div style="padding:10px 14px;">
      <p style="font-size:11px;color:#999;margin:0 0 4px;text-transform:uppercase;">最相似的切片结果</p>
      <p style="font-size:13px;line-height:1.6;margin:0;white-space:pre-wrap;">{esc(s['chunk_text'])}</p>
    </div>
  </div>
</div>""")

    for g in gaps:
        rows.append(f"""
<div style="border:1px solid #e0a0a0;border-radius:10px;margin-bottom:10px;overflow:hidden;background:#fff5f5;">
  <div style="display:flex;justify-content:space-between;padding:8px 14px;background:#fbe4e4;font-size:13px;">
    <span style="font-weight:600;">{esc(g['heading'])}</span>
    <span style="color:#a33;font-weight:600;">⚠ 未覆盖（最佳相似度 {g['ratio']:.2f}）</span>
  </div>
  <div style="padding:10px 14px;">
    <p style="font-size:11px;color:#999;margin:0 0 4px;text-transform:uppercase;">原文</p>
    <p style="font-size:13px;line-height:1.6;margin:0;white-space:pre-wrap;">{esc(g['src_text'])}</p>
  </div>
</div>""")

    return f"""<!doctype html><html><head><meta charset="utf-8">
<title>切片覆盖对照 - {esc(doc_path.name)}</title></head>
<body style="font-family:-apple-system,'PingFang SC',sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;">
<h2 style="font-size:18px;">{esc(doc_path.name)} — 原文 / 切片 对照</h2>
<p style="color:#666;font-size:13px;">共 {chunk_count} 个 chunk，{len(pairs)} 段原文精确匹配，<span style="color:#8a6d1a;">{len(suspects)} 段疑似改写/需复核</span>，<span style="color:#a33;">{len(gaps)} 段未覆盖</span>（chunk text 要求逐字取自原文，精确匹配即真实覆盖；疑似改写和未覆盖都值得人工确认）。</p>
{''.join(rows)}
</body></html>"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("doc", help="Path to the source .md file")
    parser.add_argument("--chunks", help="Path to children.jsonl (default: auto-detect sibling _rag-chunks/*.jsonl)")
    parser.add_argument("-o", "--out", help="Output HTML path (default: <doc>.diff.html)")
    parser.add_argument("--threshold", type=float, default=0.1, help="Min Jaccard ratio for the SUSPECT tier (paragraphs that fail exact containment but still resemble a chunk enough to flag for review). Not a 0-1 'percent similar' scale; unrelated text scores near 0. Does not affect what counts as covered -- only exact containment does that now.")
    args = parser.parse_args()

    doc_path = Path(args.doc)
    text = strip_boilerplate(doc_path.read_text(encoding="utf-8"))
    blocks = split_paragraphs(text)

    chunks_path = Path(args.chunks) if args.chunks else find_chunks_file(doc_path)
    if not chunks_path or not chunks_path.exists():
        raise SystemExit(f"No chunks file found near {doc_path} — pass --chunks explicitly")
    chunks = load_matching_chunks(chunks_path, doc_path)
    if not chunks:
        raise SystemExit(f"No chunks in {chunks_path} reference source_path ending in {doc_path.name}")

    chunk_by_id = {c["chunk_id"]: c for c in chunks}
    pairs, suspects, gaps = [], [], []
    for b in blocks:
        cid, ratio, status = best_match(b["text"], chunks, args.threshold)
        if status == "exact":
            pairs.append({
                "heading": b["heading"], "chunk_id": cid, "ratio": ratio,
                "src_text": b["text"],
                "chunk_text": chunk_by_id[cid].get("text") or chunk_by_id[cid].get("answer", ""),
            })
        elif status == "fuzzy":
            suspects.append({
                "heading": b["heading"], "chunk_id": cid, "ratio": ratio,
                "src_text": b["text"],
                "chunk_text": chunk_by_id[cid].get("text") or chunk_by_id[cid].get("answer", ""),
            })
        else:
            gaps.append({"heading": b["heading"], "src_text": b["text"], "ratio": ratio})

    out_path = Path(args.out) if args.out else doc_path.with_suffix(".diff.html")
    out_path.write_text(render_html(doc_path, pairs, suspects, gaps, len(chunks)), encoding="utf-8")

    print(f"{doc_path.name}: {len(chunks)} chunks, {len(pairs)} paragraphs exactly matched, "
          f"{len(suspects)} suspect (fuzzy-only), {len(gaps)} gaps")
    for s in suspects:
        print(f"  SUSPECT: {s['heading']} — {s['src_text'][:60]}... (~{s['chunk_id']}, ratio {s['ratio']:.2f})")
    for g in gaps:
        print(f"  GAP: {g['heading']} — {g['src_text'][:60]}...")
    print(f"Report written to {out_path}")


if __name__ == "__main__":
    main()
