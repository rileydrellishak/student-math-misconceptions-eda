"""
Phase 1, Task 2: Apply Enhanced Labels to Full Dataset
MAP – Charting Student Math Misunderstandings
==============================================
Paths resolve from the repository root automatically.

Inputs:
    - data/initial_cleaning/train_clean.csv
    - data/annotation_samples/annotation_sample_complete.csv  (your completed annotations)

Outputs:
    - data/enhanced_labels/train_enhanced.csv          full dataset with new label columns
    - data/enhanced_labels/enhancement_summary.md      plain-language summary of what changed
    - data/enhanced_labels/data_quality_flags.csv      rows flagged as probable dataset errors

Calibration source: 300-row annotation sample reviewed by educator.
Rules are grounded in per-question analysis, not generic text matching.
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = DATA_DIR / "enhanced_labels"

# ── LOAD ──────────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_DIR / "initial_cleaning" / "train_clean.csv")
df["Misconception"] = df["Misconception"].replace("Wrong_Fraction", "Wrong_fraction")

annotations = pd.read_csv(DATA_DIR / "annotation_samples" / "annotation_sample_complete.csv")

report = []
quality_flags = []

# ── SEED ENHANCED COLUMNS FROM ORIGINAL ───────────────────────────────────────
# enhanced_label:  the updated misconception label (sub-typed where possible)
# cp_call:         C / P / A / M
# label_source:    "original" | "annotation" | "rule_based" | "data_quality_flag"
df["enhanced_label"] = df["Misconception"]
df["cp_call"] = df["cp_call"] = pd.Series(pd.NA, index=df.index, dtype="string")
df["label_source"] = "original"

# ── STEP 1: APPLY ANNOTATION SAMPLE DIRECTLY ─────────────────────────────────
# For all 300 annotated rows, use your reviewed label as ground truth.

def resolve_annotation(row):
    """Return (enhanced_label, cp_call) from a single annotation row."""
    review = str(row.get("your_review", "")).strip()
    correction = str(row.get("your_correction", "")).strip()
    cp = str(row.get("your_cp_call", "")).strip()
    ai_sub = str(row.get("ai_proposed_sublabel", "")).strip()
    ai_cp = str(row.get("ai_cp_call", "")).strip()

    if review == "Accept":
        return ai_sub, ai_cp
    elif review in ("Modify", "Reject"):
        # If correction says "This is correct" or "correct" → data quality flag
        if correction.lower().startswith("this is correct") or correction.lower() == "this answer and reasoning is correct":
            return "__CORRECT__", cp
        return correction if correction and correction != "nan" else ai_sub, cp if cp and cp != "nan" else ai_cp
    return ai_sub, ai_cp

annotation_map = {}  # row_id → (enhanced_label, cp_call)
for _, arow in annotations.iterrows():
    label, cp = resolve_annotation(arow)
    annotation_map[int(arow["row_id"])] = (label, cp)

applied_annotation = 0
for row_id, (label, cp) in annotation_map.items():
    mask = df["row_id"] == row_id
    if mask.any():
        if label == "__CORRECT__":
            df.loc[mask, "label_source"] = "data_quality_flag"
            quality_flags.append({
                "row_id": row_id,
                "QuestionId": df.loc[mask, "QuestionId"].values[0],
                "original_label": df.loc[mask, "Misconception"].values[0],
                "flag": "Annotated as correct answer — original label likely erroneous",
                "MC_Answer": df.loc[mask, "MC_Answer"].values[0],
                "StudentExplanation": df.loc[mask, "StudentExplanation"].values[0],
            })
        else:
            df.loc[mask, "enhanced_label"] = label
            df.loc[mask, "cp_call"] = cp
            df.loc[mask, "label_source"] = "annotation"
            applied_annotation += 1

report.append(f"## Annotation Sample Applied\n- {applied_annotation} rows updated directly from your annotations\n")

# ── STEP 2: RULE-BASED ENHANCEMENT FOR REMAINING LABELED ROWS ─────────────────
# Only applies to rows with a misconception label that weren't in the annotation sample.
# Rules are derived from annotation calibration — grounded in per-question patterns.

def exp(text):
    return str(text).lower().strip()

def has(text, *terms):
    e = exp(text)
    return any(t in e for t in terms)

labeled_mask = (
    df["Misconception"].notna() &
    (df["label_source"] == "original")  # not already annotated
)

rule_counts = {}

for idx, row in df[labeled_mask].iterrows():
    label = row["Misconception"]
    e = exp(row["StudentExplanation"])
    q = str(row["QuestionId"])
    mc = str(row["MC_Answer"]).strip()
    qt = exp(row["QuestionText"])

    new_label = label
    new_cp = np.nan
    source = "rule_based"

    # ── INCOMPLETE ──────────────────────────────────────────────────────────
    if label == "Incomplete":
        simplest_in_q = "simplest" in qt or "simplest form" in qt

        # Claims fraction IS already simplified — conceptual gap
        claims_simplified = has(e,
            "simplest form", "can't simplify", "cannot simplify",
            "already simplified", "can no longer", "is simplified",
            "it is in its", "already in", "can not simplify"
        )

        # Only describes counting/identification, ignores simplification direction
        identification_only = (
            simplest_in_q and
            not has(e, "simplif", "reduc", "divid", "factor", "common", "lowest") and
            has(e, "shad", "count", "triangle", "not shad", "total", "out of",
                "aren't shad", "are not shad", "equal", "because", "colou")
        )

        if simplest_in_q and claims_simplified:
            new_label = "Incomplete — Incomplete-simplification"
            new_cp = "C"
        elif identification_only:
            new_label = "Incomplete — Incomplete-direction"
            new_cp = "P"
        elif has(e, "divid", "multipl", "times", "first", "then", "next", "step"):
            new_label = "Incomplete — Incomplete-procedure"
            new_cp = "A"
        else:
            new_label = "Incomplete"
            new_cp = "A"

    # ── DUPLICATION (Q32833 calibration) ──────────────────────────────────
    elif label == "Duplication":
        # Q32833: 2/3 × 5 — students multiplied both num and denom by 5 → Mult
        if q == "32833" and has(e, "2x5", "2 x 5", "2*5", "times 5", "× 5", "x 5",
                                  "five times", "5x2", "5 x 2", "5*2"):
            new_label = "Mult — multiplied numerator and denominator"
            new_cp = "P"
        elif has(e, "times both", "top and bottom", "both by", "multiply both"):
            new_label = "Mult — multiplied numerator and denominator"
            new_cp = "P"
        elif not has(e, "divid", "multipl", "add", "subtract", "times", "calcul"):
            new_label = "Duplication"
            new_cp = "P"
        else:
            new_label = "Duplication"
            new_cp = "P"

    # ── INVERSION (Q32833 calibration) ────────────────────────────────────
    elif label == "Inversion":
        # Q32833: 2/3 × 5 — students applied KCF to a multiplication problem
        kcf_signals = has(e,
            "flip", "1/5", "reciprocal", "kcf", "keep", "keep change",
            "denominator by", "denom", "leave the 2", "leave 2",
            "only the denominator", "keep the numerator", "keep numerator",
            "put 5 over 1", "5 over 1", "5/1", "turn 5 into"
        )
        if kcf_signals:
            new_label = "Inversion — KCF misapplication"
            new_cp = "P"
        elif has(e, "flip", "flipped", "switch", "swap", "upside", "turn over"):
            new_label = "Inversion — flip without justification"
            new_cp = "P"
        else:
            new_label = "Inversion"
            new_cp = "P"

    # ── WRONG_FRACTION ─────────────────────────────────────────────────────
    elif label == "Wrong_fraction":
        # Q31777: 3/5 of 120, answer=48 → used 2/5 (complement)
        complement_31777 = (
            q == "31777" and
            has(e, "2/5", "2 / 5", "2 out of 5", "48", "120-72", "120 - 72", "72 minus")
        )
        # Q31777: explicit calculation of complement path
        complement_calc_31777 = (
            q == "31777" and
            has(e, "left", "remain", "rest", "5/5", "whole", "1 - ")
        )
        # Q33471: 5/8 of 24, answer=9 → used 3/8 (the given fraction, not complement)
        complement_33471 = (
            q == "33471" and
            has(e, "3x3", "3 x 3", "3*3", "times 3", "× 3", "by 3", "3 by 3",
                "3/8", "three times three", "3 times 3", "times three")
        )
        # General reciprocal signal
        reciprocal = has(e, "flip", "reciprocal", "invert", "upside", "swap")

        if complement_31777 or complement_calc_31777 or complement_33471:
            new_label = "Wrong_fraction — complement error"
            new_cp = "P"
        elif reciprocal:
            new_label = "Wrong_fraction — reciprocal confusion"
            new_cp = "P"
        else:
            new_label = "Wrong_fraction"
            new_cp = "P"

    # ── MULT ────────────────────────────────────────────────────────────────
    elif label == "Mult":
        # KCF signals in a multiplication context → FlipChange
        kcf_in_mult = has(e,
            "kcf", "kfc", "keep change flip", "keep, change", "flip",
            "reciprocal", "1/6", "÷ becomes ×", "divide becomes"
        )
        # Multiplied both num and denom
        both_parts = has(e,
            "times both", "top and bottom", "both by",
            "multiply both", "all of it"
        )
        # Student admitted not knowing
        no_idea = has(e,
            "don't know", "dont know", "not sure", "no idea",
            "i don't", "didn't know", "wasn't sure"
        )

        if kcf_in_mult:
            new_label = "FlipChange"
            new_cp = "P"
        elif no_idea:
            new_label = "Mult"
            new_cp = "C"
        elif both_parts:
            new_label = "Mult — multiplied numerator and denominator"
            new_cp = "P"
        else:
            new_label = "Mult"
            new_cp = "P"

    # ── ADDITIVE ────────────────────────────────────────────────────────────
    elif label == "Additive":
        # All calibration rows were C — confirmed
        if has(e, "add", "plus", "more", "total", "double", "halv", "added",
                "subtract", "take away", "minus", "difference"):
            new_label = "Additive"
            new_cp = "C"
        else:
            new_label = "Additive"
            new_cp = "C"

    # ── SUBTRACTION ─────────────────────────────────────────────────────────
    elif label == "Subtraction":
        # All calibration rows were P — confirmed
        if has(e, "subtract", "minus", "take away", "less", "difference",
                "took off", "remove", "half", "halv"):
            new_label = "Subtraction"
            new_cp = "P"
        else:
            new_label = "Subtraction"
            new_cp = "P"

    # ── POSITIVE ────────────────────────────────────────────────────────────
    elif label == "Positive":
        # All calibration rows were C — confirmed
        # Sub-type: "two negatives = positive" rule misapplied
        rule_misapply = has(e,
            "two negative", "negative negative", "double negative",
            "makes positive", "becomes positive", "positive positive"
        )
        # Sub-type: accurate direction sense but absolute value confusion
        abs_value_confusion = has(e,
            "gets higher", "going higher", "goes up", "less negative",
            "higher up", "bigger number", "more positive"
        )
        if rule_misapply:
            new_label = "Positive — double-negative rule misapplied"
            new_cp = "C"
        elif abs_value_confusion:
            new_label = "Positive — absolute value confusion"
            new_cp = "C"
        else:
            new_label = "Positive"
            new_cp = "C"

    # ── WRONG_TERM ──────────────────────────────────────────────────────────
    elif label == "Wrong_term":
        # Q91695 data quality: MC=22 with +4 reasoning → these are correct answers
        if q == "91695" and mc in ["\\( 22 \\)", "22"]:
            if has(e, "+4", "add 4", "adds 4", "adding 4", "plus 4",
                      "goes up by 4", "up by 4", "increase by 4", "increases by 4",
                      "4 every", "by 4 each", "4 each", "4 more", "4n", "4 times"):
                source = "data_quality_flag"
                quality_flags.append({
                    "row_id": row["row_id"],
                    "QuestionId": row["QuestionId"],
                    "original_label": "Wrong_term",
                    "flag": "Q91695: MC=22 with correct +4 pattern reasoning — likely True_Correct mislabeled as Wrong_term",
                    "MC_Answer": mc,
                    "StudentExplanation": row["StudentExplanation"],
                })
                df.at[idx, "label_source"] = "data_quality_flag"
                continue

        # MC=20 on Q91695 with additive reasoning → Additive
        if q == "91695" and mc in ["\\( 20 \\)", "20"]:
            if has(e, "+4", "add 4", "up by 4", "4 each", "4 more", "4 every"):
                new_label = "Additive"
                new_cp = "C"
            else:
                new_label = "Wrong_term"
                new_cp = "A"
        elif has(e, "numerator", "denominator", "must be the same", "have to be equal",
                     "top and bottom must"):
            new_label = "Wrong_term"
            new_cp = "C"
        elif has(e, "common denominator", "equivalent", "same bottom", "times both"):
            new_label = "Wrong_term"
            new_cp = "P"
        else:
            new_label = "Wrong_term"
            new_cp = "A"

    # ── IRRELEVANT ──────────────────────────────────────────────────────────
    elif label == "Irrelevant":
        # Q31778 (A/10=9/15): students who saw 3 as common factor → Unknowable
        common_factor_31778 = (
            q == "31778" and
            has(e, "times table", "3 times", "3x3", "3 goes", "factor",
                   "multiple", "3 into", "3 and", "9 and 15", "9 is", "15 is",
                   "in the 3", "common")
        )
        # Student has correct reasoning but selected wrong answer → flag
        correct_reasoning = has(e,
            "multiply by 3", "multiplied by 3", "× 3", "times 3",
            "÷ 3", "divided by 3", "5 times table", "count in"
        )

        if common_factor_31778:
            new_label = "Unknowable"
            new_cp = "M"
        elif has(e, "don't know", "not sure", "guessed", "guess", "just thought",
                    "randomly", "just picked"):
            new_label = "Irrelevant — vague"
            new_cp = "M"
        elif correct_reasoning and q == "31778":
            source = "data_quality_flag"
            quality_flags.append({
                "row_id": row["row_id"],
                "QuestionId": row["QuestionId"],
                "original_label": "Irrelevant",
                "flag": "Q31778: explanation references correct scaling reasoning — may be mislabeled",
                "MC_Answer": mc,
                "StudentExplanation": row["StudentExplanation"],
            })
            df.at[idx, "label_source"] = "data_quality_flag"
            continue
        elif len(str(row["StudentExplanation"]).strip()) < 15:
            new_label = "Irrelevant — content-free"
            new_cp = "M"
        else:
            new_label = "Irrelevant — vague"
            new_cp = "M"

    # ── ALL OTHER LABELS: assign C/P from codebook defaults ───────────────
    else:
        cp_defaults = {
            "WNB": "C", "Whole_numbers_larger": "C", "Longer_is_bigger": "C",
            "Shorter_is_bigger": "C", "Adding_across": "C", "Denominator-only_change": "C",
            "Scale": "C", "Not_variable": "C", "Adding_terms": "C",
            "Base_rate": "C", "Certainty": "C",
            "Incorrect_equivalent_fraction_addition": "C", "Definition": "C",
            "Interior": "C", "Positive": "C",
            "Tacking": "P", "SwapDividend": "P", "FlipChange": "P",
            "Division": "P", "Firstterm": "P", "Inverse_operation": "P",
            "Multiplying_by_4": "P", "Wrong_Operation": "P",
            "Unknowable": "M", "Irrelevant": "M",
            "Wrong_term": "A",
        }
        new_cp = cp_defaults.get(label, np.nan)
        new_label = label
        source = "codebook_default"

    df.at[idx, "enhanced_label"] = new_label
    df.at[idx, "cp_call"] = new_cp
    df.at[idx, "label_source"] = source
    rule_counts[new_label] = rule_counts.get(new_label, 0) + 1

# ── STEP 3: SUMMARY STATS ─────────────────────────────────────────────────────
total = len(df)
labeled = df["Misconception"].notna().sum()
enhanced = (df["label_source"] != "original").sum()
flagged = len(quality_flags)
annotation_rows = (df["label_source"] == "annotation").sum()
rule_rows = (df["label_source"] == "rule_based").sum()
default_rows = (df["label_source"] == "codebook_default").sum()

report.append(f"## Enhancement Summary\n")
report.append(f"- Total rows: {total:,}")
report.append(f"- Rows with a misconception label: {labeled:,}")
report.append(f"- Rows enhanced (annotation + rules + defaults): {enhanced:,}")
report.append(f"  - From your 300-row annotation: {annotation_rows:,}")
report.append(f"  - From calibrated rules: {rule_rows:,}")
report.append(f"  - From codebook C/P defaults: {default_rows:,}")
report.append(f"- Data quality flags raised: {flagged:,}\n")

report.append("## C/P Distribution (enhanced labels only)")
cp_dist = df[df["cp_call"].notna()]["cp_call"].value_counts()
for cp, n in cp_dist.items():
    pct = n / labeled * 100
    report.append(f"  - {cp}: {n:,} ({pct:.1f}% of labeled)")

report.append("\n## Enhanced Label Frequency (top 30)")
el_freq = df[df["enhanced_label"].notna()]["enhanced_label"].value_counts().head(30)
report.append(el_freq.to_string())

report.append("\n## Data Quality Flags")
report.append(f"  {flagged} rows flagged — see data/enhanced_labels/data_quality_flags.csv\n")
for f in quality_flags[:10]:
    report.append(f"  - row_id={f['row_id']} Q{f['QuestionId']}: {f['flag']}")
if flagged > 10:
    report.append(f"  ... and {flagged - 10} more")

# ── SAVE ──────────────────────────────────────────────────────────────────────
df.to_csv(OUTPUT_DIR / "train_enhanced.csv", index=False)

flags_df = pd.DataFrame(quality_flags)
if not flags_df.empty:
    flags_df.to_csv(OUTPUT_DIR / "data_quality_flags.csv", index=False)
else:
    pd.DataFrame(columns=["row_id","QuestionId","original_label","flag","MC_Answer","StudentExplanation"]
                 ).to_csv(OUTPUT_DIR / "data_quality_flags.csv", index=False)

with open(OUTPUT_DIR / "enhancement_summary.md", "w") as f:
    f.write("# Label Enhancement Summary\n\n")
    f.write("\n".join(report))

print("✅ Done.")
print(f"   Enhanced dataset → data/enhanced_labels/train_enhanced.csv ({df.shape[0]:,} rows)")
print(f"   Quality flags    → data/enhanced_labels/data_quality_flags.csv ({flagged} flags)")
print(f"   Summary          → data/enhanced_labels/enhancement_summary.md")
print(f"\n📊 Quick stats:")
print(f"   Labeled rows:    {labeled:,}")
print(f"   Enhanced:        {enhanced:,}")
print(f"   Quality flags:   {flagged}")
print(f"\n   C/P distribution:")
print(cp_dist.to_string())
print(f"\n   Label source breakdown:")
print(df["label_source"].value_counts().to_string())
print(f"\n   Enhanced label sample (top 20):")
print(el_freq.head(20).to_string())
