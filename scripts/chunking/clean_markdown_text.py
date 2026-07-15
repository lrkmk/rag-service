"""
Standalone CLI wrapping the same markdown-stripping logic duplicated across
the 6 chunk_*.py scripts (clean_markdown_text() + strip_boilerplate()) --
for manual (no-script) chunking of 帮助中心规则单元 / API文档A类概念说明,
where an agent hand-copies verbatim text into JSON and needs to strip the
same inline noise (**bold**, `code`, [links](), headers, GitBook tags) a
script would have stripped automatically.

Not imported by the chunk_*.py scripts -- this is a CLI-only tool, kept
separate to match this codebase's convention of standalone, independently
runnable chunking scripts (no shared utils module between them). If the
logic here and the 6 scripts' copies drift, treat the scripts as
authoritative and update this file to match, not the other way around.

Usage:
    python scripts/chunking/clean_markdown_text.py "**问题：**这是*示例*文本"
    echo "..." | python scripts/chunking/clean_markdown_text.py
"""
import html
import re
import sys


def strip_boilerplate(text: str) -> str:
    text = re.sub(r"\{% hint.*?%\}.*?\{% endhint %\}", "", text, flags=re.DOTALL)
    text = re.sub(r"\{%[^}]*%\}", "", text)
    text = re.sub(r"<a href.*?</a>", "", text)
    return text


def clean_markdown_text(text: str) -> str:
    text = html.unescape(text)  # decode &#x624D; / &#x41; etc
    text = re.sub(r"\\\n", "\n", text)  # hard line break
    text = re.sub(r"\\([*_`\[\]()#>\\])", r"\1", text)  # un-escape markdown escapes FIRST -- GitBook exports widely escape ** and ` inside blockquotes (e.g. "\*\*Dependency:\*\*"), which otherwise survive every regex below untouched since they no longer look like real markdown syntax
    text = re.sub(r"\{%[^}]*%\}", "", text)  # stray GitBook component tags
    text = re.sub(r"(?m)^```\w*\s*$", "", text)  # fenced-code-block delimiters
    text = re.sub(r"(?m)^[ \t]*(?:\*[ \t]*){3,}$", "", text)  # *** horizontal rule
    text = re.sub(r"(?m)^[ \t]*(?:-[ \t]*){3,}$", "", text)   # --- horizontal rule
    text = re.sub(r"(?m)^[ \t]*(?:_[ \t]*){3,}$", "", text)   # ___ horizontal rule
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)    # [text](url) / ![alt](url)
    text = re.sub(r"<(https?://[^>\s]+)>", r"\1", text)
    text = re.sub(r"\*\*((?:[^*\n]|\\\*)+)\*\*", r"\1", text)
    text = re.sub(r"__([^_\n]+)__", r"\1", text)
    text = re.sub(r"(?<!\w)\*((?:[^*\n]|\\\*)+)\*(?!\w)", r"\1", text)
    text = re.sub(r"(?<!\w)_([^_\n]+)_(?!\w)", r"\1", text)
    text = re.sub(r"`([^`\n]+)`", r"\1", text)
    text = re.sub(r"(?m)^(?:>\s?)*#{1,6}\s+", "", text)  # "### h" and repeated-blockquoted "> > ### h"
    text = re.sub(r"(?m)^(?:>\s?)+", "", text)  # strip one or more leading blockquote markers
    return text


def main():
    if len(sys.argv) > 1:
        raw = " ".join(sys.argv[1:])
    else:
        raw = sys.stdin.read()
    print(clean_markdown_text(strip_boilerplate(raw)))


if __name__ == "__main__":
    main()
