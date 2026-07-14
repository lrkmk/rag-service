"""
CLI tool: run natural-language questions against the Chroma RAG store.

Default source is the Help Center:
    python ask.py "退票超过多久 Atlas 就不再处理了"
    python ask.py "航班提前多久可以非自愿退票" --carrier FR

Search API docs instead:
    python ask.py --source api "创建订单需要哪些字段"
    python ask.py --api "429 和 110 的区别"
    python ask.py --api "search.do 和 getOffers.do 怎么选" --doc-type 对比消歧
    python ask.py --api "创建订单 passenger 字段" --endpoint /book.do

Interactive mode:
    python ask.py
    > 退票要多久
    > --api 创建订单需要哪些字段
    > --source api 429 和 110 的区别 -n 5
    > exit

In interactive mode you can put flags before or after the question on the
same line. Use quotes if the question itself contains shell-like characters.
"""

import argparse
import shlex
import sys

from rag_search import search_api_docs, search_api_faq, search_faq, search_rules


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ask a question against the Atlas Help Center or API docs RAG store.",
        exit_on_error=False,
    )
    parser.add_argument("question", nargs="+", help="Natural-language question, in Chinese or English")
    parser.add_argument("-n", "--top-k", type=int, default=3, help="Number of results per source (default 3)")
    parser.add_argument(
        "--source",
        choices=("help", "api"),
        default="help",
        help="Corpus to search: help for Help Center, api for API docs (default: help)",
    )
    parser.add_argument(
        "--api",
        action="store_const",
        const="api",
        dest="source",
        help="Shortcut for --source api",
    )
    parser.add_argument(
        "--help-center",
        action="store_const",
        const="help",
        dest="source",
        help="Shortcut for --source help",
    )
    parser.add_argument(
        "--carrier",
        help="Help Center only: pre-filter rule chunks to this applicable_carrier value (e.g. FR, IJ, W4/W6/W9)",
    )
    parser.add_argument(
        "--doc-type",
        help='API docs only: filter by doc_type, e.g. "对比消歧", "请求参数", "响应组件", "端点概览"',
    )
    parser.add_argument(
        "--endpoint",
        help='API docs only: filter by endpoint, e.g. "/search.do"',
    )
    parser.add_argument("--faq-only", action="store_true", help="Only search the FAQ collection")
    parser.add_argument(
        "--rules-only",
        action="store_true",
        help="Only search the main chunk collection (Help Center rules or API docs chunks)",
    )
    return parser


def _print_faq_hits(title: str, hits: list[dict]):
    print(title)
    if not hits:
        print("(no results)")
        return
    for h in hits:
        print(f"\n[{h['distance']:.3f}] ({h['topic']}) {h['question']}")
        print(f"  {h['answer']}")


def _print_help_hits(title: str, hits: list[dict]):
    print(title)
    if not hits:
        print("(no results; if you used --carrier, try again without that filter)")
        return
    for h in hits:
        print(f"\n[{h['distance']:.3f}] {h['level1_category']} / {h['level2_category']} - {h['section']}")
        print(f"  Article: {h['parent_title']} ({h['source_path']})")
        print(f"  Carrier: {h['applicable_carrier']}")
        print(f"  {h['text']}")


def _print_api_hits(title: str, hits: list[dict]):
    print(title)
    if not hits:
        print("(no results; if you used --doc-type or --endpoint, try again without that filter)")
        return
    for h in hits:
        endpoint = f" endpoint={h['endpoint']}" if h.get("endpoint") else ""
        doc_type = h.get("doc_type") or "API chunk"
        print(f"\n[{h['distance']:.3f}] {doc_type}{endpoint} - {h['section']}")
        print(f"  Source: {h['source_path']}")
        if h.get("compares"):
            print(f"  Compares: {h['compares']}")
        print(f"  {h['text']}")


def run_query(
    question: str,
    top_k: int,
    source: str,
    carrier: str | None,
    doc_type: str | None,
    endpoint: str | None,
    faq_only: bool,
    rules_only: bool,
):
    if source == "api":
        if carrier:
            print("Note: --carrier only applies to Help Center searches; ignoring it for --source api.")

        if not rules_only:
            hits = search_api_faq(question, n_results=top_k)
            _print_faq_hits(f"=== API docs FAQ results (top {top_k}) ===", hits)

        if not faq_only:
            conditions = []
            if doc_type:
                conditions.append({"doc_type": doc_type})
            if endpoint:
                conditions.append({"endpoint": endpoint})
            where = None
            if len(conditions) == 1:
                where = conditions[0]
            elif len(conditions) > 1:
                where = {"$and": conditions}

            suffix = []
            if doc_type:
                suffix.append(f"doc_type={doc_type}")
            if endpoint:
                suffix.append(f"endpoint={endpoint}")
            suffix_text = f", filter: {', '.join(suffix)}" if suffix else ""
            hits = search_api_docs(question, n_results=top_k, where=where)
            _print_api_hits(f"\n=== API docs chunk results (top {top_k}{suffix_text}) ===", hits)
        return

    if doc_type or endpoint:
        print("Note: --doc-type/--endpoint only apply to API docs searches; ignoring them for --source help.")

    if not rules_only:
        hits = search_faq(question, n_results=top_k)
        _print_faq_hits(f"=== Help Center FAQ results (top {top_k}) ===", hits)

    if not faq_only:
        where = {"applicable_carrier": carrier} if carrier else None
        suffix = f", filter: applicable_carrier={carrier}" if carrier else ""
        hits = search_rules(question, n_results=top_k, where=where)
        _print_help_hits(f"\n=== Help Center rule chunk results (top {top_k}{suffix}) ===", hits)


def interactive_loop():
    print("Interactive mode. Enter a question to search; enter exit / quit to leave.")
    print("Examples:")
    print("  退票要多久 --carrier FR")
    print("  --api 创建订单需要哪些字段")
    print("  --source api 429 和 110 的区别 -n 5\n")
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
            print("Argument parsing failed. Example: --api 创建订单需要哪些字段 -n 5")
            continue
        run_query(
            " ".join(args.question),
            args.top_k,
            args.source,
            args.carrier,
            args.doc_type,
            args.endpoint,
            args.faq_only,
            args.rules_only,
        )
        print()


def main():
    if len(sys.argv) == 1:
        interactive_loop()
        return

    parser = build_parser()
    args = parser.parse_args()
    run_query(
        " ".join(args.question),
        args.top_k,
        args.source,
        args.carrier,
        args.doc_type,
        args.endpoint,
        args.faq_only,
        args.rules_only,
    )


if __name__ == "__main__":
    main()
