# Cleaning Summary Report

**Raw shape:** 36,696 rows × 7 columns

**Columns:** ['row_id', 'QuestionId', 'QuestionText', 'MC_Answer', 'StudentExplanation', 'Category', 'Misconception']

## Column Types
|Column|Type|
|-|-|
|row_id|int64
|QuestionId|int64
|QuestionText|str
|MC_Answer|str
|StudentExplanation|str
|Category|str
|Misconception|str


## Null / Missing Values
||null_count|null_%|
|-|-|-|
|Misconception|26836|73.13


## Literal 'NA' String Counts (not the same as null)


## Duplicates

  - Full duplicate rows: 0

  - Duplicate row_id values: 0

  - Duplicate (QuestionId + MC_Answer + StudentExplanation) combos: 797


## Category Column — Unique Values

|Category|# Unique Values|
|-|-|
|True_Correct|14802
|False_Misconception|9457
|False_Neither|6542
|True_Neither|5265
|True_Misconception|403
|False_Correct|227


## Misconception Column — Value Overview

  - Rows with a misconception label: 9,860

  - Rows without a misconception label (NA): 26,836

  - Unique misconception labels: 35


### Top 20 Most Frequent Misconceptions

|Misconception_clean|Count|
|-|-|
|Incomplete                 |1454
|Additive                   |929
|Duplication                 |704
|Subtraction                 |620
|Positive                    |566
|Wrong_term                  |558
|Irrelevant                  |497
|Wrong_fraction              |418
|Inversion                   |414
|Mult                        |353
|Denominator-only_change     |336
|Whole_numbers_larger        |329
|Adding_across               |307
|WNB                         |299
|Tacking                     |290
|Unknowable                  |282
|Wrong_Fraction              |273
|SwapDividend                |206
|Scale                       |179
|Not_variable                |154


## Questions Referencing Images

  - 8,653 of 36,696 rows (23.6%) reference an image in QuestionText

  ⚠️  Image content is described in text only — no actual image data available.


## Student Explanation Length (characters)

|Statistic|Value|
|-|-|
count    |36696.0
mean        |70.0
std         |38.7
min          |1.0
25%         |43.0
50%         |60.0
75%         |86.0
max        |586.0

  - Explanations under 5 characters: 11 (potentially empty/placeholder)


## Question Coverage

  - Unique QuestionId values: 15

  - Average student responses per question: 2446.4


## Cleaning Actions Taken

  - Replaced literal 'NA' strings in Misconception with NaN

  - Stripped leading/trailing whitespace from all string columns

  - Dropped 0 fully duplicate rows


**Clean shape:** 36,696 rows × 7 columns


---
## ⚠️ Anomalies — Human Review Needed

These findings need your educator judgment before proceeding:


1. **True_Correct rows that also have a Misconception label:** 0


2. **Incorrect answers missing a Misconception label:** 12,034

   → These are errors without a diagnosis. Worth investigating — are they ambiguous cases or data gaps?


3. **Very short student explanations (< 5 chars):** 11

   → Are these meaningful (e.g. '1/3') or placeholder/empty responses to exclude?