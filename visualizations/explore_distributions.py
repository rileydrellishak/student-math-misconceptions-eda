"""
Phase 1, Task 2: Explore Misconception Category Distributions
MAP – Charting Student Math Misunderstandings
==============================================
Paths resolve from the repository root automatically.
Outputs:
  - figures/fig1_category_breakdown.png
  - figures/fig2_misconception_freq.png
  - figures/fig3_labeled_vs_unlabeled.png
  - figures/fig4_top10_by_question.png
    - data/explore_distributions/distribution_summary.md
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = DATA_DIR / "explore_distributions"

Path("figures").mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── LOAD ──────────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_DIR / "initial_cleaning" / "train_clean.csv")
df["Misconception"] = df["Misconception"].replace("Wrong_Fraction", "Wrong_fraction")

# ── COLOR PALETTE ─────────────────────────────────────────────────────────────
PALETTE = {
    "True_Correct":        "#4CAF50",
    "True_Misconception":  "#FF9800",
    "True_Neither":        "#9E9E9E",
    "False_Misconception": "#F44336",
    "False_Neither":       "#90A4AE",
    "False_Correct":       "#9C27B0",
}

cat_counts = df["Category"].value_counts()
labeled    = df[df["Misconception"].notna()]
misc_freq  = labeled["Misconception"].value_counts().reset_index()
misc_freq.columns = ["label", "count"]
misc_freq["pct"] = (misc_freq["count"] / len(labeled) * 100).round(1)

# ── FIG 1: RESPONSE CATEGORY DONUT ───────────────────────────────────────────
colors = [PALETTE.get(c, "#ccc") for c in cat_counts.index]
fig, ax = plt.subplots(figsize=(8, 5))
wedges, texts, autotexts = ax.pie(
    cat_counts.values,
    labels=cat_counts.index,
    autopct="%1.1f%%",
    colors=colors,
    startangle=140,
    pctdistance=0.82,
    wedgeprops=dict(width=0.55)
)
for t in autotexts:
    t.set_fontsize(8)
ax.set_title("Response Category Breakdown\n(n = 36,696 student responses)", fontsize=13, pad=12)
plt.tight_layout()
plt.savefig("figures/fig1_category_breakdown.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ fig1 saved")

# ── FIG 2: MISCONCEPTION FREQUENCY BAR ───────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 8))
bars = ax.barh(
    misc_freq["label"][::-1],
    misc_freq["count"][::-1],
    color="#5C6BC0", edgecolor="white", linewidth=0.4
)
for bar, pct in zip(bars, misc_freq["pct"][::-1]):
    ax.text(bar.get_width() + 15, bar.get_y() + bar.get_height()/2,
            f"{pct}%", va="center", fontsize=7.5, color="#444")
ax.set_xlabel("Number of student responses", fontsize=10)
ax.set_title(f"Misconception Label Frequency\n(n = {len(labeled):,} labeled responses, {misc_freq.shape[0]} unique labels)",
             fontsize=12)
mean_val = misc_freq["count"].mean()
ax.axvline(x=mean_val, color="#E53935", linestyle="--", alpha=0.6, linewidth=1)
ax.text(mean_val + 20, 1, f"mean = {mean_val:.0f}", color="#E53935", fontsize=8)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("figures/fig2_misconception_freq.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ fig2 saved")

# ── FIG 3: LABELED vs UNLABELED by CATEGORY ──────────────────────────────────
df["has_label"] = df["Misconception"].notna()
label_by_cat = df.groupby(["Category","has_label"]).size().unstack(fill_value=0)
label_by_cat.columns = ["No label","Has label"]
label_by_cat = label_by_cat.reindex(cat_counts.index)

fig, ax = plt.subplots(figsize=(8, 4.5))
label_by_cat.plot(kind="barh", stacked=True, ax=ax,
                  color=["#CFD8DC","#5C6BC0"], edgecolor="white")
ax.set_xlabel("Number of responses")
ax.set_title("Labeled vs. Unlabeled Responses by Category", fontsize=12)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("figures/fig3_labeled_vs_unlabeled.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ fig3 saved")

# ── FIG 4: TOP 10 MISCONCEPTIONS PER QUESTION (heatmap) ──────────────────────
top10 = misc_freq["label"].head(10).tolist()
heatmap_df = (
    labeled[labeled["Misconception"].isin(top10)]
    .groupby(["QuestionId","Misconception"])
    .size()
    .unstack(fill_value=0)
)
heatmap_pct = heatmap_df.div(heatmap_df.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(12, 5))
sns.heatmap(
    heatmap_pct, annot=True, fmt=".0f", cmap="Blues",
    linewidths=0.4, linecolor="#e0e0e0", ax=ax,
    cbar_kws={"label": "% of question's labeled responses"}
)
ax.set_title("Top 10 Misconceptions by Question\n(% of each question's labeled responses)", fontsize=12)
ax.set_xlabel("Misconception label")
ax.set_ylabel("Question ID")
plt.xticks(rotation=35, ha="right", fontsize=8)
plt.tight_layout()
plt.savefig("figures/fig4_top10_by_question.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ fig4 saved")

# ── DISTRIBUTION SUMMARY REPORT ───────────────────────────────────────────────
total        = len(df)
n_labeled    = labeled.shape[0]
n_incorrect  = df[df["Category"] != "True_Correct"].shape[0]
n_inc_labeled = df[(df["Category"] != "True_Correct") & df["Misconception"].notna()].shape[0]
top5_pct      = misc_freq["pct"].head(5).sum()
top10_pct     = misc_freq["pct"].head(10).sum()

dom = (
    labeled.groupby("QuestionId")["Misconception"]
    .agg(lambda x: x.value_counts().idxmax())
    .reset_index()
    .rename(columns={"Misconception": "dominant_misconception"})
)

lines = [
    "# Distribution Summary — Phase 1, Task 2\n",
    f"## Quick Stats",
    f"- Total responses: {total:,}",
    f"- Labeled with a misconception: {n_labeled:,} ({n_labeled/total*100:.1f}%)",
    f"- Incorrect responses (non-True_Correct): {n_incorrect:,}",
    f"- Incorrect w/ a misconception label: {n_inc_labeled:,} ({n_inc_labeled/n_incorrect*100:.1f}% of incorrect)",
    f"- Top 5 labels cover: {top5_pct:.1f}% of labeled responses",
    f"- Top 10 labels cover: {top10_pct:.1f}% of labeled responses",
    f"\n## Category Counts\n{cat_counts.to_string()}",
    f"\n## Full Misconception Frequency\n{misc_freq.to_string(index=False)}",
    f"\n## Rarest Labels (< 30 occurrences)\n{misc_freq[misc_freq['count'] < 30][['label','count','pct']].to_string(index=False)}",
    f"\n## Dominant Misconception per Question\n{dom.to_string(index=False)}",
]

with open(OUTPUT_DIR / "distribution_summary.md","w") as f:
    f.write("\n".join(lines))

print("\n✅ All done.")
print(f"   Figures → figures/")
print(f"   Summary → data/explore_distributions/distribution_summary.md")
print(f"\n📊 Key numbers:")
print(f"   Labeled: {n_labeled:,} / {total:,} ({n_labeled/total*100:.1f}%)")
print(f"   Top 5 labels: {top5_pct:.1f}% of labeled")
print(f"\n   Top 10 misconceptions:")
print(misc_freq.head(10)[["label","count","pct"]].to_string(index=False))
