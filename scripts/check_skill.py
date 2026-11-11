import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "copy-studio"
skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
template = (SKILL_DIR / "references" / "channel-calibration-template.md").read_text(encoding="utf-8")
errors = []

# Every §X the skill cites must be a section the template scaffolds
sections = set(re.findall(r"^\| ([A-Z]) \|", template, re.M)) | set(re.findall(r"^## §([A-Z]+)\b", template, re.M))
for sec in sorted(set(re.findall(r"§([A-Z]+)\b", skill))):
    if sec not in sections:
        errors.append(f"SKILL.md cites §{sec}, which the template doesn't define")

# A blank line inside a table splits it in two
lines = skill.splitlines()
for i in range(1, len(lines) - 1):
    if not lines[i].strip() and lines[i - 1].startswith("|") and lines[i + 1].startswith("|"):
        errors.append(f"SKILL.md line {i + 1}: blank line splits a table")

# Every row has the same column count as its header
table = []
for n, line in enumerate(lines + [""], 1):
    if line.startswith("|"):
        table.append((n, line.count("|")))
        continue
    for row_no, cols in table:
        if cols != table[0][1]:
            errors.append(f"SKILL.md line {row_no}: column count differs from the header")
    table = []

# "eight-point" must match the pre-show self-check list
m = re.search(r"\*\*Pre-show self-check\*\*.*?\n\n((?:\d+\. .*\n)+)", skill)
if not m:
    errors.append("pre-show self-check list not found")
elif "eight-point" in skill and len(re.findall(r"^\d+\. ", m.group(1), re.M)) != 8:
    errors.append("the done-check says eight-point, the self-check list has a different count")

for e in errors:
    print("✗", e)
print("OK" if not errors else f"{len(errors)} problem(s)")
sys.exit(1 if errors else 0)
