"""
Extract the master error-code markdown table from 错误码.md into structured
JSON — this is the site's own authoritative code->meaning->retryable->next-step
table (44 rows), strictly a lookup artifact, not something to semantically chunk.
"""
import json
import re
from pathlib import Path

md_path = Path("API文档/05-支持与参考/errors-handing/错误码.md")
text = md_path.read_text(encoding="utf-8")

# find the markdown table block (starts with "| 代码", ends at first blank-ish line after rows)
m = re.search(r"\| 代码.*?\n\|[- ]+\|.*?\n((?:\|.*\n)+)", text)
if not m:
    raise SystemExit("table not found")

rows = []
for line in m.group(1).splitlines():
    line = line.strip()
    if not line.startswith("|"):
        continue
    cells = [c.strip() for c in line.strip("|").split("|")]
    if len(cells) != 4:
        continue
    code = cells[0].strip("`")
    rows.append({
        "code": code,
        "meaning": cells[1],
        "retryable": cells[2],
        "next_step": cells[3],
    })

out_dir = md_path.parent / "_rag-chunks"
out_dir.mkdir(exist_ok=True)
out_path = out_dir / "错误码速查表.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(rows)} rows -> {out_path}")
for r in rows[:3]:
    print(r)
