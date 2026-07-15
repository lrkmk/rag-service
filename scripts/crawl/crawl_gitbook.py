"""
Reusable GitBook crawler for resources.atriptech.com — replaces the ad-hoc
curl/WebFetch commands used to build 帮助中心/API文档/产品介绍 (none of
which were ever checked in as a script, see git history).

Built on two GitBook site features:
  - https://resources.atriptech.com/llms.txt — a full site index (title,
    url, one-line description per page), covering all three corpora in one
    file.
  - Appending ".md" to any page URL returns clean raw markdown directly, no
    HTML parsing needed.

Three subcommands:
  list        — print (title, url) pairs from llms.txt for one corpus, to
                find pages that don't have a local file yet.
  fetch       — fetch one URL's raw markdown and save it.
  diff-check  — for every existing local .md file under a corpus, find its
                likely current URL by matching titles against llms.txt,
                fetch fresh content, and report which files' content has
                actually changed since the local copy was made. This is the
                incremental-update / content-drift check that was designed
                but never built earlier — see the "核价出票" case where the
                live site had been re-edited since the original crawl and
                nothing caught it.

Does NOT attempt to auto-assign new pages into the numbered category
folders (01-ATRIP, 04-售后票务, etc.) — that assignment is a judgment call
about where a topic belongs, not something derivable from the URL slug
(GitBook URLs are pinyin transliterations, not category paths). `list`
surfaces new pages for a human/agent to read and place manually, same as
the original crawls did.

Usage:
    python crawl_gitbook.py list 帮助中心
    python crawl_gitbook.py list API文档
    python crawl_gitbook.py list 产品介绍
    python crawl_gitbook.py fetch <url> <output_path>
    python crawl_gitbook.py diff-check 帮助中心
    python crawl_gitbook.py diff-check API文档 --apply   # overwrite changed files in place
"""
import argparse
import glob
import os
import re
import time
import urllib.request

BASE = "https://resources.atriptech.com"
LLMS_TXT_URL = f"{BASE}/llms.txt"

CORPUS_PREFIX = {
    "帮助中心": "bang-zhu-zhong-xin",
    "API文档": "api-wen-dang",
    "产品介绍": "chan-pin-jie-shao",
}

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC_ROOT = os.path.join(REPO_ROOT, "doc")

LEADING_REF_RE = re.compile(r"^>\s*For the complete documentation index.*?\n+", re.DOTALL)
LLMS_LINE_RE = re.compile(r"^-\s*\[(.+?)\]\((https?://\S+?)\)(?::\s*(.*))?$")


def _fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8")


def fetch_page_md(url: str) -> str:
    """Fetch one page's raw markdown (appends .md if not already present),
    stripping the leading llms.txt/markdown-export reference line."""
    md_url = url if url.endswith(".md") else url + ".md"
    text = _fetch(md_url)
    text = LEADING_REF_RE.sub("", text, count=1).lstrip("\n")
    return text


def parse_llms_txt(prefix: str) -> list[tuple[str, str, str]]:
    """Returns [(title, url, description), ...] for entries whose URL path
    starts with the given corpus prefix (e.g. "bang-zhu-zhong-xin")."""
    text = _fetch(LLMS_TXT_URL)
    entries = []
    for line in text.splitlines():
        m = LLMS_LINE_RE.match(line.strip())
        if not m:
            continue
        title, url, desc = m.group(1), m.group(2), m.group(3) or ""
        path = url.split(BASE, 1)[-1].lstrip("/")
        if path.startswith(prefix):
            entries.append((title, url, desc))
    return entries


def title_of_local_file(path: str) -> str | None:
    text = open(path, encoding="utf-8").read()
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def cmd_list(args):
    prefix = CORPUS_PREFIX[args.corpus]
    entries = parse_llms_txt(prefix)
    print(f"{len(entries)} pages found under {prefix}/\n")
    for title, url, desc in entries:
        suffix = f" — {desc}" if desc else ""
        print(f"  {title}{suffix}\n    {url}")


def cmd_fetch(args):
    text = fetch_page_md(args.url)
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved -> {args.output} ({len(text)} chars)")


def cmd_diff_check(args):
    prefix = CORPUS_PREFIX[args.corpus]
    entries = parse_llms_txt(prefix)
    by_title = {title: url for title, url, _ in entries}

    corpus_dir = os.path.join(DOC_ROOT, args.corpus)
    local_files = [
        p for p in glob.glob(os.path.join(corpus_dir, "**", "*.md"), recursive=True)
        if "_rag-chunks" not in p
    ]

    changed, unmatched, unchanged = [], [], []
    for path in local_files:
        title = title_of_local_file(path)
        if not title or title not in by_title:
            unmatched.append(path)
            continue
        url = by_title[title]
        try:
            fresh = fetch_page_md(url)
        except Exception as e:
            unmatched.append(f"{path} (fetch error: {e})")
            continue
        local = open(path, encoding="utf-8").read()
        if fresh.strip() != local.strip():
            changed.append((path, url, fresh))
        else:
            unchanged.append(path)
        time.sleep(0.2)

    print(f"Checked {len(local_files)} local files under {args.corpus}/")
    print(f"  unchanged: {len(unchanged)}")
    print(f"  changed:   {len(changed)}")
    print(f"  unmatched (no title match in llms.txt, or fetch failed): {len(unmatched)}")

    if changed:
        print("\nChanged pages (content differs from live site):")
        for path, url, fresh in changed:
            rel = os.path.relpath(path, REPO_ROOT)
            print(f"  {rel}\n    {url}")
            if args.apply:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(fresh)
                print("    -> overwritten with fresh content (re-chunk + re-ingest this file next)")

    if unmatched:
        print("\nUnmatched (couldn't confirm via title match, check manually):")
        for u in unmatched[:20]:
            print(f"  {u}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="List pages for a corpus from llms.txt")
    p_list.add_argument("corpus", choices=list(CORPUS_PREFIX.keys()))
    p_list.set_defaults(func=cmd_list)

    p_fetch = sub.add_parser("fetch", help="Fetch one page's raw markdown")
    p_fetch.add_argument("url")
    p_fetch.add_argument("output")
    p_fetch.set_defaults(func=cmd_fetch)

    p_diff = sub.add_parser("diff-check", help="Check existing local files against the live site for content drift")
    p_diff.add_argument("corpus", choices=list(CORPUS_PREFIX.keys()))
    p_diff.add_argument("--apply", action="store_true", help="Overwrite changed local files with fresh content (does NOT re-chunk/re-ingest)")
    p_diff.set_defaults(func=cmd_diff_check)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
