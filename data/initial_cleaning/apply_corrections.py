"""
Phase 1, Task 1 — Apply Dataset Corrections
MAP – Charting Student Math Misunderstandings
=============================================
Paths resolve from the repository root automatically.
Corrections applied:
  1. Consolidate Wrong_Fraction → Wrong_fraction (case dedupe)
  2. Reclassify 3 mislabeled Q91695 rows from False_Neither → True_Correct
  3. Add data_quality_note column flagging the mislabeled rows
Output:
  - data/initial_cleaning/train_clean.csv   (overwritten with corrections)
  - data/initial_cleaning/corrections_log.md (plain-language record of what changed)
"""

import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = DATA_DIR / "initial_cleaning"

df = pd.read_csv(OUTPUT_DIR / "train_clean.csv")

log = ["# Corrections Log\n"]
log.append(f"**Starting shape:** {df.shape[0]:,} rows × {df.shape[1]} columns\n")

# ── 1. ADD DATA QUALITY NOTE COLUMN ──────────────────────────────────────────

df["data_quality_note"] = ""

# ── 2. CONSOLIDATE Wrong_Fraction → Wrong_fraction ───────────────────────────

before = (df["Misconception"] == "Wrong_Fraction").sum()
df["Misconception"] = df["Misconception"].replace("Wrong_Fraction", "Wrong_fraction")
after = (df["Misconception"] == "Wrong_Fraction").sum()

log.append("## Correction 1 — Misconception Label Dedupe\n")
log.append(f"  - Replaced `Wrong_Fraction` (capital F) with `Wrong_fraction` across {before:,} rows\n")
log.append(f"  - `Wrong_Fraction` remaining after fix: {after:,}\n")

# ── 3. RECLASSIFY MISLABELED Q91695 ROWS ─────────────────────────────────────

# These are False_Neither rows that answered 22 — the correct answer
mislabeled_mask = (
    (df["QuestionId"] == 91695) &
    (df["Category"] == "False_Neither") &
    (df["MC_Answer"].astype(str).str.strip() == "22")
)

mislabeled_count = mislabeled_mask.sum()

df.loc[mislabeled_mask, "Category"] = "True_Correct"
df.loc[mislabeled_mask, "data_quality_note"] = "reclassified_from_False_Neither: answer_22_is_correct"

log.append("\n## Correction 2 — Q91695 Mislabeled Correct Answers\n")
log.append(f"  - Found {mislabeled_count:,} rows in Q91695 where MC_Answer = 22 (correct) but Category = False_Neither\n")
log.append(f"  - Reclassified these rows to `True_Correct`\n")
log.append(f"  - Added `data_quality_note` = `reclassified_from_False_Neither: answer_22_is_correct`\n")
log.append("  - Dashboard note: this is a data quality finding worth naming — curated datasets have noise\n")

# ── 4. VERIFY ─────────────────────────────────────────────────────────────────

log.append("\n## Post-Correction Verification\n")
log.append(f"  - Unique Misconception labels: {df['Misconception'].nunique():,}\n")
log.append(f"  - Wrong_Fraction (old): {(df['Misconception'] == 'Wrong_Fraction').sum():,} (should be 0)\n")
log.append(f"  - Wrong_fraction (canonical): {(df['Misconception'] == 'Wrong_fraction').sum():,}\n")
log.append(f"\n  - Category breakdown after reclassification:\n")
log.append(df["Category"].value_counts().to_string() + "\n")
log.append(f"\n  - Rows with data_quality_note: {(df['data_quality_note'] != '').sum():,}\n")
log.append(f"\n**Final shape:** {df.shape[0]:,} rows × {df.shape[1]} columns\n")

# ── 5. SAVE ───────────────────────────────────────────────────────────────────

df.to_csv(OUTPUT_DIR / "train_clean.csv", index=False)

with open(OUTPUT_DIR / "corrections_log.md", "w") as f:
    f.write("\n".join(log))

print("✅ Done.")
print(f"   Updated data  → data/initial_cleaning/train_clean.csv")
print(f"   Corrections log → data/initial_cleaning/corrections_log.md")
print(f"\n📋 Quick check:")
print(f"   Wrong_Fraction remaining: {(df['Misconception'] == 'Wrong_Fraction').sum()}")
print(f"   Wrong_fraction count: {(df['Misconception'] == 'Wrong_fraction').sum()}")
print(f"   Reclassified rows: {(df['data_quality_note'] != '').sum()}")
print(f"\n   Category breakdown:")
print(df["Category"].value_counts().to_string())
