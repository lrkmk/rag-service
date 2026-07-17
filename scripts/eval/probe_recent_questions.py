"""
Send the first N native-Chinese questions from aoc_eva_recent30d_questions_only.md
to the aoc-test chat endpoint, one at a time with a delay between requests so we
don't hammer the service.

Usage:
    python probe_recent_questions.py [--n 20] [--sleep 30] [--out probe_results.jsonl]
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

import requests

# Windows consoles are often GBK, not UTF-8 - reconfigure so printing Chinese
# text or emoji from responses never crashes the run mid-way.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]
QUESTIONS_FILE = REPO_ROOT / "scripts" / "eval" / "reports" / "aoc_eva_recent30d_questions_only.md"

DEFAULT_ENDPOINT = "https://aoc-test.atlastravel.tech/v1/chat/completions"
DEFAULT_AGENT_ID = "yihan"

ITEM_RE = re.compile(r"^(\d+)\.\s+(.+)$")


def load_zh_questions(path):
    """Pull the numbered items out of the '第一部分：中文原生问题' section only."""
    text = path.read_text(encoding="utf-8")
    section_start = text.index("第一部分")
    section_end = text.index("第二部分") if "第二部分" in text else len(text)
    section = text[section_start:section_end]

    questions = []
    for line in section.splitlines():
        m = ITEM_RE.match(line.strip())
        if m:
            questions.append(m.group(2).strip())
    return questions


def ask(question, endpoint, headers, timeout=120):
    payload = {"model": "openclaw", "messages": [{"role": "user", "content": question}]}
    started = time.time()
    try:
        resp = requests.post(endpoint, headers=headers, json=payload, timeout=timeout)
        elapsed = time.time() - started
        try:
            body = resp.json()
        except ValueError:
            body = {"raw_text": resp.text[:2000]}
        return {
            "status_code": resp.status_code,
            "elapsed_sec": round(elapsed, 2),
            "response": body,
        }
    except requests.RequestException as e:
        elapsed = time.time() - started
        return {
            "status_code": None,
            "elapsed_sec": round(elapsed, 2),
            "error": str(e),
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=20, help="how many questions to send (default 20)")
    parser.add_argument("--sleep", type=float, default=30, help="seconds to wait between requests (default 30)")
    parser.add_argument("--out", default="probe_results.jsonl", help="output JSONL path")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="chat completions URL")
    parser.add_argument("--agent-id", default=DEFAULT_AGENT_ID, help="x-openclaw-agent-id header value")
    parser.add_argument("--questions-file", default=None, help="plain text file, one question per line, overrides --n/default source")
    args = parser.parse_args()

    headers = {
        "Authorization": "Bearer 88888888",
        "Content-Type": "application/json",
        "x-openclaw-agent-id": args.agent_id,
    }

    if args.questions_file:
        questions = [l.strip() for l in Path(args.questions_file).read_text(encoding="utf-8").splitlines() if l.strip()]
        print(f"Loaded {len(questions)} questions from {args.questions_file}")
    else:
        questions = load_zh_questions(QUESTIONS_FILE)[: args.n]
        print(f"Loaded {len(questions)} questions from {QUESTIONS_FILE.name}")
    print(f"Endpoint: {args.endpoint}  agent-id: {args.agent_id}  sleep: {args.sleep}s")

    out_path = Path(args.out)
    with out_path.open("w", encoding="utf-8") as f:
        for i, q in enumerate(questions, 1):
            print(f"[{i}/{len(questions)}] asking: {q[:60]!r}")
            result = ask(q, args.endpoint, headers)
            record = {"index": i, "question": q, **result}
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()

            if "error" in result:
                print(f"    -> ERROR: {result['error']} ({result['elapsed_sec']}s)")
            else:
                content = ""
                try:
                    content = result["response"]["choices"][0]["message"]["content"]
                except (KeyError, IndexError, TypeError):
                    content = str(result["response"])[:200]
                print(f"    -> {result['status_code']} in {result['elapsed_sec']}s: {content[:80]!r}")

            if i < len(questions):
                time.sleep(args.sleep)

    print(f"\nDone. Wrote {len(questions)} results to {out_path}")


if __name__ == "__main__":
    main()
