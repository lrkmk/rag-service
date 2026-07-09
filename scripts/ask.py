"""
CLI tool: run natural-language questions against the Chroma store.

One-shot mode (starts a fresh process each time, model reloads every call):
    python ask.py "退票超过多久Atlas就不再处理了"
    python ask.py "航班提前多久可以非自愿退票" --carrier FR
    python ask.py "出票要多长时间" --faq-only
    python ask.py "婴儿票怎么加购" -n 5

Interactive mode (model loads once, then keeps prompting — use this if
you're asking more than one question in a row):
    python ask.py
    > 退票要多久
    ... results ...
    > 航班提前多久可以非自愿退票 --carrier FR
    ... results ...
    > exit

In interactive mode you can append the same flags (--carrier/-n/--faq-only/
--rules-only) after your question on the same line; they're parsed per line.

Pass --carrier to pre-filter rule chunks by applicable_carrier before
ranking (use this whenever the question names a specific airline code — it
avoids getting drowned out by generic rules, per the "精确匹配航司再
fallback 通用" principle from the chunking design).
"""

import argparse
import shlex
import sys

from rag_search import search_faq, search_rules


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ask a question against the Atlas help-center RAG store.",
        exit_on_error=False,
    )
    parser.add_argument("question", help="Natural-language question, in Chinese or English")
    parser.add_argument("-n", "--top-k", type=int, default=3, help="Number of results per source (default 3)")
    parser.add_argument("--carrier", help="Pre-filter rule chunks to this applicable_carrier value (e.g. FR, IJ, W4/W6/W9)")
    parser.add_argument("--faq-only", action="store_true", help="Only search the FAQ collection")
    parser.add_argument("--rules-only", action="store_true", help="Only search the rule-chunk collection")
    return parser


def run_query(question: str, top_k: int, carrier: str | None, faq_only: bool, rules_only: bool):
    if not rules_only:
        print(f"=== FAQ 结果（Top {top_k}） ===")
        faq_hits = search_faq(question, n_results=top_k)
        if not faq_hits:
            print("(无结果)")
        for h in faq_hits:
            print(f"\n[{h['distance']:.3f}] ({h['topic']}) {h['question']}")
            print(f"  {h['answer']}")

    if not faq_only:
        where = {"applicable_carrier": carrier} if carrier else None
        print(f"\n=== 规则 Chunk 结果（Top {top_k}{f'，过滤 applicable_carrier={carrier}' if carrier else ''}） ===")
        rule_hits = search_rules(question, n_results=top_k, where=where)
        if not rule_hits:
            print("(无结果，考虑去掉 --carrier 过滤再试)")
        for h in rule_hits:
            print(f"\n[{h['distance']:.3f}] {h['level1_category']} / {h['level2_category']} — {h['section']}")
            print(f"  所属文章：{h['parent_title']}（{h['source_path']}）")
            print(f"  适用航司：{h['applicable_carrier']}")
            print(f"  {h['text']}")


def interactive_loop():
    print("交互模式（模型只会加载这一次）。输入问题回车检索，输入 exit / quit 退出。")
    print("同一行可以加参数，比如：航班提前多久可以非自愿退票 --carrier FR\n")
    line_parser = build_parser()
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line or line.lower() in ("exit", "quit"):
            break
        try:
            tokens = shlex.split(line)
            args = line_parser.parse_args(tokens)
        except (argparse.ArgumentError, SystemExit):
            print("参数解析失败，请检查格式，例如：问题内容 --carrier FR -n 5")
            continue
        run_query(args.question, args.top_k, args.carrier, args.faq_only, args.rules_only)
        print()


def main():
    # First pass: does argv contain a question (any non-flag token)?
    has_question = any(not a.startswith("-") for a in sys.argv[1:])
    if not has_question:
        interactive_loop()
        return

    parser = build_parser()
    args = parser.parse_args()
    run_query(args.question, args.top_k, args.carrier, args.faq_only, args.rules_only)


if __name__ == "__main__":
    main()
