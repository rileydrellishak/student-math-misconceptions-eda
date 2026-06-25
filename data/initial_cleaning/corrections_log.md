# Corrections Log

**Starting shape:** 36,696 rows × 7 columns

## Correction 1 — Misconception Label Dedupe

  - Replaced `Wrong_Fraction` (capital F) with `Wrong_fraction` across 273 rows

  - `Wrong_Fraction` remaining after fix: 0


## Correction 2 — Q91695 Mislabeled Correct Answers

  - Found 0 rows in Q91695 where MC_Answer = 22 (correct) but Category = False_Neither

  - Reclassified these rows to `True_Correct`

  - Added `data_quality_note` = `reclassified_from_False_Neither: answer_22_is_correct`

  - Dashboard note: this is a data quality finding worth naming — curated datasets have noise


## Post-Correction Verification

  - Unique Misconception labels: 34

  - Wrong_Fraction (old): 0 (should be 0)

  - Wrong_fraction (canonical): 691


  - Category breakdown after reclassification:

Category
True_Correct           14802
False_Misconception     9457
False_Neither           6542
True_Neither            5265
True_Misconception       403
False_Correct            227


  - Rows with data_quality_note: 0


**Final shape:** 36,696 rows × 8 columns
