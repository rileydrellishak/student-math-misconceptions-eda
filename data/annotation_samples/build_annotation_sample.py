"""
Phase 1, Task 2: Build Annotation Sample
MAP – Charting Student Math Misunderstandings
=============================================
Paths resolve from the repository root automatically.
Inputs:
    - data/initial_cleaning/train_clean.csv
Outputs:
    - data/annotation_samples/annotation_sample.csv    300-row sample, AI proposals pre-filled
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = DATA_DIR / "annotation_samples"

np.random.seed(42)

# ── LOAD ──────────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_DIR / "initial_cleaning" / "train_clean.csv")
df["Misconception"] = df["Misconception"].replace("Wrong_Fraction", "Wrong_fraction")

# ── TOP 10 LABELS ─────────────────────────────────────────────────────────────
TOP10 = [
    "Incomplete",
    "Additive",
    "Duplication",
    "Subtraction",
    "Positive",
    "Wrong_term",
    "Irrelevant",
    "Wrong_fraction",
    "Inversion",
    "Mult",
]

ROWS_PER_LABEL = 30

# ── DIAGNOSIS ENGINE ──────────────────────────────────────────────────────────
# For each label, a function that takes a row and returns:
#   (proposed_sublabel, cp_call, rationale)
# cp_call: "C", "P", "A", or "M"

def explain_len(exp):
    return len(str(exp).strip())

def exp(row):
    return str(row["StudentExplanation"]).strip().lower()

def has(row, *terms):
    e = exp(row)
    return any(t in e for t in terms)

def answer(row):
    return str(row["MC_Answer"]).strip()

# ── INCOMPLETE ────────────────────────────────────────────────────────────────
def diagnose_incomplete(row):
    e = exp(row)
    qt = str(row["QuestionText"]).lower()

    # Sub-type 1: direction missed
    # Signals: "simplest form" in question but student says it IS simplified,
    # or student explains the identification step only (counted, looked, found)
    # without any reference to simplification
    simplest_in_q = "simplest form" in qt or "simplest" in qt
    claims_simplified = any(p in e for p in [
        "simplest form", "can't simplify", "cannot simplify",
        "already simplified", "can no longer", "is simplified",
        "it is in its", "already in"
    ])
    only_identification = (
        simplest_in_q and
        not any(p in e for p in ["simplif", "reduc", "divid", "factor", "common"]) and
        any(p in e for p in ["count", "look", "found", "work", "shad", "not shad"])
    )

    if simplest_in_q and claims_simplified:
        return (
            "Incomplete — Incomplete-simplification",
            "C",
            "Student claims the fraction is already in simplest form, indicating a conceptual gap in understanding what simplification requires (testing for common factors). The 'simplest form' instruction was present in the question."
        )
    if only_identification:
        return (
            "Incomplete — Incomplete-direction",
            "A",
            "Student explains only the identification step (counting, finding the fraction) with no reference to simplification, despite the question asking for simplest form. May have missed the instruction rather than lacking the skill — ambiguous between C and P without further probing."
        )

    # Sub-type 2: procedure started but halted
    procedure_started = any(p in e for p in [
        "divid", "multipl", "times", "add", "subtract", "first", "then",
        "next", "step", "start", "begin", "so i", "because i"
    ])
    if procedure_started:
        return (
            "Incomplete — Incomplete-procedure",
            "A",
            "Student began a procedure but did not complete it. Ambiguous: may be a procedural gap (doesn't know the next step) or conceptual (doesn't know a next step is needed)."
        )

    # Default: not enough signal to sub-type
    return (
        "Incomplete — sub-type unclear",
        "A",
        "Explanation does not contain enough signal to assign a sub-type. Review needed: check whether the question included a direction (e.g. 'simplest form') and whether the student's explanation references or ignores it."
    )

# ── ADDITIVE ──────────────────────────────────────────────────────────────────
def diagnose_additive(row):
    e = exp(row)

    # Strong conceptual signal: student explicitly adds or uses additive language
    # on a multiplicative problem
    explicit_add = any(p in e for p in [
        "add", "plus", "more", "total", "and", "double", "half of",
        "halved", "added", "subtract", "take away", "minus"
    ])
    multiplicative_vocab = any(p in e for p in [
        "times", "multipl", "fraction of", "of the", "percent", "ratio"
    ])

    if explicit_add and not multiplicative_vocab:
        return (
            "Additive",
            "C",
            "Student uses explicitly additive language (adding, doubling, halving) on a multiplicative/proportional problem. No multiplicative reasoning visible. Indicates the additive-to-multiplicative conceptual transition has not occurred."
        )
    if explicit_add and multiplicative_vocab:
        return (
            "Additive",
            "C",
            "Student mixes additive and multiplicative language, suggesting partial understanding of the multiplicative relationship but defaulting to additive operations in execution. Still conceptual — the mental model is not yet fully multiplicative."
        )
    # Minimal explanation
    return (
        "Additive",
        "C",
        "Additive error confirmed by incorrect answer pattern. Explanation is brief but consistent with additive reasoning applied to a multiplicative context. Conceptual: the additive-to-multiplicative transition is the root issue."
    )

# ── DUPLICATION ───────────────────────────────────────────────────────────────
def diagnose_duplication(row):
    e = exp(row)
    a = answer(row)

    no_procedure = not any(p in e for p in [
        "divid", "multipl", "add", "subtract", "times", "calcul",
        "work", "comput", "simplif", "convert"
    ])
    guess_language = any(p in e for p in [
        "think", "guess", "not sure", "unsure", "don't know",
        "because it is", "it looks", "seems", "i think it"
    ])

    if no_procedure and guess_language:
        return (
            "Duplication",
            "P",
            "Student echoed a value from the problem without performing a computation. Guess language present ('I think', 'not sure'). Procedural: student had no entry point into the problem and anchored on a visible number."
        )
    if no_procedure:
        return (
            "Duplication",
            "P",
            "Answer duplicates a value present in the problem (numerator, given number, or other visible quantity). No computational procedure visible in explanation. Procedural: student defaulted to what was available rather than deriving a new value."
        )
    return (
        "Duplication",
        "P",
        "Duplication confirmed by answer pattern. Some procedural language present but the computation did not produce a new value — student ended where they started. Procedural error."
    )

# ── SUBTRACTION ───────────────────────────────────────────────────────────────
def diagnose_subtraction(row):
    e = exp(row)

    explicit_sub = any(p in e for p in [
        "subtract", "minus", "take away", "less", "difference",
        "took off", "remove", "left over", "leftover", "remaining"
    ])
    halving = any(p in e for p in ["half", "halv", "divide by 2", "split"])

    if explicit_sub:
        return (
            "Subtraction",
            "P",
            "Student explicitly describes a subtraction operation where multiplication or proportional reasoning was required. Procedural default — familiar operation applied to unfamiliar context. Check whether student understood this was a multiplication/fraction problem (if not, lean toward C)."
        )
    if halving:
        return (
            "Subtraction",
            "P",
            "Student used repeated halving (a subtraction-adjacent operation) in a context requiring fraction multiplication. Procedural: student substituted a simpler, familiar operation. Note: if student genuinely believed halving was the correct approach here (not just an execution shortcut), reclassify as C."
        )
    return (
        "Subtraction",
        "P",
        "Subtraction error confirmed by answer pattern. Explanation suggests the student applied a subtraction-based approach to a problem requiring a different operation. Likely procedural, but verify whether the student understood the problem type."
    )

# ── POSITIVE ──────────────────────────────────────────────────────────────────
def diagnose_positive(row):
    e = exp(row)

    double_neg_confusion = any(p in e for p in [
        "negative", "minus", "take away", "subtract", "goes down",
        "goes up", "smaller", "bigger", "positive"
    ])
    rule_recall = any(p in e for p in [
        "two negatives", "negative negative", "double negative",
        "makes positive", "becomes positive"
    ])

    if rule_recall:
        return (
            "Positive",
            "C",
            "Student attempted to recall the 'two negatives make a positive' rule but applied it incorrectly. Conceptual: memorized rule without understanding the underlying structure of signed number operations."
        )
    if double_neg_confusion:
        return (
            "Positive",
            "C",
            "Student's explanation reveals confusion about the directionality of negative number operations — treating subtraction of a negative as 'going more negative' rather than 'going less negative.' Conceptual: the number line model for signed numbers is not established."
        )
    return (
        "Positive",
        "C",
        "Positive/negative sign error confirmed by answer. Student ignored or incorrectly handled a negative sign. Conceptual: without an explanation revealing a correct procedure, the default classification is a conceptual gap in signed number understanding."
    )

# ── WRONG_TERM ────────────────────────────────────────────────────────────────
def diagnose_wrong_term(row):
    e = exp(row)

    # Check if procedure accompanying the wrong term is correct or incorrect
    # Signals of correct underlying procedure:
    correct_procedure_signals = any(p in e for p in [
        "common denominator", "equivalent", "same bottom", "times both",
        "multiply top and bottom", "scale", "simplif"
    ])
    # Signals of wrong concept accompanying wrong term:
    wrong_concept_signals = any(p in e for p in [
        "must be the same", "have to be equal", "numerator and denominator",
        "top and bottom must", "both parts"
    ])

    if wrong_concept_signals and not correct_procedure_signals:
        return (
            "Wrong_term",
            "C",
            "Student uses incorrect mathematical vocabulary AND the underlying concept is wrong (e.g., 'numerator and denominator must be the same' — a misstatement of both the term and the rule). Reclassify toward C: the vocabulary error is a symptom of a conceptual misunderstanding."
        )
    if correct_procedure_signals:
        return (
            "Wrong_term",
            "P",
            "Student uses an incorrect term but the surrounding explanation suggests the underlying procedure is intact. Vocabulary error with correct concept = lower priority. Primarily a language/terminology fix."
        )
    return (
        "Wrong_term",
        "A",
        "Insufficient context to determine whether the wrong term reflects a conceptual gap or a vocabulary-only error. Review needed: check whether the student's described procedure is correct. If yes → P. If no → C."
    )

# ── IRRELEVANT ────────────────────────────────────────────────────────────────
def diagnose_irrelevant(row):
    e = exp(row)

    very_short = explain_len(row) < 15
    social = any(p in e for p in [
        "teacher", "class", "we learned", "been learning", "told me",
        "lesson", "remember", "because we"
    ])
    no_math = not any(p in e for p in [
        "add", "subtract", "multipl", "divid", "fraction", "number",
        "equal", "percent", "decimal", "factor", "simplif", "denomin",
        "numer", "ratio", "probab", "variable", "equation"
    ])

    if social:
        return (
            "Irrelevant — social/contextual",
            "M",
            "Student references the classroom context rather than explaining their mathematical reasoning. Undiagnosable: cannot determine the nature of the error from this explanation."
        )
    if very_short or no_math:
        return (
            "Irrelevant — content-free",
            "M",
            "Explanation contains no mathematical content — too short, vague, or off-topic to reveal anything about the student's thinking. Undiagnosable."
        )
    return (
        "Irrelevant — vague",
        "M",
        "Explanation references the problem but provides no diagnostic information about the student's mathematical reasoning. Undiagnosable from written explanation alone."
    )

# ── WRONG_FRACTION ────────────────────────────────────────────────────────────
def diagnose_wrong_fraction(row):
    e = exp(row)

    complement_signals = any(p in e for p in [
        "yellow", "green", "red", "blue", "rest", "remaining",
        "other", "left", "not", "complement"
    ])
    reciprocal_signals = any(p in e for p in [
        "flip", "reciprocal", "invert", "upside", "swap"
    ])
    correct_method = any(p in e for p in [
        "divide by", "times by", "multiply", "fraction of",
        "÷", "×", "of the total"
    ])

    if complement_signals and correct_method:
        return (
            "Wrong_fraction — complement error",
            "P",
            "Student applied the correct procedure (e.g., divide by denominator, multiply by numerator) but to the asked-for fraction rather than its complement. Found the yellow count when asked for green, or vice versa. Procedural: the method is correct, the fraction selection is wrong."
        )
    if reciprocal_signals:
        return (
            "Wrong_fraction — reciprocal confusion",
            "P",
            "Student used the reciprocal of the required fraction. Overlaps with Inversion — check whether the student flipped numerator/denominator (Inversion) or selected a related-but-wrong fraction (Wrong_fraction). Procedural."
        )
    return (
        "Wrong_fraction",
        "P",
        "Student used an incorrect fraction value in an otherwise reasonable procedure. The specific wrong fraction is not identifiable from the explanation alone, but the answer pattern confirms it. Procedural: method intact, fraction input wrong."
    )

# ── INVERSION ─────────────────────────────────────────────────────────────────
def diagnose_inversion(row):
    e = exp(row)

    flip_language = any(p in e for p in [
        "flip", "flipped", "invert", "upside", "turn over",
        "reciprocal", "switch", "swap"
    ])
    kcf_attempt = any(p in e for p in [
        "keep", "change", "flip", "multiply by the reciprocal",
        "divide becomes", "times instead"
    ])

    if kcf_attempt:
        return (
            "Inversion — KCF misapplication",
            "P",
            "Student attempted the keep-change-flip procedure but inverted the wrong fraction (dividend instead of divisor, or both). Part of the fraction division confusion cluster (Inversion + SwapDividend + FlipChange). Procedural: procedure memorized but not correctly applied."
        )
    if flip_language:
        return (
            "Inversion — flip without justification",
            "P",
            "Student describes flipping a fraction without a clear model of why or when to do so. Procedural: the flip is a memorized action applied at the wrong moment or to the wrong fraction."
        )
    return (
        "Inversion",
        "P",
        "Inversion confirmed by answer pattern (answer is the reciprocal of the correct result or uses the reciprocal in computation). No explicit description of the flip in the explanation. Procedural."
    )

# ── MULT ──────────────────────────────────────────────────────────────────────
def diagnose_mult(row):
    e = exp(row)

    both_parts = any(p in e for p in [
        "both", "top and bottom", "numerator and denominator",
        "times both", "multiply both", "all of it", "everything"
    ])
    cross_mult = any(p in e for p in [
        "cross", "across", "diagonal", "opposite"
    ])

    if both_parts:
        return (
            "Mult — multiplied numerator and denominator",
            "P",
            "Student multiplied both the numerator and denominator by the whole number, rather than only the numerator. E.g., 2/3 × 5 → 10/15 instead of 10/3. Procedural: the student over-applied a rule (possibly from equivalent fractions) to a multiplication context."
        )
    if cross_mult:
        return (
            "Mult — cross-multiplication misapplication",
            "P",
            "Student applied cross-multiplication (a procedure for proportions/equations) in a context that required straight multiplication. Procedural: procedure-mixing, not a conceptual gap about multiplication itself."
        )
    return (
        "Mult",
        "P",
        "Multiplication error confirmed by answer pattern. Student used multiplication where a different operation was required, or applied multiplication incorrectly (e.g., to both numerator and denominator). Procedural."
    )

# ── DISPATCH ──────────────────────────────────────────────────────────────────
DIAGNOSERS = {
    "Incomplete":     diagnose_incomplete,
    "Additive":       diagnose_additive,
    "Duplication":    diagnose_duplication,
    "Subtraction":    diagnose_subtraction,
    "Positive":       diagnose_positive,
    "Wrong_term":     diagnose_wrong_term,
    "Irrelevant":     diagnose_irrelevant,
    "Wrong_fraction": diagnose_wrong_fraction,
    "Inversion":      diagnose_inversion,
    "Mult":           diagnose_mult,
}

# ── SAMPLE & DIAGNOSE ─────────────────────────────────────────────────────────
labeled = df[df["Misconception"].isin(TOP10)].copy()

frames = []
for label in TOP10:
    subset = labeled[labeled["Misconception"] == label]
    # Stratify by QuestionId so no single question dominates
    n_questions = subset["QuestionId"].nunique()
    if n_questions >= ROWS_PER_LABEL:
        # One row per question up to 30
        sample = (
            subset.groupby("QuestionId", group_keys=False)
            .sample(n=1, random_state=42)
            .sample(ROWS_PER_LABEL, random_state=42)
        )
    else:
        # Spread 30 rows across available questions proportionally
        per_q = max(1, ROWS_PER_LABEL // n_questions)
        sample = (
            subset
            .groupby("QuestionId", group_keys=False)
            .sample(n=1, random_state=42)
        )
        if len(sample) < ROWS_PER_LABEL:
            # Top up from remaining rows not yet selected
            remaining = subset.drop(sample.index)
            top_up = remaining.sample(
                min(len(remaining), ROWS_PER_LABEL - len(sample)), random_state=42
            )
            sample = pd.concat([sample, top_up])
        sample = sample.head(ROWS_PER_LABEL)

    frames.append(sample)

sample_df = pd.concat(frames).reset_index(drop=True)

# ── APPLY DIAGNOSER ───────────────────────────────────────────────────────────
results = sample_df.apply(lambda row: DIAGNOSERS[row["Misconception"]](row), axis=1)
sample_df["ai_proposed_sublabel"] = results.apply(lambda r: r[0])
sample_df["ai_cp_call"]           = results.apply(lambda r: r[1])
sample_df["ai_rationale"]         = results.apply(lambda r: r[2])

# ── REVIEW COLUMNS ────────────────────────────────────────────────────────────
sample_df["your_review"]          = ""   # ✅ / ✏️ / ❌
sample_df["your_cp_call"]         = ""   # C / P / A / M  (fill for A labels)
sample_df["your_correction"]      = ""   # if ✏️ or ❌: correct label or note
sample_df["your_notes"]           = ""   # optional freeform

# ── COLUMN ORDER ──────────────────────────────────────────────────────────────
out_cols = [
    "row_id",
    "QuestionId",
    "QuestionText",
    "MC_Answer",
    "StudentExplanation",
    "Category",
    "Misconception",
    "ai_proposed_sublabel",
    "ai_cp_call",
    "ai_rationale",
    "your_review",
    "your_cp_call",
    "your_correction",
    "your_notes",
]

sample_df = sample_df[out_cols]

# ── SAVE ──────────────────────────────────────────────────────────────────────
out_path = OUTPUT_DIR / "annotation_sample.csv"
sample_df.to_csv(out_path, index=False)

print("✅ Done.")
print(f"   Output → {out_path}")
print(f"   Total rows: {len(sample_df)}")
print(f"\n   Rows per label:")
print(sample_df["Misconception"].value_counts().to_string())
print(f"\n   AI C/P call distribution:")
print(sample_df["ai_cp_call"].value_counts().to_string())
print(f"\n   Sub-label variety:")
print(sample_df["ai_proposed_sublabel"].value_counts().head(20).to_string())
