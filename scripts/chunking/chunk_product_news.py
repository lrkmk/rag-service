"""
Chunk Atlas资讯 (product news/announcements under doc/产品介绍/Atlas资讯/) into
RAG chunks — one chunk per article.

Unlike 帮助中心/API文档's rule content, these are time-stamped announcements,
not evergreen rules: the same airline/topic can get MULTIPLE posts over time
where a later one supersedes an earlier one's conclusion (e.g. "精神航空停运"
followed months later by "精神航空已恢复"). A rule engine has no way to know
this from text alone, so each chunk carries:

  - entity_tags: IATA-style codes found in parens in the title (e.g. "NK"
    from "精神航空（NK）"), used at query time to group posts about the same
    subject and keep only the most recent. Also scans body bullet lines
    matching "名称（CODE[、CODE...]）" (added 2026-07-17 -- confirmed for
    real: "中东地区运营更新-部分航司临时下线通知.md" names its affected
    carriers only in a body bullet ("Air Arabia（G9、E5、3L）"), never in
    the title, so title-only extraction gave it entity_tags: [] and this
    dedup-by-entity mechanism silently couldn't fire for it). Deliberately
    NOT a blanket body scan -- tested one first and it false-positived on
    airport codes in prose ("...机场（SAW）"), metric abbreviations in
    bullets ("航班准点率（OTP）达 87%" -- paren isn't at the end of the
    bullet, that's excluded), and, worse, an EXCLUSION list ("暂不包含
    9C、FR、U2" -- tagging FR here would make this article wrongly outrank
    the actual Ryanair launch announcement in the dedup-by-recency logic
    below, since recency comparison doesn't know "excluded from X" isn't
    "about X"). So: only bullet lines, skip ones containing a negation word
    (暂不包含/不包含/除外/排除/暂无法/不含/不支持), and only take the paren
    group if it's at the end of a short line (a name, not a sentence with
    unrelated content trailing it) or contains 2+ comma/dun/slash-separated
    codes together (unambiguously a carrier list either way).
  - recency_rank: position in the site's own Atlas资讯 listing (1 = newest).
    The site does not expose a reliable per-page timestamp via crawlable
    means (no visible "last updated" in the .md export; the rendered page's
    Next.js payload embeds updatedAt values but not attributably per-page
    without deeper framework-specific parsing; the page and section rss.xml
    endpoints returned no items). The listing itself is maintained in
    reverse-chronological order (confirmed against the dated entries mixed
    into it), so ordinal rank is used as the recency signal instead of a
    real timestamp.

Section-splitting (added 2026-07-17): about half the corpus (15/33 files as
of this writing) is NOT single-topic despite the assumption this script
started with -- longer announcements (e.g. a major feature/plan launch)
bundle several distinct sub-topics under GitBook's own
`### <mark style="color:...">sub-heading</mark>` convention (heading level
varies per file -- some use ##, some ###, a few #### -- but is consistent
*within* one file). Left as one chunk, a query about just one sub-topic
(e.g. "Starter 套餐多少钱一个月") gets an embedding that represents the
whole multi-topic announcement and doesn't rank the pricing sentence
buried in it -- confirmed for real: the "$69/月" detail in "舆途科技（Atlas）
正式开放给新一代Travel Seller.md" (four distinct sub-topics: 套餐上线定价 /
注册即用 / ATRIP首页升级 / 自助UAT测试, plus a before/after table and a
4-step activation section) never surfaced for pricing-shaped queries while
it was one 165-line chunk.

Detection: find the heading level(s) that wrap a `<mark>` tag in that
file's body, take the shallowest one (a file mixing levels means the
shallow one is the true section break, deeper mark-wrapped headings inside
it are sub-points of that section, not separate topics), and split there.
Files with 0 or 1 such heading stay a single chunk exactly as before --
this is deliberately not "split everything by heading", since a short
single-topic post's conclusion still shouldn't be cut from its lead-in.
Each resulting section chunk's `text` is prefixed with the parent
announcement's title (same topic-anchoring fix used for the webhook field
chunks) so a section chunk about pricing still carries "this is from the
Travel Seller launch announcement" context rather than reading as an
orphaned fragment.

Usage:
    python chunk_product_news.py  # processes the whole Atlas资讯/ folder
"""
import argparse
import glob
import hashlib
import html
import json
import os
import re

ENTITY_GROUP_RE = re.compile(r"[（(]([^（）()]{1,20})[）)]")
ENTITY_SPLIT_RE = re.compile(r"[、,，/]")
ENTITY_BULLET_RE = re.compile(r"^\s*[*\-]\s+(.*)$", re.MULTILINE)
ENTITY_NEGATION_RE = re.compile(r"暂不包含|不包含|除外|排除|暂无法|不含|不支持")
HEADER_RE = re.compile(r"^(#{1,6})[ \t]+(.+)$", re.MULTILINE)
MARK_INNER_RE = re.compile(r"<mark[^>]*>(.*?)</mark>", re.DOTALL)


def strip_boilerplate(text: str) -> str:
    text = re.sub(r"\{% hint.*?%\}", "", text)
    text = re.sub(r"\{% endhint %\}", "", text)
    # Strip GitBook wrapper tags and retain the visible content they enclose.
    text = re.sub(r"\{%[^}]*%\}", "", text)
    text = re.sub(r"&#x20;", " ", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_markdown_text(text: str) -> str:
    """Strip inline markdown formatting markers from otherwise-real prose,
    keeping the underlying text -- see chunk_disambiguation.py's function of
    the same name for the full rationale. Safe to apply directly here (no
    reordering needed unlike chunk_disambiguation.py/chunk_product_intro.py):
    this script never collapses single/double newlines to spaces before
    calling it, so the bold/italic regexes' single-line scoping is never
    defeated by an earlier newline-collapse step."""
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


def _codes_in_group(group_text: str) -> list[str]:
    parts = [p.strip() for p in ENTITY_SPLIT_RE.split(group_text)]
    return [p.upper() for p in parts if re.fullmatch(r"[A-Za-z0-9]{1,4}", p)]


def extract_entities(title: str, raw_body: str = "") -> list[str]:
    seen = []

    def add_all(codes):
        for code in codes:
            if code not in seen:
                seen.append(code)

    for g in ENTITY_GROUP_RE.finditer(title):
        add_all(_codes_in_group(g.group(1)))

    for m in ENTITY_BULLET_RE.finditer(raw_body):
        line = m.group(1)
        if ENTITY_NEGATION_RE.search(line):
            continue
        # strip markdown emphasis markers before the end-of-line check -- a
        # bolded bullet like "**Fly Jinnah（9P）**" has "**" trailing the
        # closing paren, which would otherwise defeat the anchor below
        stripped_line = re.sub(r"[*_`]", "", line).strip()
        end_m = re.search(r"[（(]([^（）()]{1,20})[）)]\s*$", stripped_line)
        if end_m:
            add_all(_codes_in_group(end_m.group(1)))
            continue
        # not at the end of the bullet -- only trust it if it's unambiguously
        # a carrier list (2+ codes together), not a single stray match buried
        # in an unrelated sentence (e.g. "航班准点率（OTP）达 87%")
        for g in ENTITY_GROUP_RE.finditer(line):
            codes = _codes_in_group(g.group(1))
            if len(codes) >= 2:
                add_all(codes)

    return seen


def split_into_sections(raw_body: str):
    """Split a boilerplate-stripped-but-not-yet-markdown-cleaned article body
    into (section_title, section_body) pairs at whichever heading level
    wraps a <mark> tag in THIS file (varies per file -- see module
    docstring). Must run before clean_markdown_text, which would otherwise
    strip the very # and <mark> markers this looks for.

    Returns None if there are fewer than 2 mark-wrapped headings -- callers
    should fall back to treating the whole body as a single chunk, same as
    before this function existed.
    """
    mark_levels = set()
    for m in HEADER_RE.finditer(raw_body):
        if "<mark" in m.group(2):
            mark_levels.add(len(m.group(1)))
    if not mark_levels:
        return None
    split_level = min(mark_levels)
    pattern = re.compile(rf"^#{{{split_level}}}[ \t]+(.+)$", re.MULTILINE)
    matches = list(pattern.finditer(raw_body))
    if len(matches) < 2:
        return None

    sections = []
    intro = raw_body[: matches[0].start()].strip()
    if intro:
        sections.append(("概述", intro))
    for i, m in enumerate(matches):
        heading_text = MARK_INNER_RE.sub(r"\1", m.group(1))
        section_title = clean_markdown_text(heading_text).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw_body)
        section_body = raw_body[start:end].strip()
        if section_body:
            sections.append((section_title, section_body))
    return sections if len(sections) >= 2 else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--news-dir",
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "doc", "产品介绍", "Atlas资讯"),
    )
    args = parser.parse_args()

    files = [f for f in glob.glob(os.path.join(args.news_dir, "*.md")) if not f.endswith("Atlas资讯.md")]
    # Reverse-chronological listing order is not recoverable from the filesystem
    # (crawl wrote files in the order they were fetched, which matched the
    # site's own listing order at crawl time) — os.listdir doesn't preserve
    # that, so rank comes from ORDER below, captured at crawl time from
    # llms.txt and hand-kept in this list. Any article added later that
    # isn't in ORDER falls back to being treated as rank 1 (newest), which is
    # the safe assumption for anything freshly added.
    ORDER = [
        "舆途科技（Atlas）核价出票接口上线.md",
        "舆途科技（Atlas）正式开放给新一代Travel Seller.md",
        "泰国亚洲航空（FD）超售政策更新.md",
        "舆途科技（Atlas）废票 API 正式上线.md",
        "舆途科技（Atlas）选座 API 上线.md",
        "AJet 航空（VF）API 已正式上线.md",
        "维兹航空（Wizz Air）API 直连正式上线舆途科技（Atlas）.md",
        "三家航司即将上线：维兹、AJet、越洋.md",
        "精神航空(NK)停运及退款处理说明.md",
        "ATRIP 全新上线-履约能力与售后服务全景可视化.md",
        "中东地区运营更新-部分航司临时下线通知.md",
        "中东地区运营调整通知（客户通告）.md",
        "重磅升级-舆途科技（Atlas）×亚洲航空（AirAsia）API升级完成.md",
        "爱琴海航空(A3)与奥林匹克航空(OA)服务升级.md",
        "FlyOne Asia（7Q）现已正式接入 Atlas.md",
        "精神航空(NK)航班数据与售后服务已恢复.md",
        "精神航空(NK)产品临时下架公告.md",
        "EVA 智能客服上线-舆途科技（Atlas）用 AI 重塑服务新体验.md",
        "航司上新-九元航空（AQ）正式接入 Atlas.md",
        "春秋航空日本（IJ）超售政策通知.md",
        "VU上线-PNR Claim 功能解锁行李加购新路径.md",
        "新玩法-行程信息直查二次行李价格.md",
        "Ryanair航班现已上线Atlas API.md",
        "新增废票附件上传功能.md",
        "API 文档中心升级.md",
        "HB工单客服机器人上线.md",
        "Seat Selection API 上线.md",
        "N0上线-搜索与订单服务双优化.md",
        "新航司JA上线+首页焕新.md",
        "日韩廉航退票那些坑.md",
        "票价套餐及代金券退款.md",
        "VCC 透传支付介绍与提示.md",
        "Atlas与Ryanair达成战略合作.md",
    ]
    rank_of = {name: i + 1 for i, name in enumerate(ORDER)}

    chunks = []
    split_count = 0
    for fpath in files:
        fname = os.path.basename(fpath)
        text = strip_boilerplate(open(fpath, encoding="utf-8").read())
        title_m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = clean_markdown_text(title_m.group(1).strip() if title_m else fname[:-3])
        raw_body = text[title_m.end():].strip() if title_m else text
        # maxsplit=1, take [1] not [-1] — see chunk_product_intro.py for why:
        # split(marker) with no limit cuts at every occurrence of "产品介绍",
        # and a title containing that substring would shift where [-1] cuts.
        source_path = fpath.split("产品介绍", 1)[1].lstrip("\\/").replace("\\", "/")
        source_path = "产品介绍/" + source_path
        # ASCII-stripped title alone isn't unique: two Spirit Airlines posts
        # both reduce to "spiritairlinesnk", and several all-Chinese titles
        # (e.g. "日韩廉航退票那些坑") reduce to "" — same class of bug fixed
        # in chunk_disambiguation.py before, recurring here since this
        # script started from a copy of that pattern. Path hash guarantees
        # uniqueness regardless of title content.
        ascii_hint = re.sub(r"[^a-zA-Z0-9]+", "", title.lower())[:16]
        path_hash = hashlib.md5(fpath.encode("utf-8")).hexdigest()[:8]
        base_chunk_id = f"news-{ascii_hint}{path_hash}" if ascii_hint else f"news-{path_hash}"
        entity_tags = extract_entities(title, raw_body)

        sections = split_into_sections(raw_body)
        if sections is None:
            body = clean_markdown_text(raw_body)
            chunks.append({
                "chunk_id": base_chunk_id,
                "doc_type": "资讯",
                "level1_category": "产品介绍",
                "level2_category": "Atlas资讯",
                "title": title,
                "entity_tags": entity_tags,
                "recency_rank": rank_of.get(fname, 1),
                "source_path": source_path,
                "text": f"{title}。{body}",
            })
        else:
            split_count += 1
            for i, (section_title, section_raw) in enumerate(sections, 1):
                section_body = clean_markdown_text(section_raw)
                chunks.append({
                    "chunk_id": f"{base_chunk_id}-s{i}",
                    "doc_type": "资讯",
                    "level1_category": "产品介绍",
                    "level2_category": "Atlas资讯",
                    "title": title,
                    "section": section_title,
                    "entity_tags": entity_tags,
                    "recency_rank": rank_of.get(fname, 1),
                    "source_path": source_path,
                    "text": f"{title}：{section_title}。{section_body}",
                })

    out_dir = os.path.join(args.news_dir, "_rag-chunks")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "children.jsonl")
    with open(out_file, "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    print(f"{len(chunks)} news chunks ({split_count} article(s) section-split) -> {out_file}")
    unranked = [os.path.basename(f) for f in files if os.path.basename(f) not in rank_of]
    if unranked:
        print(f"WARNING: {len(unranked)} file(s) not in ORDER, defaulted to rank 1: {unranked}")


if __name__ == "__main__":
    main()
