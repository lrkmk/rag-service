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
import json
from pathlib import Path

import markdown as md
from flask import Flask, jsonify, request, send_from_directory

import chunk_diff

REPO_ROOT = Path(__file__).resolve().parent.parent
ROOTS = ["帮助中心", "API文档"]

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
    pairs, gaps = [], []
    for b in blocks:
        cid, ratio = chunk_diff.best_match(b["text"], chunks, threshold)
        if cid:
            c = chunk_by_id[cid]
            pairs.append({
                "heading": b["heading"], "chunk_id": cid, "ratio": round(ratio, 3),
                "src_text": b["text"],
                "chunk_text": c.get("text") or c.get("answer", ""),
                "doc_type": c.get("doc_type") or c.get("rule_type"),
                "applicable_carrier": c.get("applicable_carrier"),
                "compares": c.get("compares"),
            })
        else:
            gaps.append({"heading": b["heading"], "src_text": b["text"], "ratio": round(ratio, 3)})

    return jsonify({
        "doc": rel_path,
        "chunk_count": len(chunks),
        "matched_count": len(pairs),
        "gap_count": len(gaps),
        "pairs": pairs,
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
    # Strip GitBook-specific {% hint %}...{% endhint %} blocks before
    # rendering — Python-Markdown doesn't know this syntax and would render
    # it as a literal paragraph of Liquid-template noise instead of the
    # "ask Eva" callout box it represents on the source site.
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
        for p in chunk_diff.load_jsonl(parents_path):
            if p.get("source_path", "").endswith(doc_path.name):
                parent = p
                break

    return jsonify({
        "doc": rel_path,
        "chunks_file": str(chunks_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "parent": parent,
        "chunks": chunks,
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5001)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=False)
