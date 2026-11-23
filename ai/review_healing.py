import json
from pathlib import Path

PENDING = Path("ai/healing_pending.jsonl")
REPORT = Path("ai/healing_report.md")
SKIP_FILES = {"test_healing_demo.py"}  # this demo uses a wrong locator on purpose

if not PENDING.exists() or not PENDING.read_text(encoding="utf-8").strip():
    print("No pending healing suggestions.")
    raise SystemExit

records = [json.loads(line) for line in PENDING.read_text(encoding="utf-8").splitlines() if line.strip()]

for r in records:
    print(f"\n{r['time']} | element: {r['element']}")
    print(f"  old locator: {r['old']}")
    print(f"  AI suggests: {r['new']}")
    answer = input("Approve and update the tests? (y/n): ").strip().lower()

    if answer == "y":
        changed = []
        for f in Path("tests").glob("*.py"):
            if f.name in SKIP_FILES:
                continue
            text = f.read_text(encoding="utf-8")
            if r["old"] in text:
                f.write_text(text.replace(r["old"], r["new"]), encoding="utf-8")
                changed.append(f.name)
        status = "approved"
        files = ", ".join(changed) or "none"
        print("  Approved. Files updated:", files)
    else:
        status = "rejected"
        files = "none"
        print("  Rejected. Nothing changed.")

    with REPORT.open("a", encoding="utf-8") as rep:
                rep.write(f"- {r['time']} | {status} | old: `{r['old']}` | new: `{r['new']}` | files: {files}\n")

PENDING.write_text("", encoding="utf-8")
print("\nAll suggestions reviewed.")