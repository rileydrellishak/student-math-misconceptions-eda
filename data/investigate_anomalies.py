"""
Phase 1, Task 1 Follow-Up: Anomaly Investigation
MAP – Charting Student Math Misunderstandings
==============================================
Run from repo root: python investigate_anomalies.py
Outputs:
  - data/misconception_labels.md        dedupe check on label taxonomy
  - data/neither_sample.csv             stratified sample of Neither rows for educator review
  - data/neither_sample_summary.md      plain-language briefing on Neither rows
"""

import pandas as pd
import numpy as np

df = pd.read_csv("data/train_clean.csv")

# ── 1. MISCONCEPTION LABEL DEDUPE CHECK ──────────────────────────────────────

labels = df["Misconception"].dropna().unique()
label_series = pd.Series(labels)

# Normalize: lowercase + strip for comparison
label_norm = label_series.str.lower().str.strip()
norm_df = pd.DataFrame({
    "original_label": label_series,
    "normalized": label_norm
})

# Find any pairs that match when normalized but differ in original
dupes = norm_df[norm_df.duplicated(subset="normalized", keep=False)].sort_values("normalized")

report = ["# Misconception Label Dedupe Check\n"]
report.append(f"**Total unique labels (raw):** {len(labels)}\n")
report.append(f"**Total unique labels (normalized):** {label_norm.nunique()}\n")

if dupes.empty:
    report.append("\n✅ No case/whitespace duplicates found.\n")
else:
    report.append(f"\n⚠️ Found {len(dupes)} labels that appear to be duplicates when normalized:\n")
    report.append(dupes.to_string(index=False) + "\n")
    report.append("\n→ Recommend: consolidate to a single canonical label before EDA.\n")

# Full label frequency table for reference
report.append("\n## Full Label Frequency Table\n")
freq = df["Misconception"].value_counts().reset_index()
freq.columns = ["label", "count"]
freq["pct_of_labeled"] = (freq["count"] / freq["count"].sum() * 100).round(1)
report.append(freq.to_string(index=False) + "\n")

with open("data/misconception_labels.md", "w") as f:
    f.write("\n".join(report))

print("✅ Misconception label dedupe → data/misconception_labels.md")

# ── 2. NEITHER SAMPLE FOR EDUCATOR REVIEW ────────────────────────────────────

neither = df[df["Category"].isin(["False_Neither", "True_Neither"])].copy()

summary = ["# Neither Category — Briefing\n"]
summary.append(f"**Total Neither rows:** {len(neither):,}\n")
summary.append(f"  - False_Neither (wrong answer, no misconception track): {(neither['Category']=='False_Neither').sum():,}\n")
summary.append(f"  - True_Neither (correct answer, but not via standard reasoning): {(neither['Category']=='True_Neither').sum():,}\n")

# Distribution by question
summary.append("\n## Neither Rows by Question\n")
by_q = neither.groupby("QuestionId").agg(
    total=("row_id", "count"),
    false_neither=("Category", lambda x: (x == "False_Neither").sum()),
    true_neither=("Category", lambda x: (x == "True_Neither").sum()),
).sort_values("total", ascending=False)
summary.append(by_q.to_string() + "\n")

# MC_Answer distribution within Neither — are certain wrong answers clustering?
summary.append("\n## Most Common MC_Answers in False_Neither rows\n")
false_neither_answers = neither[neither["Category"] == "False_Neither"]["MC_Answer"].value_counts().head(10)
summary.append(false_neither_answers.to_string() + "\n")

with open("data/neither_sample_summary.md", "w") as f:
    f.write("\n".join(summary))

print("✅ Neither summary → data/neither_sample_summary.md")

# Stratified sample: 5 rows per question from False_Neither
# Gives you a spread across all 15 questions rather than clustering on one
false_neither = neither[neither["Category"] == "False_Neither"].copy()
sample = pd.concat([
    grp.sample(min(5, len(grp)), random_state=42)
    for _, grp in false_neither.groupby("QuestionId")
]).reset_index(drop=True)

# Keep only the columns useful for educator review — drop row_id noise
sample_out = sample[["QuestionId", "QuestionText", "MC_Answer", "StudentExplanation", "Category"]].copy()
sample_out.to_csv("data/neither_sample.csv", index=False)

print(f"✅ Neither sample ({len(sample_out)} rows) → data/neither_sample.csv")
print(f"\n📋 Sample breakdown by question:")
print(sample_out["QuestionId"].value_counts().sort_index().to_string())