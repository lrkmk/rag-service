"""
Local browsing/QA tool for the chunking pipeline — NOT part of the
retrieval-only Docker service (see ../Dockerfile). Pick any source article
in the 帮助中心/API文档 tree, see it side-by-side with its produced chunks
(reusing chunk_diff.py's matching logic), or view the raw chunk JSONL.

Usage:
    python webapp.py [--port 5001]

Then open http://localhost:5001
"""

import argparse
import difflib
import json
import sys
from pathlib import Path

import markdown as md
from flask import Flask, jsonify, request, send_from_directory

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# chunk_diff.py lives in the sibling chunking/ directory, not here.
sys.path.insert(0, str(REPO_ROOT / "scripts" / "chunking"))
import chunk_diff  # noqa: E402

# crawl_gitbook.py — reused here for the same fetch_page_md() the diff-check
# CLI uses, so "看新旧文档差异" fetches live content the identical way
# instead of re-implementing GitBook's .md-export fetch a second time.
sys.path.insert(0, str(REPO_ROOT / "scripts" / "crawl"))
import crawl_gitbook  # noqa: E402

ROOTS = ["doc/帮助中心", "doc/API文档", "doc/产品介绍"]

app = Flask(__name__)


def build_tree(root: Path) -> dict:
    """Recursive {name, type, path, children} tree, .md files only,
    _rag-chunks output dirs excluded (they're an implementation detail,
    not something to browse as a 'document')."""
    node = {"name": root.name, "type": "dir", "path": str(root.relative_to(REPO_ROOT)).replace("\\", "/"), "children": []}
    entries = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name))
    for entry in entries:
        if entry.name == "_rag-chunks" or entry.name.startswith("."):
            continue
        if entry.is_dir():
            child = build_tree(entry)
            if child["children"]:
                node["children"].append(child)
        elif entry.suffix == ".md":
            node["children"].append({
                "name": entry.name,
                "type": "file",
                "path": str(entry.relative_to(REPO_ROOT)).replace("\\", "/"),
            })
    return node


@app.route("/")
def index():
    return send_from_directory(Path(__file__).parent / "webapp_static", "index.html")


@app.route("/api/tree")
def api_tree():
    trees = []
    for r in ROOTS:
        root_path = REPO_ROOT / r
        if root_path.exists():
            trees.append(build_tree(root_path))
    return jsonify(trees)


def _resolve_doc(rel_path: str) -> Path:
    doc_path = (REPO_ROOT / rel_path).resolve()
    if REPO_ROOT not in doc_path.parents or doc_path.suffix != ".md":
        raise ValueError("invalid path")
    return doc_path


@app.route("/api/diff")
def api_diff():
    rel_path = request.args.get("path", "")
    threshold = float(request.args.get("threshold", 0.1))
    try:
        doc_path = _resolve_doc(rel_path)
    except ValueError:
        return jsonify({"error": "invalid path"}), 400
    if not doc_path.exists():
        return jsonify({"error": "file not found"}), 404

    text = chunk_diff.strip_boilerplate(doc_path.read_text(encoding="utf-8"))
    blocks = chunk_diff.split_paragraphs(text)

    chunks_path = chunk_diff.find_chunks_file(doc_path)
    if not chunks_path:
        return jsonify({"error": "no _rag-chunks folder found next to this file"}), 404
    chunks = chunk_diff.load_matching_chunks(chunks_path, doc_path)
    if not chunks:
        return jsonify({"error": f"no chunks in {chunks_path.name} reference this file"}), 404

    chunk_by_id = {c.get("chunk_id"): c for c in chunks}
    pairs, suspects, gaps = [], [], []
    for b in blocks:
        cid, ratio, status = chunk_diff.best_match(b["text"], chunks, threshold)
        # best_match() already clean_markdown_text()s both sides internally
        # to DECIDE coverage, but that never made it into what's displayed —
        # src_text was the raw strip_boilerplate()-only paragraph, so even an
        # "exact" match could show two visually different texts (leftover
        # **bold**/&#x624D; entities on the source side that the chunk's
        # stored text never had, since the chunker cleaned it before
        # writing). Clean it the same way for display.
        display_text = chunk_diff.clean_markdown_text(b["text"])
        if status in ("exact", "fuzzy"):
            c = chunk_by_id[cid]
            entry = {
                "heading": b["heading"], "chunk_id": cid, "ratio": round(ratio, 3),
                "src_text": display_text,
                "chunk_text": c.get("text") or c.get("answer", ""),
                "doc_type": c.get("doc_type") or c.get("rule_type"),
                "applicable_carrier": c.get("applicable_carrier"),
                "compares": c.get("compares"),
            }
            (pairs if status == "exact" else suspects).append(entry)
        else:
            gaps.append({"heading": b["heading"], "src_text": display_text, "ratio": round(ratio, 3)})

    return jsonify({
        "doc": rel_path,
        "chunk_count": len(chunks),
        "matched_count": len(pairs),
        "suspect_count": len(suspects),
        "gap_count": len(gaps),
        "pairs": pairs,
        "suspects": suspects,
        "gaps": gaps,
    })


@app.route("/api/source")
def api_source():
    rel_path = request.args.get("path", "")
    try:
        doc_path = _resolve_doc(rel_path)
    except ValueError:
        return jsonify({"error": "invalid path"}), 400
    if not doc_path.exists():
        return jsonify({"error": "file not found"}), 404

    raw_text = doc_path.read_text(encoding="utf-8")
    # Strip GitBook wrapper tags before rendering while retaining visible hint
    # text; Python-Markdown does not understand Liquid-template syntax.
    cleaned = chunk_diff.strip_boilerplate(raw_text)
    html = md.markdown(cleaned, extensions=["extra", "sane_lists", "toc"])

    return jsonify({"doc": rel_path, "text": raw_text, "html": html, "line_count": len(raw_text.splitlines())})


@app.route("/api/raw")
def api_raw():
    rel_path = request.args.get("path", "")
    try:
        doc_path = _resolve_doc(rel_path)
    except ValueError:
        return jsonify({"error": "invalid path"}), 400
    if not doc_path.exists():
        return jsonify({"error": "file not found"}), 404

    chunks_path = chunk_diff.find_chunks_file(doc_path)
    if not chunks_path:
        return jsonify({"error": "no _rag-chunks folder found next to this file"}), 404
    chunks = chunk_diff.load_matching_chunks(chunks_path, doc_path)

    parent = None
    parents_path = chunks_path.parent / "parents.jsonl"
    if parents_path.exists() and parents_path != chunks_path:
        target_name = doc_path.name
        for p in chunk_diff.load_jsonl(parents_path):
            sp = p.get("source_path", "")
            # Path-segment-boundary match, not a raw substring -- see
            # chunk_diff.load_matching_chunks for the same fix and why a bare
            # endswith(filename) false-matches sibling files like 搜索.md /
            # 智能搜索.md.
            if sp == target_name or sp.endswith("/" + target_name):
                parent = p
                break

    return jsonify({
        "doc": rel_path,
        "chunks_file": str(chunks_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "parent": parent,
        "chunks": chunks,
    })


@app.route("/api/crawl-status")
def api_crawl_status():
    """Aggregated .crawl-status.json summaries across all corpora — lets the
    frontend badge which tree files have a pending line-check diff to review
    without a round-trip per file."""
    result = {}
    for r in ROOTS:
        manifest_path = REPO_ROOT / r / ".crawl-status.json"
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            result[r] = {
                "checked_at": manifest.get("checked_at"),
                "changed": [c["path"] for c in manifest.get("changed", [])],
                "new_count": len(manifest.get("new", [])),
            }
    return jsonify(result)


def _find_corpus_root(doc_path: Path) -> Path | None:
    """Walk up from doc_path to the corpus dir directly under doc/ (e.g.
    doc/API文档), which is where diff-check writes .crawl-status.json."""
    rel = doc_path.relative_to(REPO_ROOT)
    parts = rel.parts
    if len(parts) < 2 or parts[0] != "doc":
        return None
    return REPO_ROOT / parts[0] / parts[1]


@app.route("/api/crawl-diff")
def api_crawl_diff():
    """Git-diff-style comparison of a local doc against the live GitBook
    page, for files diff-check flagged as changed in .crawl-status.json.
    Reuses crawl_gitbook.fetch_page_md() so this fetches content the exact
    same way the CLI's diff-check does, rather than a second implementation
    that could drift out of sync with it."""
    rel_path = request.args.get("path", "")
    try:
        doc_path = _resolve_doc(rel_path)
    except ValueError:
        return jsonify({"error": "invalid path"}), 400
    if not doc_path.exists():
        return jsonify({"error": "file not found"}), 404

    corpus_root = _find_corpus_root(doc_path)
    if corpus_root is None:
        return jsonify({"error": "could not determine corpus for this path"}), 400

    manifest_path = corpus_root / ".crawl-status.json"
    if not manifest_path.exists():
        return jsonify({
            "doc": rel_path,
            "has_manifest": False,
            "message": "没有 .crawl-status.json，请先运行 crawl_gitbook.py diff-check",
        })

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rel_posix = str(doc_path.relative_to(REPO_ROOT)).replace("\\", "/")
    entry = next((c for c in manifest.get("changed", []) if c.get("path") == rel_posix), None)
    if entry is None:
        return jsonify({
            "doc": rel_path,
            "has_manifest": True,
            "checked_at": manifest.get("checked_at"),
            "flagged_changed": False,
            "message": "diff-check 未将此文件标记为 changed（未变化，或从未匹配到线上页面）",
        })

    url = entry["url"]
    try:
        fresh = crawl_gitbook.fetch_page_md(url)
    except Exception as e:
        return jsonify({"error": f"fetch failed: {e}"}), 502

    local = doc_path.read_text(encoding="utf-8")
    local_lines = local.splitlines()
    fresh_lines = fresh.splitlines()

    diff_lines = []
    sm = difflib.SequenceMatcher(None, local_lines, fresh_lines)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for line in local_lines[i1:i2]:
                diff_lines.append({"type": "equal", "text": line})
        else:
            for line in local_lines[i1:i2]:
                diff_lines.append({"type": "delete", "text": line})
            for line in fresh_lines[j1:j2]:
                diff_lines.append({"type": "insert", "text": line})

    return jsonify({
        "doc": rel_path,
        "has_manifest": True,
        "flagged_changed": True,
        "url": url,
        "checked_at": manifest.get("checked_at"),
        "applied": entry.get("applied", False),
        "diff_lines": diff_lines,
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5001)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=False)
