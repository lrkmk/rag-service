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
                actually changed since the local copy was made. Also cross-
                checks llms.txt for pages with no local title match at all
                (brand new pages, same detection `list` does). This is the
                incremental-update / content-drift check that was designed
                but never built earlier — see the "核价出票" case where the
                live site had been re-edited since the original crawl and
                nothing caught it.

                Writes doc/<corpus>/.crawl-status.json (new/changed/
                unchanged/unmatched, with paths) as a durable marker — the
                point is that a later chunking pass (or the doc-chunking
                skill) can read that file and only touch what's flagged
                `changed`/`new`, instead of re-chunking the whole corpus or
                re-deriving "what changed" from scratch each time. The
                marker only reflects the results of the diff-check run that
                wrote it — it goes stale the moment the live site changes
                again, it's not live state.

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

diff-check writes doc/<corpus>/.crawl-status.json (gitignored, point-in-time
only) — after running it, only re-chunk the paths under "changed" (via the
doc-chunking skill), not the whole corpus.
"""
import argparse
import glob
import json
import os
import re
import time
import urllib.request
from collections import Counter
from datetime import datetime, timezone

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
# {% hint %}...{% endhint %} blocks (the "Ask Eva" CTA at the top of every
# page, plus assorted inline warning/info notes) went through a site-wide
# EN->CN translation at some point — confirmed on 2 separate pages, both
# with byte-identical meaning before/after, just re-worded in Chinese
# instead of English. Comparing raw text made ~90% of API文档 look
# "changed" (107/124) purely from this, drowning out real drift like the
# getOfferPrice.do terminology rename found in the SAME diff-check run.
# Stripping all hint-block CONTENT (not just the Ask-Eva one) before
# comparing is a deliberate tradeoff: a hint whose actual informational
# content changes (not just language) would be missed by diff-check, but
# every case found so far has been translation-only noise, and the
# alternative (no stripping) makes the whole "changed" list too noisy to
# act on. Only used for the diff-check comparison — fetch/list still
# save/report the raw untouched page.
GITBOOK_TAG_RE = re.compile(r"\{%[^}]*%\}")


def normalize_for_diff(text: str) -> str:
    return GITBOOK_TAG_RE.sub("", text).strip()


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


def _category_of(path: str, corpus_dir: str) -> str:
    """Local file's top-level category folder relative to the corpus root
    (e.g. "04-API参考"), used to disambiguate same-titled pages below."""
    rel = os.path.relpath(path, corpus_dir)
    parts = rel.split(os.sep)
    return parts[0] if len(parts) > 1 else ""


def _url_top_segment(url: str, base_path: str) -> str:
    """First path segment of a page's URL after the corpus prefix (e.g.
    "product-guides" vs "api-reference"), used as a per-category signature."""
    path = url.split(f"{BASE}/", 1)[-1]
    if path.startswith(base_path + "/"):
        path = path[len(base_path) + 1:]
    return path.split("/")[0]


def cmd_diff_check(args):
    prefix = CORPUS_PREFIX[args.corpus]
    entries = parse_llms_txt(prefix)
    # Some titles are shared by two live pages -- most commonly a prose
    # product-guide page and its matching raw api-reference page for the
    # same endpoint/topic (e.g. "创建订单" exists once under
    # product-guides/... and once under api-reference/...). A plain
    # title->url dict silently drops one of them, which then makes BOTH
    # local files (living in different category folders) get diffed
    # against the SAME url -- i.e. exactly the bug this was rewritten to
    # avoid. Keep every candidate URL per title instead.
    by_title: dict[str, list[str]] = {}
    for title, url, _ in entries:
        by_title.setdefault(title, []).append(url)

    corpus_dir = os.path.join(DOC_ROOT, args.corpus)
    local_files = [
        p for p in glob.glob(os.path.join(corpus_dir, "**", "*.md"), recursive=True)
        if "_rag-chunks" not in p
    ]
    local_titles = {p: title_of_local_file(p) for p in local_files}

    # Learn each local category folder's typical URL top-segment from the
    # files whose title is NOT ambiguous (only one candidate URL) -- e.g.
    # most files under 03-产品指南 resolve unambiguously to a
    # "product-guides/..." URL, so that folder's signature is
    # "product-guides". Used below to pick the right candidate when a
    # title has more than one URL match.
    category_votes: dict[str, "Counter[str]"] = {}
    for path, title in local_titles.items():
        candidates = by_title.get(title) or []
        if len(candidates) != 1:
            continue
        cat = _category_of(path, corpus_dir)
        category_votes.setdefault(cat, Counter())[_url_top_segment(candidates[0], prefix)] += 1
    category_signature = {cat: votes.most_common(1)[0][0] for cat, votes in category_votes.items() if votes}

    changed, unmatched, unchanged = [], [], []
    matched_titles = set()
    for path in local_files:
        title = local_titles[path]
        candidates = by_title.get(title) if title else None
        if not title or not candidates:
            unmatched.append(path)
            continue
        if len(candidates) == 1:
            url = candidates[0]
        else:
            cat = _category_of(path, corpus_dir)
            expected = category_signature.get(cat)
            filtered = [u for u in candidates if _url_top_segment(u, prefix) == expected] if expected else []
            if len(filtered) != 1:
                unmatched.append(
                    f"{path} (ambiguous title '{title}' matches {len(candidates)} live pages, "
                    f"could not disambiguate by folder -- check manually)"
                )
                continue
            url = filtered[0]
        matched_titles.add(title)
        try:
            fresh = fetch_page_md(url)
        except Exception as e:
            unmatched.append(f"{path} (fetch error: {e})")
            continue
        local = open(path, encoding="utf-8").read()
        if normalize_for_diff(fresh) != normalize_for_diff(local):
            changed.append((path, url, fresh))
        else:
            unchanged.append(path)
        time.sleep(0.2)

    # Pages in llms.txt with no local file at all — same detection `list`
    # does, folded in here so diff-check gives one complete picture instead
    # of needing a separate `list` run to catch brand-new pages.
    new_pages = [(title, url) for title, url, _ in entries if title not in matched_titles]

    print(f"Checked {len(local_files)} local files under {args.corpus}/")
    print(f"  unchanged: {len(unchanged)}")
    print(f"  changed:   {len(changed)}")
    print(f"  new (no local file, found in llms.txt): {len(new_pages)}")
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

    if new_pages:
        print("\nNew pages (not crawled yet — decide where they belong, then `fetch` + doc-chunking skill):")
        for title, url in new_pages:
            print(f"  {title}\n    {url}")

    if unmatched:
        print("\nUnmatched (couldn't confirm via title match, check manually):")
        for u in unmatched[:20]:
            print(f"  {u}")

    manifest_path = os.path.join(corpus_dir, ".crawl-status.json")
    manifest = {
        "corpus": args.corpus,
        "checked_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "new": [{"title": title, "url": url} for title, url in new_pages],
        "changed": [
            {"path": os.path.relpath(path, REPO_ROOT).replace("\\", "/"), "url": url, "applied": bool(args.apply)}
            for path, url, _ in changed
        ],
        "unchanged": [os.path.relpath(p, REPO_ROOT).replace("\\", "/") for p in unchanged],
        "unmatched": [str(u) for u in unmatched],
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"\nMarker written -> {os.path.relpath(manifest_path, REPO_ROOT)}")
    print("Next: re-chunk only the paths listed under \"changed\" (and any \"new\" ones you've fetched+placed), via the doc-chunking skill — not the whole corpus.")


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
