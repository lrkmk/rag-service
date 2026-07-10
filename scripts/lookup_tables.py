"""
Query interface for the 17 structured lookup tables that are deliberately
NOT ingested into Chroma (see RAG-切片设计总览.md and each ingest script's
docstring for why: they're exact-lookup data — error codes, time limits,
test data — not semantic-search content, and chunking them would destroy
their queryability as a table).

Until now these just sat as static JSON files with no programmatic access
from an agent — this module is what mcp_server.py's list_lookup_tables/
query_lookup_table tools are built on.

Three different JSON shapes exist across the files (found by inspection,
not assumed):
  1. Flat list of flat dicts:      [{...}, {...}]
  2. Wrapped under "entries":      {"field": ..., "endpoint": ..., "entries": [...]}
  3. Wrapped under "rows":         {"source_path": ..., "rows": [...]}
_normalize() detects and flattens all three into a uniform (rows, meta) pair.
"""

import glob
import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HELP_CENTER = os.path.join(REPO_ROOT, "doc", "帮助中心")
API_DOCS = os.path.join(REPO_ROOT, "doc", "API文档")

_ROW_KEYS = ("entries", "rows")


def _normalize(raw):
    """Returns (rows: list[dict], meta: dict) regardless of which of the
    three shapes `raw` was in. meta holds whatever non-row wrapper fields
    existed (field/endpoint/source_path/ref/etc.), empty for shape 1."""
    if isinstance(raw, list):
        return raw, {}
    if isinstance(raw, dict):
        for key in _ROW_KEYS:
            if key in raw and isinstance(raw[key], list):
                meta = {k: v for k, v in raw.items() if k != key}
                return raw[key], meta
    return [], {}


def discover_tables() -> dict:
    """table_name -> {path, rows, meta, columns}. Scanned fresh on every
    call — these files are small (max ~130 rows) and change rarely, so
    there's no real cost to skip caching and the complexity that comes with
    keeping a cache correct across re-ingests."""
    paths = []
    for root in (HELP_CENTER, API_DOCS):
        paths += glob.glob(os.path.join(root, "**", "_rag-chunks", "*.json"), recursive=True)

    tables = {}
    for p in paths:
        name = os.path.splitext(os.path.basename(p))[0]
        with open(p, encoding="utf-8-sig") as f:
            raw = json.load(f)
        rows, meta = _normalize(raw)
        if not rows:
            continue  # not actually a row-shaped table, skip silently
        columns = sorted({k for row in rows for k in row.keys()})
        tables[name] = {
            "path": os.path.relpath(p, REPO_ROOT).replace("\\", "/"),
            "rows": rows,
            "meta": meta,
            "columns": columns,
        }
    return tables


def list_tables() -> list[dict]:
    tables = discover_tables()
    return [
        {
            "table_name": name,
            "path": t["path"],
            "row_count": len(t["rows"]),
            "columns": t["columns"],
            "meta": t["meta"],
        }
        for name, t in sorted(tables.items())
    ]


def _char_overlap(a: str, b: str) -> float:
    """Bigram Jaccard, not substring containment — a query like '错误码表'
    should still surface '错误码速查表' even though '错误码表' isn't a
    contiguous substring of it ('速查' sits in between)."""
    def bigrams(s):
        return {s[i : i + 2] for i in range(len(s) - 1)} or {s}
    ba, bb = bigrams(a.lower()), bigrams(b.lower())
    return len(ba & bb) / len(ba | bb) if (ba or bb) else 0.0


def query_table(table_name: str, filters: dict | None = None, limit: int = 50) -> dict:
    tables = discover_tables()
    if table_name not in tables:
        close = sorted(tables, key=lambda n: -_char_overlap(table_name, n))
        close = [n for n in close if _char_overlap(table_name, n) > 0.15]
        return {"error": f"no table named '{table_name}'", "did_you_mean": close[:5]}

    t = tables[table_name]
    rows = t["rows"]
    if filters:
        def _match(row):
            for k, v in filters.items():
                cell = row.get(k)
                if cell is None:
                    return False
                # Case-insensitive substring match on strings (carrier codes,
                # error codes etc. are queried inconsistently cased in
                # practice); exact match for non-strings.
                if isinstance(cell, str) and isinstance(v, str):
                    if v.lower() not in cell.lower():
                        return False
                elif cell != v:
                    return False
            return True
        rows = [r for r in rows if _match(r)]

    truncated = len(rows) > limit
    return {
        "table_name": table_name,
        "meta": t["meta"],
        "total_matched": len(rows),
        "rows": rows[:limit],
        "truncated": truncated,
    }
