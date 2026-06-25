# Misconception Label Codebook

**Dataset:** MAP – Charting Student Math Misunderstandings  
**Phase:** 1, Task 2 — Label Enhancement (Option D workflow)  
**Labels:** 34 canonical · 15 questions · grades 4–8

---

## Purpose

This codebook is the shared reference for the Option D annotation workflow: AI drafts diagnostic labels for sampled responses, and the educator reviews and ratifies (or corrects) each one. Every definition is grounded in actual student explanations from the dataset — not abstract math education theory. The goal is richer labels that support dashboard recommendations, not just frequency tables.

---

## Category System

Each label is assigned a category along two dimensions: **type** (Conceptual vs. Procedural) and **diagnosability** (diagnosable vs. undiagnosable from the written explanation alone).

| Symbol | Category | What it means |
|--------|----------|---------------|
| 🔴 C | **Conceptual** | The student's mental model of a concept is incorrect or incomplete. The error is in what they *believe*, not just how they execute. Requires re-teaching the concept, not just the procedure. **Higher instructional priority** — harder to self-correct and more likely to persist. |
| 🔵 P | **Procedural** | The student's concept is sound but they execute a procedure incorrectly — wrong step, wrong order, wrong operation. Responds well to targeted practice and procedure review. |
| 🟣 A | **Ambiguous** | Could be either Conceptual or Procedural depending on the student's explanation. Sub-categorization is required before instructional recommendations can be made. `Incomplete` and `Wrong_term` are the two primary Ambiguous labels in this dataset. |
| 🟢 M | **Meta / Undiagnosable** | Not diagnosable from the written explanation alone. The label describes explanation quality (irrelevant, unknowable), not the mathematical error. These students need individual probing — group instruction based on written explanations cannot target them. |

---

## Option D Annotation Workflow

For each sampled response, AI proposes an enhanced label and brief rationale. The educator reviews and takes one of three actions:

- ✅ **Accept** — The proposed label and rationale accurately capture the error.
- ✏️ **Modify** — The label is close but needs refinement. Correct the sub-categorization or swap to a better-fitting label and note the reason.
- ❌ **Reject** — The label is wrong. Provide the correct label from this codebook (or flag as a new label if nothing fits). This becomes a training signal for future AI proposals.

> **Ambiguous labels (🟣 A)** require an additional judgment call on the C/P axis. Your rationale for that decision becomes the sub-categorization logic for the dashboard.

---

## Label Definitions

Sorted by frequency (most common first).

---

### Incomplete · 1,454 responses · 14.7% · 🟣 A

**Short definition:** Student begins with correct reasoning but stops before completing the full argument or simplification.

**Full definition:** The student demonstrates partial understanding — they identify the right operation, fraction, or approach — but do not follow through to the final step. The gap may be procedural (don't know the next step) or conceptual (don't know that a next step is needed). This is the dataset's most common label and its broadest: it requires sub-categorization to be instructionally actionable.

**Example from this dataset:** Q31772: *"What fraction of the shape is not shaded? Give your answer in its simplest form."* Student selects 3/9 and writes: *"it is also in its simplest form because you can no longer simplify it."* — The student correctly identified the unshaded fraction but has a gap about what simplest form means.

**Student voice:** *"it is also in its simplest form because you can no longer simplify it."*

**Dashboard note:** Flag for sub-categorization. Three sub-types identified:
1. **Incomplete-direction** — student did not register or ignored the instruction (e.g., "simplest form" in Q31772 — may have seen only "what fraction is not shaded?")
2. **Incomplete-simplification** — saw the instruction but lacks the skill to reduce
3. **Incomplete-procedure** — started the correct method but stopped mid-process

Sub-type (1) has a different instructional response than (2) and (3) — direction-reading is a different intervention than fraction simplification.

---

### Additive · 929 responses · 9.4% · 🔴 C

**Short definition:** Student applies additive reasoning to a multiplicative situation.

**Full definition:** One of the most significant conceptual misconceptions in middle school math. The student treats a multiplicative relationship (scaling, proportionality, multiplication of fractions) as if it were additive (adding or subtracting). This reflects a failure to transition from additive to multiplicative thinking — a well-documented developmental milestone in grades 4–7. Almost always conceptual: the student has a fundamentally incorrect mental model of how quantities relate.

**Example from this dataset:** Q31777: *"3/5 of 120 counters are red. How many red counters?"* Student selects 60 and writes: *"120 divided by 3 is 30. to get it out of 5 i doubled it to get 2 more, which is 60."* — The student is applying additive steps rather than multiplicative scaling (should be 120 × 3/5 = 72).

**Student voice:** *"120 divided by 3 is 30. to get it out of 5 i doubled it to get 2 more, which is 60."*

**Dashboard note:** High instructional priority. Additive errors are resistant to quick fixes — they require rebuilding the concept of multiplicative relationships, often through ratio tables or double number lines. Connect to `Scale` in the dashboard as a related cluster.

---

### Duplication · 704 responses · 7.1% · 🔵 P

**Short definition:** Student repeats or copies part of the problem rather than computing a new value.

**Full definition:** The student's answer is not the result of a computation but a verbatim or near-verbatim repetition of something already present in the problem — often the numerator, denominator, or a given number. Usually procedural: the student doesn't know what to do, so they echo what they see. Can occasionally signal a conceptual misunderstanding about what the question is asking.

**Example from this dataset:** Q31778: *A/10 = 9/15. What is the value of A?* Student selects A = 9 and writes: *"because they are the same fraction."* — The student duplicated the numerator 9 rather than computing the equivalent value (6).

**Student voice:** *"because they are the same fraction."*

**Dashboard note:** Often indicates the student has no entry point into the problem — they are guessing with what is available. Instructionally: verify that foundational prerequisite skills are in place before re-teaching the target concept.

---

### Subtraction · 620 responses · 6.3% · 🔵 P

**Short definition:** Student uses subtraction when a different operation (usually multiplication or division) is required.

**Full definition:** The student defaults to subtraction in a context that requires multiplication, division, or proportional reasoning. Usually procedural — the student may understand the concept partially but reaches for a familiar operation. Often overlaps with Additive errors in that the student is applying simpler arithmetic to a more complex situation.

**Example from this dataset:** Q31777: Student finds the fraction of red counters by subtracting rather than multiplying: *"i found half of it and then halfled it again"* — applying repeated halving (subtraction-adjacent) instead of computing 3/5 × 120.

**Student voice:** *"i found half of it and then halfled it again and finally i had this answer."*

**Dashboard note:** Check whether the student understands which operation the problem is calling for. If yes → procedural fix. If no (they thought this was a subtraction problem) → conceptual re-teaching needed. This label sits close to the C/P boundary.

---

### Positive · 566 responses · 5.7% · 🔴 C

**Short definition:** Student ignores or incorrectly handles negative signs, treating negative quantities as positive.

**Full definition:** The student strips the negative sign from a value and operates on the absolute value instead. Conceptual misunderstanding about how negative numbers behave — particularly common with negative-minus-negative operations, where students often confuse the double negative and apply it incorrectly.

**Example from this dataset:** Q89443: *(-8) - (-5) = ?* Student selects -13 and explains: *"if you add to something, it goes down in negatives."* — treating -(-5) as if it remains -5 rather than becoming +5, producing -8 + (-5) = -13 instead of -8 + 5 = -3.

**Student voice:** *"if you add to something, it goes down in negatives, and take away goes up."*

**Dashboard note:** Conceptual priority. Number line models and temperature/debt contexts are the most effective re-teaching tools. Abstract rule memorization ("two negatives make a positive") often fails without the conceptual anchor.

---

### Wrong_term · 558 responses · 5.7% · 🟣 A

**Short definition:** Student uses an incorrect mathematical term or confuses two related but distinct terms.

**Full definition:** The student demonstrates knowledge of a concept but applies the wrong vocabulary label to it, or confuses two related terms (e.g., numerator/denominator, mean/median, factor/multiple). Can be either conceptual (genuinely conflates the terms) or superficially procedural (knows the concept, uses wrong word). The distinction matters: wrong vocabulary with correct procedure is a different instructional target than wrong vocabulary signaling wrong concept.

**Example from this dataset:** Q31778: Student writes *"The numerator and denominator must be the same"* — confusing the rule for equivalent fractions with a rule for fractions equal to 1, or for simplification in addition contexts.

**Student voice:** *"The numerator and denominator must be the same."*

**Dashboard note:** Investigate whether the wrong term accompanies a correct or incorrect procedure. Vocabulary mismatch with correct work = low priority fix. Vocabulary mismatch with incorrect work = may signal deeper conceptual confusion.

---

### Irrelevant · 497 responses · 5.0% · 🟢 M

**Short definition:** Student explanation provides no meaningful diagnostic information about their mathematical thinking.

**Full definition:** The student's explanation is either content-free ("I just knew it," "it looked right"), socially oriented ("my teacher told me"), or entirely off-topic. Meta-category: it tells us about explanation quality, not about the nature of the mathematical error. Cannot be classified as procedural or conceptual because there is nothing to analyze.

**Example from this dataset:** Q31774: *Calculate 1/2 ÷ 6.* Student selects 1/3 and writes: *"i think it's because we've been learning about these things, and i have an answer."* — completely uninformative about how they arrived at their answer.

**Student voice:** *"I just used my comb sens" / "i'm not too sure so i went with..."*

**Dashboard note:** Cannot be used for instructional targeting. Group with `Unknowable` as "undiagnosable" in the dashboard and note the prevalence as a data quality finding. These students need one-on-one probing, not group instruction based on written explanations.

---

### Wrong_fraction · 691 responses · 7.0% · 🔵 P

**Short definition:** Student identifies the correct operation or approach but applies it to the wrong fraction — often the complement or reciprocal.

**Full definition:** The student's procedure is largely intact but they work with the wrong fraction — most often confusing a fraction with its complement (1 - x) or its reciprocal. Primarily procedural: the student has a working method but misidentifies which fraction to input. Note: deduplicated from `Wrong_Fraction` and `Wrong_fraction` in the raw dataset.

**Example from this dataset:** Q33471: *A bag has 24 balls. 3/8 are yellow. How many are green?* Student correctly computes 3/8 × 24 = 9 but selects 9 as the answer — having found the yellow count rather than using 5/8 or subtracting from 24.

**Student voice:** *"divide by the bottom and times by the top"*

**Dashboard note:** Distinguish from `Inversion` (specifically about flipping numerator/denominator). `Wrong_fraction` is broader — any use of the wrong fraction value, including complement errors. High frequency suggests systematic confusion about which fraction the question is asking for.

---

### Inversion · 414 responses · 4.2% · 🔵 P

**Short definition:** Student flips the numerator and denominator of a fraction (uses the reciprocal when they should not).

**Full definition:** The student inverts a fraction — swapping numerator and denominator — when the problem does not call for it. Common in fraction division contexts where "flip and multiply" is a learned procedure. Students who have memorized the rule without understanding it sometimes invert at the wrong moment, or invert the wrong fraction.

**Example from this dataset:** Q31774: *Calculate 1/2 ÷ 6.* Student selects 6/2 (= 3), having inverted 1/2 to 2/1 and then multiplied by 6/1, rather than multiplying 1/2 by 1/6.

**Student voice:** *"If we flip it over we would get 3 if we keep changing."*

**Dashboard note:** Closely related to `FlipChange` and `SwapDividend` — consider grouping these three in the dashboard as a **fraction division confusion cluster**. All three stem from misapplication of the flip-and-multiply procedure.

---

### Mult · 353 responses · 3.6% · 🔵 P

**Short definition:** Student uses multiplication when a different operation (addition, subtraction, or division) is required.

**Full definition:** The inverse of the Subtraction/Additive error family: the student reaches for multiplication when the problem calls for something else. Often occurs in fraction contexts where the student has learned to multiply fractions but over-generalizes — multiplying denominators when adding fractions, for example.

**Example from this dataset:** Q32833: *Calculate 2/3 × 5.* Student selects 10/15, having multiplied both numerator and denominator by 5 (2×5=10, 3×5=15) rather than only the numerator (2×5=10, denominator stays 3).

**Student voice:** *"5 turned into 5/1 then i multiplied both together."*

**Dashboard note:** Look for co-occurrence with `Adding_across` and `Denominator-only_change` — these three often appear together on fraction arithmetic questions and form a natural **fraction operation errors cluster**.

---

### Denominator-only_change · 336 responses · 3.4% · 🔴 C

**Short definition:** Student changes only the denominator when finding equivalent fractions, leaving the numerator unchanged (or vice versa).

**Full definition:** The student understands that equivalent fractions require changing the denominator but does not apply the same scaling factor to the numerator. Conceptual: the student has an incomplete model of equivalence. They may know the rule "change the bottom" without understanding that equivalence requires proportional scaling of both parts.

**Example from this dataset:** Q31778: *A/10 = 9/15.* Student selects A = 9, reasoning *"Thr denominator does not have to be the same."* They see 9 in the problem and copy it, not recognizing that 9/10 ≠ 9/15.

**Student voice:** *"Thr denominator does not have to be the same."*

**Dashboard note:** High conceptual priority. Equivalent fractions are foundational for fraction arithmetic, ratios, and proportional reasoning. Students with this misconception cannot reliably add unlike fractions or set up proportions.

---

### Whole_numbers_larger · 329 responses · 3.3% · 🔴 C

**Short definition:** Student applies whole-number magnitude intuition to fractions or decimals — assuming larger digits always mean larger values.

**Full definition:** The student believes a fraction or decimal is larger simply because its digits are larger, without accounting for the part-whole relationship. For fractions: 3/8 > 3/5 because 8 > 5. For decimals: 6.079 > 6.2 because 79 > 2. Rooted in the transfer of whole-number thinking to rational numbers — one of the most researched and persistent errors in elementary and middle school math.

**Example from this dataset:** Q32835: *Which number is greatest?* Student selects 6.079 and writes: *"because the 100ths and 10ths are larger"* — reasoning that 79 as a number is bigger than 2.

**Student voice:** *"I think c because if you look at the 100ths it is 9. And when you go to see the 10th's, it'll be 7."*

**Dashboard note:** Part of the **Whole Number Bias cluster** alongside `WNB`, `Longer_is_bigger`, and `Shorter_is_bigger`. All four are manifestations of the same root cause: whole-number intuitions that haven't been restructured for rational numbers.

---

### Adding_across · 307 responses · 3.1% · 🔴 C

**Short definition:** Student adds numerators and denominators independently when adding fractions (e.g., 1/3 + 2/5 = 3/8).

**Full definition:** One of the most well-known fraction misconceptions. The student treats a fraction as two independent whole numbers and adds across both: (a/b) + (c/d) = (a+c)/(b+d). Conceptual: the student has a misunderstanding of what a fraction represents as a part-whole ratio. They have not internalized that the denominator names the unit — and units can't simply be added.

**Example from this dataset:** 1/3 + 2/5 = 3/8. The student adds numerators (1+2=3) and denominators (3+5=8) separately, treating the fraction as two independent integers rather than as a single rational number.

**Student voice:** *"i added the top numbers and the bottom numbers"*

**Dashboard note:** One of the highest-priority conceptual misconceptions in the dataset. This error prevents any reliable fraction arithmetic. Research suggests fraction bars and area models are more effective than procedural re-teaching.

---

### WNB · 299 responses · 3.0% · 🔴 C

**Short definition:** Whole Number Bias — student applies whole-number reasoning to fractions or decimals, treating the numerator or denominator as independent whole numbers rather than as parts of a ratio.

**Full definition:** Whole Number Bias (WNB) is a well-documented conceptual phenomenon in which students whose number sense was built on whole integers have not yet restructured that understanding for rational numbers. The student treats the parts of a fraction as independent integers rather than as a relational quantity. This produces errors like believing 3/9 is already in simplest form ("9 is bigger than 3 so it's correct"), or that 1/8 > 1/5 because 8 > 5. WNB underlies multiple labels in this dataset — including `Whole_numbers_larger`, `Longer_is_bigger`, and `Shorter_is_bigger` — making it one of the most structurally important conceptual categories.

**Example from this dataset:** Q31772: Student selects 3/9 as the simplest form of the unshaded fraction, writing *"it is also in its simplest form because you can no longer simplify it."* — applying whole-number intuition (9 is larger than 3, so the fraction feels "as reduced as possible") rather than testing divisibility of both parts by a common factor.

**Student voice:** *"it is also in its simplest form because you can no longer simplify it."*

**Dashboard note:** High conceptual priority. WNB is the root cause of a **Whole Number Bias cluster**: `WNB` + `Whole_numbers_larger` + `Longer_is_bigger` + `Shorter_is_bigger`. Research base: Ni & Zhou (2005), Vamvakoussi & Vosniadou — one of the most studied misconceptions in rational number development.

---

### Tacking · 290 responses · 2.9% · 🔵 P

**Short definition:** Student appends an operation or value without integrating it into the calculation — adding a step that doesn't connect to the rest.

**Full definition:** The student performs a correct initial calculation but then adds an additional operation that was not required, disconnecting from the original problem. The extra step is procedurally "tacked on" without logical justification — often borrowed from a related procedure the student is confusing this problem with.

**Example from this dataset:** Q31774: *Calculate 1/2 ÷ 6.* Student writes: *"1/2 divided by 6 = 6/3 divide both by 3 = 3/1, but switch it around would equal 1/3."* — performing multiple unjustified inversions.

**Student voice:** *"i think this because, 1/2 divided by 6 = 6/3 divide both by 3 = 3/1, but switch it around would equal 1/3."*

**Dashboard note:** Often signals procedure-mixing: the student is blending two procedures (e.g., dividing fractions and simplifying) without a clear model of when each step applies.

---

### Unknowable · 282 responses · 2.9% · 🟢 M

**Short definition:** Student explanation is present but does not contain enough information to diagnose the nature of the error.

**Full definition:** Unlike `Irrelevant` (where the explanation is clearly off-topic), Unknowable responses contain mathematical language or partial reasoning that appears related to the problem, but is too vague, incoherent, or incomplete to determine whether the error is conceptual or procedural. The student is attempting to explain but the explanation cannot be decoded.

**Example from this dataset:** Q104665: *3 people take 192 hours to build a wall. How long for 12 people?* Student selects 64 hours and writes: *"12 x 64 divuded by 4 is"* — trails off. The student appears to be computing something, but the expression is uninterpretable.

**Student voice:** *"as it cone to around 600 dicided by 5 gets you closest to that"*

**Dashboard note:** Group with `Irrelevant` as "undiagnosable" in the dashboard. Note that Unknowable responses often come from students who are guessing and reverse-engineering an explanation — a different instructional signal than a student who is genuinely confused.

---

### SwapDividend · 206 responses · 2.1% · 🔵 P

**Short definition:** Student swaps the dividend and divisor, computing the division in the wrong order.

**Full definition:** The student performs a division correctly in terms of procedure but reverses which quantity is being divided by which. Procedural: the student knows how to divide but has an incorrect model of the order of operations in division. Common in contexts where division is presented abstractly rather than in a story structure that clarifies which quantity is being shared.

**Example from this dataset:** Q31774: *Calculate 1/2 ÷ 6.* Student computes 6 ÷ (1/2) = 12 instead of (1/2) ÷ 6 = 1/12.

**Student voice:** *"one half divided by 6 is not the same as 6 divided in half"*

**Dashboard note:** Related to `Inversion` — both involve fraction division errors. Consider grouping `SwapDividend` + `Inversion` + `FlipChange` as a **fraction division confusion cluster** in the dashboard.

---

### Scale · 179 responses · 1.8% · 🔴 C

**Short definition:** Student does not scale both parts of a relationship proportionally — applies a scale factor to only one quantity.

**Full definition:** In ratio, proportion, or scale factor problems, the student recognizes that a scaling relationship exists but applies the factor to only one side of the equation or ratio. Conceptual: the student understands "multiply by something" but not "multiply everything by the same thing."

**Example from this dataset:** Q104665: *3 people, 192 hours. How long for 12 people?* Student recognizes that 12 is 4 times 3 — correct scaling identification — but applies the division to only one part of the relationship, or applies the wrong operation (×4 instead of ÷4).

**Student voice:** *"they have 9 people more so you divide"*

**Dashboard note:** Connects to `Additive` — both are proportional reasoning errors. Scale errors often emerge at the additive-to-multiplicative transition. Consider a **proportional reasoning cluster**: `Additive` + `Scale`.

---

### Not_variable · 154 responses · 1.6% · 🔴 C

**Short definition:** Student treats an algebraic variable as a specific number rather than an unknown quantity.

**Full definition:** The student substitutes a literal value (often from the problem) for the variable rather than solving for it. Foundational algebraic misconception: the student has not developed the concept of a variable as a placeholder for an unknown. Variables are seen as abbreviations or shorthand for a specific number the student selects, often from recognizing something "nice" in the problem.

**Example from this dataset:** Q32829: *2y = 24. What is the value of y?* Student selects y = 4 and writes: *"24 is also the same number as 24, so it has to be equal."* — The student verified that writing "24" for y makes the statement 24 = 24 look true.

**Student voice:** *"24 is also thr same number as 24, so it has to be equal."*

**Dashboard note:** One of the most significant conceptual barriers to algebra readiness. High instructional priority for grades 6–8. Often appears alongside `Adding_terms` — students who don't understand variables also struggle with why you can't add unlike terms.

---

### Firstterm · 107 responses · 1.1% · 🔵 P

**Short definition:** Student uses only the first term or initial value in a sequence or expression, ignoring subsequent terms or the rule.

**Full definition:** The student anchors on the first number or term in a sequence, expression, or pattern and either repeats it, treats it as the answer, or fails to apply the rule to later terms. Primarily procedural — the student may understand the first step but does not continue applying the rule consistently.

**Example from this dataset:** Q91695: *Dot pattern growing by 4 each time (Pattern 1: 6, Pattern 2: 10...). How many dots in Pattern 6?* Student responds with a value based on Pattern 1 rather than continuing the +4 rule to Pattern 6 (= 26).

**Student voice:** *"i know because the last pattern would have 6 rows"*

**Dashboard note:** Common in pattern and sequence questions. Check whether the student understands the difference between the term number and the term value — this confusion is often the root cause.

---

### Adding_terms · 97 responses · 1.0% · 🔴 C

**Short definition:** Student adds algebraic terms that cannot be combined — treats unlike terms as like terms.

**Full definition:** The student combines terms with different variables or different powers as if they were the same — simplifying 3x + 4 to 7x, or x² + x to x³. Reflects a conceptual misunderstanding of what "like terms" means: the student treats addition as universally applicable regardless of what is being added.

**Example from this dataset:** Q31778 context: Student simplifies an expression by adding a coefficient and a constant, treating them as the same type of quantity.

**Student voice:** *"therefore, the answer is 7"* (for an expression where 3 and a variable term were added)

**Dashboard note:** Foundational algebra error that blocks simplification of all polynomial expressions. Often appears alongside `Not_variable`.

---

### Multiplying_by_4 · 96 responses · 1.0% · 🔵 P

**Short definition:** Student multiplies by 4 in a context that requires a different scalar (typically dividing by 4 or using a different factor).

**Full definition:** A specific procedural error appearing primarily in proportion or fraction-of-a-quantity questions. The student correctly identifies that 4 is a relevant number in the problem but applies multiplication instead of division, or uses 4 as the scale factor when the correct factor is something else.

**Example from this dataset:** Q104665: *3 people, 192 hours. How long for 12 people?* Student who should divide by 4 instead multiplies: 192 × 4 = 768.

**Student voice:** *"64 times 1 is 768 times 7 then you times by 12 which is 12 times 64"*

**Dashboard note:** May be concentrated in 1–2 specific questions in this dataset. Check per-question distribution before treating as a generalizable pattern.

---

### FlipChange · 78 responses · 0.8% · 🔵 P

**Short definition:** Student misapplies the "keep, change, flip" procedure for fraction division — flips the wrong fraction or applies it at the wrong moment.

**Full definition:** The student knows the KCF procedure for dividing fractions but applies it incorrectly: flipping the wrong fraction, applying the change to the wrong operation, or flipping when they should not. Procedural: the student has memorized a procedure without understanding why it works. Related to `Inversion` and `SwapDividend`.

**Example from this dataset:** Q31774: *Calculate 1/2 ÷ 6.* Student should keep 1/2, change ÷ to ×, flip 6 to 1/6. Instead, student flips 1/2 to 2/1 and multiplies: 2/1 × 6 = 12.

**Student voice:** *"if you flip it over and multiply you get the answer"*

**Dashboard note:** KCF errors strongly signal that the student learned a procedure without conceptual grounding. Teaching fraction division through proportional reasoning (how many 1/6s fit in 1/2?) before introducing KCF reduces these errors. Part of the **fraction division confusion cluster**: `FlipChange` + `Inversion` + `SwapDividend`.

---

### Division · 63 responses · 0.6% · 🔵 P

**Short definition:** Student uses division when a different operation is required, or performs a division incorrectly in a fraction/proportion context.

**Full definition:** The student defaults to division in a situation requiring multiplication, addition, or a proportional approach. Or correctly identifies that division is needed but performs it in the wrong direction or with the wrong values. Distinct from `SwapDividend` (which specifically involves reversing dividend and divisor) — `Division` is the broader catch-all for division-related procedural errors.

**Example from this dataset:** Q32833: *Calculate 2/3 × 5.* Student divides rather than multiplies: *"when you divide the number on the bottom by 5, it will be five times larger."*

**Student voice:** *"when you divide the number on the bottom by 5, it will be five times larger"*

**Dashboard note:** Low frequency (63 cases). May co-occur with `Mult` as complementary errors on the same fraction multiplication questions.

---

### Definition · 54 responses · 0.5% · 🔴 C

**Short definition:** Student misunderstands or misapplies the definition of a key mathematical term.

**Full definition:** The student has an incorrect or incomplete definition of a mathematical concept and applies their (wrong) definition consistently. Different from `Wrong_term` (where the student uses the wrong word for a correctly understood concept) — in Definition errors, the student's underlying concept is wrong. They believe they know what the term means, but their belief is incorrect.

**Example from this dataset:** Q31778: *A/10 = 9/15.* Student writes *"The numerator and denominator must be the same"* — applying a rule that is true for fractions equal to 1 (or for simplification) but not for equivalent fractions in general.

**Student voice:** *"The numerator and denominator must be the same."*

**Dashboard note:** Definition errors require explicit vocabulary instruction paired with multiple examples and non-examples. A student who "knows" the wrong definition is harder to reach than one who has no definition at all.

---

### Interior · 50 responses · 0.5% · 🔴 C

**Short definition:** Student focuses on the interior or internal elements of a geometric figure rather than the whole or the relationship being asked about.

**Full definition:** In geometry contexts, the student fixates on a part of the figure (interior region, interior angle, inside elements) when the question asks about the whole or a different part. Conceptual: the student has an incorrect mental model of which elements are relevant to the question.

**Example from this dataset:** Q91695: *Dot pattern question.* Several students counted only interior or unfilled dots rather than all dots in the pattern arrangement.

**Student voice:** *"you add an extra dot at the bottom and don't fill in the last two dots"*

**Dashboard note:** Relatively rare (50 cases). Most likely concentrated in geometry and pattern arrangement questions.

---

### Longer_is_bigger · 24 responses · 0.2% · 🔴 C

**Short definition:** Student believes a decimal with more digits after the decimal point is always larger.

**Full definition:** A specific manifestation of Whole Number Bias: the student believes that the length of a decimal representation correlates directly with its magnitude. 6.0001 > 6.2 because 6.0001 has more digits. The student does not understand that place value position (tenths, hundredths, thousandths) determines size, not the count of digits.

**Example from this dataset:** Q32835: *Which number is greatest?* Student selects 6.0001 and writes: *"i think d because it has more thousandths than any of the other numbers."*

**Student voice:** *"i think d because it has more thousandths than any of the other numbers."*

**Dashboard note:** Part of the **Whole Number Bias cluster**: `WNB` + `Whole_numbers_larger` + `Longer_is_bigger` + `Shorter_is_bigger`. Rare but high-impact — students with this error cannot reliably compare or order decimals.

---

### Shorter_is_bigger · 23 responses · 0.2% · 🔴 C

**Short definition:** Student believes a decimal with fewer digits is always larger — the inverse of Longer_is_bigger.

**Full definition:** The student has internalized a "shorter = bigger" rule for decimals, possibly over-generalizing from the correct intuition that fractions with smaller denominators are larger (1/2 > 1/8). Transferred to decimals, this becomes an inconsistently applied rule that produces correct answers in some cases (6.2 > 6.09) and incorrect ones in others (6 > 6.9).

**Example from this dataset:** Q32835: Student selects 6 as the greatest number, reasoning *"because it is bigger then all the decimal numbers."*

**Student voice:** *"because it is bigger then all the decimal numbers"*

**Dashboard note:** Conceptually interesting — this student may get some decimal comparison problems right for the wrong reason. Part of the **Whole Number Bias cluster**.

---

### Base_rate · 23 responses · 0.2% · 🔴 C

**Short definition:** Student ignores the base rate or total quantity when computing a proportion or probability.

**Full definition:** The student focuses on a part without relating it to the whole. In probability problems, this manifests as ignoring total outcomes and focusing on favorable ones. In proportion problems, as computing a partial value without accounting for the total. Conceptual: the student has not internalized that all proportional reasoning requires both a part and a whole.

**Example from this dataset:** Q109465: *Probability of an event is 0.9.* Student selects "Unlikely" and writes: *"there is just a 1 in 10,000 chance of this happening"* — interpreting 0.9 as 0.9% rather than 90%, a base-rate confusion between decimal probability and percentage.

**Student voice:** *"there is just a 1 in 10,000 chance of this happening."*

**Dashboard note:** The 0.9-as-unlikely error is a striking cascade failure: a decimal place-value misread produces a completely wrong probability judgment. Connect to `Certainty` in the dashboard as a **probability scale cluster**.

---

### Inverse_operation · 21 responses · 0.2% · 🔵 P

**Short definition:** Student applies the inverse of the required operation.

**Full definition:** The student correctly identifies the operation family (multiplication/division or addition/subtraction) but applies the inverse: divides when they should multiply, subtracts when they should add. Usually procedural — the student's equation-solving instinct (undo what's there) fires in the wrong direction.

**Example from this dataset:** Q32829: *2y = 24.* Student multiplies both sides by 2 (getting 4y = 48) rather than dividing both sides by 2.

**Student voice:** *"24 divided by 12 equals 12. The answer will be 12."*

**Dashboard note:** Low frequency (21 cases). Likely concentrated in equation-solving questions.

---

### Certainty · 18 responses · 0.2% · 🔴 C

**Short definition:** Student conflates high probability with certainty, or treats any non-zero probability as certain.

**Full definition:** The student does not distinguish between "very likely" and "certain" on the probability scale — either selecting "Certain" for probabilities like 0.9, or treating the absence of impossibility as certainty. Conceptual: the student has not internalized that probability exists on a continuous scale between 0 (impossible) and 1 (certain).

**Example from this dataset:** Q109465: *Probability = 0.9.* Student selects "Certain" because 0.9 is almost 1.0 and 1.0 is certain.

**Student voice:** *"1.0 is certainty, so if it is likely that must be a large number."*

**Dashboard note:** Related to `Base_rate` — both are probability scale errors. Together these suggest that probability as a continuous numerical concept (rather than a verbal category) is a shared instructional gap. **Probability scale cluster**: `Base_rate` + `Certainty`.

---

### Incorrect_equivalent_fraction_addition · 9 responses · 0.1% · 🔴 C

**Short definition:** Student creates a common denominator when adding fractions but scales the denominator without proportionally scaling the numerator.

**Full definition:** A specific sub-type of `Denominator-only_change`, specific to fraction addition contexts. The student recognizes that a common denominator is needed and finds one, but when converting, changes only the denominator — or applies the wrong scaling factor to the numerator — producing an incorrect equivalent fraction that looks procedurally reasonable.

**Example from this dataset:** For 1/3 + 2/5: Student correctly identifies 15 as a common denominator, writes 1/15 + 2/15 = 3/15 (changed denominators to 15 but didn't scale numerators), instead of the correct 5/15 + 6/15 = 11/15.

**Student voice:** *"i changed the bottom to 15 to make it even"*

**Dashboard note:** Very rare (9 cases). Consider merging with `Denominator-only_change` in dashboard display, noting it as a fraction-addition-specific variant.

---

### Wrong_Operation · 6 responses · 0.1% · 🔵 P

**Short definition:** Student selects a completely incorrect operation with no apparent connection to the correct approach.

**Full definition:** The student applies an operation that is not adjacent to, or a recognizable mis-application of, the correct one. Distinct from `Subtraction`, `Mult`, and `Division` (which describe specific wrong-operation patterns) — `Wrong_Operation` is the catch-all for cases where the operation chosen is entirely off. Very rare (6 cases) — may indicate labeling errors or truly outlier responses.

**Example from this dataset:** Insufficient data (6 cases) to establish a clear pattern.

**Student voice:** *(insufficient data — only 6 cases)*

**Dashboard note:** Too rare to display independently. Recommend grouping with `Irrelevant`/`Unknowable` as "unclassifiable" or noting in a data quality footnote.

---

## Dashboard Clusters

These groupings surface in the EDA and should be reflected in the dashboard's recommendation layer.

| Cluster | Labels | Root cause |
|---------|--------|------------|
| **Whole Number Bias** | `WNB`, `Whole_numbers_larger`, `Longer_is_bigger`, `Shorter_is_bigger` | Whole-number intuitions not restructured for rational numbers |
| **Fraction Division Confusion** | `Inversion`, `SwapDividend`, `FlipChange` | Misapplication of keep-change-flip without conceptual grounding |
| **Fraction Operation Errors** | `Adding_across`, `Denominator-only_change`, `Mult`, `Incorrect_equivalent_fraction_addition` | Treating numerator and denominator as independent integers |
| **Proportional Reasoning** | `Additive`, `Scale` | Additive-to-multiplicative transition failure |
| **Algebra Readiness** | `Not_variable`, `Adding_terms` | Variable concept not yet developed |
| **Probability Scale** | `Base_rate`, `Certainty` | Probability as verbal category rather than continuous numeric scale |
| **Undiagnosable** | `Irrelevant`, `Unknowable`, `Wrong_Operation` | Insufficient explanation to diagnose — needs individual probing |

---

*Last updated: Phase 1, Task 2 · Option D workflow · June 2026*
