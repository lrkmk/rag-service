"""One-off verification script: fresh-crawl all 3 corpora into docbak/,
using the raw URL path structure (not the curated doc/ category layout),
to sanity-check crawl_gitbook.py's current correctness (title matching,
duplicate-title handling, fetch_page_md) against a clean slate. Not part
of the normal crawl/chunk/ingest pipeline -- delete after inspecting.
"""
import os
import time

import crawl_gitbook as cg

REPO_ROOT = cg.REPO_ROOT
OUT_ROOT = os.path.join(REPO_ROOT, "docbak")


def main():
    for corpus, prefix in cg.CORPUS_PREFIX.items():
        entries = cg.parse_llms_txt(prefix)
        print(f"{corpus}: {len(entries)} pages")
        for title, url, desc in entries:
            rel = url.split(f"{cg.BASE}/{prefix}/", 1)[-1]
            if not rel.endswith(".md"):
                rel += ".md"
            out_path = os.path.join(OUT_ROOT, corpus, rel)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            try:
                text = cg.fetch_page_md(url)
            except Exception as e:
                print(f"  FAILED {url}: {e}")
                continue
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text)
            time.sleep(0.15)
        print(f"{corpus}: done")


if __name__ == "__main__":
    main()
