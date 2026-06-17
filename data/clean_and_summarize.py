"""
Phase 1, Task 1: Load and Clean the Dataset
MAP – Charting Student Math Misunderstandings
=============================================
Run from repo root: python clean_and_summarize.py
Outputs:
  - data/train_clean.csv       cleaned dataset
  - data/cleaning_summary.md   plain-language summary report
"""

import pandas as pd
import numpy as np

# ── 1. LOAD ──────────────────────────────────────────────────────────────────

df = pd.read_csv("data/train.csv")

report = []
report.append("# Cleaning Summary Report\n")
report.append(f"**Raw shape:** {df.shape[0]:,} rows × {df.shape[1]} columns\n")
report.append(f"**Columns:** {list(df.columns)}\n")

# ── 2. DTYPES & BASIC PROFILE ─────────────────────────────────────────────

report.append("## Column Types\n")
report.append(df.dtypes.to_string() + "\n")

# ── 3. NULL / MISSING AUDIT ───────────────────────────────────────────────

null_counts = df.isnull().sum()
null_pct    = (null_counts / len(df) * 100).round(2)
null_df     = pd.DataFrame({"null_count": null_counts, "null_pct": null_pct})
null_df     = null_df[null_df["null_count"] > 0]

report.append("\n## Null / Missing Values\n")
if null_df.empty:
    report.append("✅ No null values found.\n")
else:
    report.append(null_df.to_string() + "\n")

# Also flag literal "NA" strings (common in this dataset for Misconception col)
report.append("\n## Literal 'NA' String Counts (not the same as null)\n")
for col in df.select_dtypes(include=["object", "string"]).columns:
    na_str_count = (df[col].astype(str).str.strip().str.upper() == "NA").sum()
    if na_str_count > 0:
        report.append(f"  - `{col}`: {na_str_count:,} rows contain the string 'NA'\n")

# ── 4. DUPLICATES ─────────────────────────────────────────────────────────

dup_full = df.duplicated().sum()
dup_rowid = df.duplicated(subset=["row_id"]).sum()
dup_combo = df.duplicated(subset=["QuestionId", "MC_Answer", "StudentExplanation"]).sum()

report.append(f"\n## Duplicates\n")
report.append(f"  - Full duplicate rows: {dup_full:,}\n")
report.append(f"  - Duplicate row_id values: {dup_rowid:,}\n")
report.append(f"  - Duplicate (QuestionId + MC_Answer + StudentExplanation) combos: {dup_combo:,}\n")

# ── 5. CATEGORY COLUMN AUDIT ─────────────────────────────────────────────

report.append("\n## Category Column — Unique Values\n")
cat_counts = df["Category"].value_counts()
report.append(cat_counts.to_string() + "\n")

# ── 6. MISCONCEPTION COLUMN AUDIT ────────────────────────────────────────

report.append("\n## Misconception Column — Value Overview\n")
# Treat "NA" string as missing
df["Misconception_clean"] = df["Misconception"].replace("NA", np.nan)
misc_null = df["Misconception_clean"].isnull().sum()
misc_filled = df["Misconception_clean"].notna().sum()
misc_unique = df["Misconception_clean"].dropna().nunique()

report.append(f"  - Rows with a misconception label: {misc_filled:,}\n")
report.append(f"  - Rows without a misconception label (NA): {misc_null:,}\n")
report.append(f"  - Unique misconception labels: {misc_unique:,}\n")

report.append("\n### Top 20 Most Frequent Misconceptions\n")
top_misc = df["Misconception_clean"].value_counts().head(20)
report.append(top_misc.to_string() + "\n")

# ── 7. QUESTION TEXT — IMAGE REFERENCES ──────────────────────────────────

has_image = df["QuestionText"].str.contains(r"\[Image:", na=False)
report.append(f"\n## Questions Referencing Images\n")
report.append(f"  - {has_image.sum():,} of {len(df):,} rows ({has_image.mean()*100:.1f}%) reference an image in QuestionText\n")
report.append("  ⚠️  Image content is described in text only — no actual image data available.\n")

# ── 8. STUDENT EXPLANATION — LENGTH STATS ────────────────────────────────

df["explanation_len"] = df["StudentExplanation"].astype(str).str.len()
report.append(f"\n## Student Explanation Length (characters)\n")
report.append(df["explanation_len"].describe().round(1).to_string() + "\n")

# Flag very short explanations (likely low-signal)
very_short = (df["explanation_len"] < 5).sum()
report.append(f"  - Explanations under 5 characters: {very_short:,} (potentially empty/placeholder)\n")

# ── 9. UNIQUE QUESTIONS ───────────────────────────────────────────────────

report.append(f"\n## Question Coverage\n")
report.append(f"  - Unique QuestionId values: {df['QuestionId'].nunique():,}\n")
report.append(f"  - Average student responses per question: {len(df)/df['QuestionId'].nunique():.1f}\n")

# ── 10. PRODUCE CLEAN DATAFRAME ──────────────────────────────────────────

df_clean = df.copy()

# Normalize Misconception: replace "NA" string with actual NaN
df_clean["Misconception"] = df_clean["Misconception_clean"]
df_clean = df_clean.drop(columns=["Misconception_clean", "explanation_len"])

# Strip whitespace from all string columns
for col in df_clean.select_dtypes(include=["object", "string"]).columns:
    df_clean[col] = df_clean[col].str.strip()

# Drop full duplicate rows (keep first)
dupes_dropped = df_clean.duplicated().sum()
df_clean = df_clean.drop_duplicates()

report.append(f"\n## Cleaning Actions Taken\n")
report.append(f"  - Replaced literal 'NA' strings in Misconception with NaN\n")
report.append(f"  - Stripped leading/trailing whitespace from all string columns\n")
report.append(f"  - Dropped {dupes_dropped:,} fully duplicate rows\n")
report.append(f"\n**Clean shape:** {df_clean.shape[0]:,} rows × {df_clean.shape[1]} columns\n")

# ── 11. FLAG ANOMALIES FOR HUMAN REVIEW ──────────────────────────────────

report.append("\n---\n## ⚠️ Anomalies — Human Review Needed\n")
report.append("These findings need your educator judgment before proceeding:\n\n")

# a. True_Correct rows with a Misconception label (shouldn't exist)
conflict = df_clean[
    (df_clean["Category"] == "True_Correct") &
    (df_clean["Misconception"].notna())
]
report.append(f"1. **True_Correct rows that also have a Misconception label:** {len(conflict):,}\n")
if len(conflict) > 0:
    report.append("   → Should these be reclassified, or is the misconception label a tagging artifact?\n")
    report.append(conflict[["row_id","QuestionId","Category","Misconception"]].head(5).to_string() + "\n")

# b. Non-True_Correct rows missing a Misconception label
missing_misc = df_clean[
    (df_clean["Category"] != "True_Correct") &
    (df_clean["Misconception"].isna())
]
report.append(f"\n2. **Incorrect answers missing a Misconception label:** {len(missing_misc):,}\n")
if len(missing_misc) > 0:
    report.append("   → These are errors without a diagnosis. Worth investigating — are they ambiguous cases or data gaps?\n")

# c. Very short student explanations
short_exp = df_clean[df_clean["StudentExplanation"].astype(str).str.len() < 5]
report.append(f"\n3. **Very short student explanations (< 5 chars):** {len(short_exp):,}\n")
if len(short_exp) > 0:
    report.append("   → Are these meaningful (e.g. '1/3') or placeholder/empty responses to exclude?\n")

# ── 12. SAVE OUTPUTS ─────────────────────────────────────────────────────

df_clean.to_csv("data/train_clean.csv", index=False)

summary_text = "\n".join(report)
with open("data/cleaning_summary.md", "w") as f:
    f.write(summary_text)

print("✅ Done.")
print(f"   Cleaned data  → data/train_clean.csv  ({df_clean.shape[0]:,} rows)")
print(f"   Summary report → data/cleaning_summary.md")
print("\n📋 Quick stats:")
print(f"   Rows: {df_clean.shape[0]:,}")
print(f"   Unique questions: {df_clean['QuestionId'].nunique():,}")
print(f"   Unique misconceptions: {df_clean['Misconception'].nunique():,}")
print(f"   Category breakdown:\n{df_clean['Category'].value_counts().to_string()}")
