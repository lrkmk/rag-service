"""
Extract the 售后服务受理范围 markdown table from Atlas售后服务受理范围.md into
structured JSON — a 一级类别/二级类别/是否受理 lookup ("Atlas 受理改护照信息吗？"
is an exact-lookup question, not a semantic-search one), same rationale as
extract_error_code_table.py's 错误码表.
"""
import json
import re
from pathlib import Path

md_path = Path("doc/帮助中心/04-售后票务/Atlas售后服务受理范围.md")
text = md_path.read_text(encoding="utf-8")

m = re.search(r"\|\s*\*\*一级类别\*\*.*?\n\|[- ]+\|.*?\n((?:\|.*\n)+)", text)
if not m:
    raise SystemExit("table not found")

link_re = re.compile(r"\[([^\]]*)\]\([^)]*\)")

rows = []
for line in m.group(1).splitlines():
    line = line.strip()
    if not line.startswith("|"):
        continue
    cells = [c.strip() for c in line.strip("|").split("|")]
    if len(cells) != 3:
        continue
    level1, level2, status = cells
    level2 = link_re.sub(r"\1", level2)  # keep the visible label, drop the URL
    rows.append({"一级类别": level1, "二级类别": level2, "是否受理": status})

out_dir = md_path.parent / "_rag-chunks"
out_dir.mkdir(exist_ok=True)
out_path = out_dir / "售后服务受理范围表.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"source_path": "04-售后票务/Atlas售后服务受理范围.md", "rows": rows}, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(rows)} rows -> {out_path}")
for r in rows[:3]:
    print(r)
