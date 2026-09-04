# CGM Analysis Protocol v1.0

## Purpose

This protocol defines the agreed workflow for Darren's ongoing Dexcom and insulin-to-carb ratio (ICR) reviews. It is intended to keep future analysis consistent, avoid duplicate meal logging, and make each review useful for discussion with the diabetes team.

## Current clinical context

- Diabetes context: Type 3c diabetes post-Whipple.
- Current CGM baseline: Dexcom is the primary baseline. Libre is archived historical reference only unless pre-Dexcom comparison is specifically requested.
- Basal insulin: Lantus 20 units daily, usually taken on waking.
- Current fast-acting ICR benchmark: 1 unit per 15 g carbohydrate (1:15).
- Bolus timing: usually at eating time because of slower post-Whipple digestion. Do not assume a standard 20-minute pre-bolus is automatically appropriate.
- High-fat and high-carbohydrate meals may cause delayed or extended glucose rises, often beyond Dexcom's 4-hour meal window.

## Required files for every full review

A full CGM and ICR review requires all three files:

1. Dexcom Clarity PDF
   - Overall glucose metrics
   - GMI
   - Time in Range
   - AGP
   - Daily and hourly patterns
   - Comparison periods

2. Dexcom CSV export
   - Detailed glucose trace
   - Post-meal peak
   - Time above 10 mmol/L
   - Time to return below 10 mmol/L
   - Glucose at approximately 2, 4 and 6 hours
   - Overnight patterns and variability

3. ICR Meal Dashboard CSV
   - Primary source of truth for structured meal and dose information
   - Meal description and type
   - Carbohydrate grams
   - Fat level or actual fat grams
   - ICR used
   - Calculated dose
   - Actual insulin taken
   - Bolus timing
   - Notes and confounders

## Hard workflow rule

Do not start the full review unless all three files are present.

If only one or two files are uploaded, stop and remind Darren which file is missing before processing the review.

Do not perform detailed meal-by-meal or ICR analysis from Dexcom alone.

The ICR Meal Dashboard CSV is the primary meal source. Do not double-count meals by treating Dexcom meal entries as a second independent meal log when the app CSV is available.

## Unmatched fast-acting insulin rule

If Dexcom contains a fast-acting insulin entry but there is no matching ICR Meal Dashboard meal/dose entry, treat it as:

> Estimated / best-guess dose - meal nutrition was not known well enough to log accurately, commonly because restaurant or takeaway nutritional information was unavailable.

For these unmatched doses:

- Include them in the overall insulin and glucose picture.
- They may be mentioned when the glucose outcome is notable.
- Do not reverse-engineer a carbohydrate amount or ICR from them.
- Do not use them as evidence that 1:15 is too strong or too weak.
- Keep them separate from the clean meal set used for ICR decisions.

## How the three sources are combined

- ICR Meal Dashboard CSV explains what was eaten and how it was dosed.
- Dexcom CSV shows the glucose outcome after that meal.
- Dexcom PDF provides the wider clinical context and trend view.

Meal records should be matched primarily by timestamp. Dexcom meal notes can be used as a cross-check or for extra context, but not as a duplicate source of meal events.

## Meal logging standard

Continue adding top-line information to Dexcom where useful, but use the ICR Meal Dashboard for structured meal tracking.

For the ICR Meal Dashboard:

- Carbohydrate grams: record as accurately as practical.
- Fat grams: if available from packaging or reliable nutrition information, enter the actual fat grams.
- If exact fat grams are not known, leave the grams blank and use the fat-level dropdown as the best estimate.
- Meal description: use a short recognisable description.
- Meal type: choose the most appropriate category.
- Actual insulin: record what was really taken, not just the calculated amount.
- Bolus timing: record timing relative to the meal.
- Notes: use for relevant context such as exercise, alcohol, Creon, illness, ketones, unusual meal timing, new/faulty sensor, or other confounders.

Rows marked TEST ONLY, TEST 2, or clearly identified as test records must be excluded from real ICR and meal-performance analysis.

## ICR review method

The current 1:15 ICR is a benchmark to test, not an assumption that it is automatically correct.

For each suitable meal, assess:

- Starting glucose
- Carbohydrate grams
- Fat grams or fat category
- Meal type
- ICR used
- Calculated insulin dose
- Actual insulin taken
- Bolus timing
- Peak glucose
- Rise from starting glucose
- Time above 10 mmol/L
- Time to return below 10 mmol/L
- Approximate 2-hour glucose
- Approximate 4-hour glucose
- Approximate 6-hour glucose
- Whether there is a late rise
- Whether a low occurs after the meal
- Relevant activity, alcohol, illness, sensor issues or other confounders

The aim is to determine whether 1:15:

- Works well as the everyday baseline
- Looks too weak for ordinary meals
- Looks too strong
- Works for normal meals but needs a different strategy for high-fat/high-carb meals
- Appears to vary by meal type, carbohydrate amount or time of day

Do not recommend a blanket move to a stronger ratio such as 1:10 simply because some meals remain above 10 mmol/L. Distinguish between inadequate ICR, delayed digestion, high-fat effects, timing mismatch and correction/stacking issues.

Any insulin-setting changes should be treated as matters to discuss with the diabetes team rather than instructions for self-adjustment.

## Sensor-error rule

Documented suspected sensor errors should not be allowed to distort trend conclusions. When a Dexcom low is clearly contradicted by a finger-prick and is documented as a faulty sensor/compression issue, flag it as a sensor exception rather than treating it as a genuine hypo for interpretation.

## After every complete 3-file review

Once all three files have been processed:

1. Produce the full combined review.
2. Compare the new period with relevant previous uploads.
3. Review whether the current 1:15 ICR is still supported.
4. Update the live app's latest CGM progress summary.
5. Add/update the review timeline.
6. Update "What I've learned about Darren's diabetes" only where the evidence genuinely supports a change.
7. Keep the Clinical Goals section tied to real Dexcom/AGP targets rather than an invented score.
8. Update version history if the app itself changes.
9. Send Darren a concise email summary with a one-line coach summary, headline metrics, progress, ICR verdict, what is working, what to watch and any sensor/data exceptions.

## Evidence-status rule for learned insights

Statements in "What I've learned about Darren's diabetes" should carry one of these statuses:

- PROVEN REPEATEDLY - supported consistently across repeated clean data.
- LIKELY - supported by the current pattern but still needs more observations.
- UNDER INVESTIGATION - a plausible pattern that does not yet have enough evidence.
- ANALYSIS RULE - an agreed interpretation rule rather than a biological conclusion.

Do not promote a statement to PROVEN REPEATEDLY merely because it sounds plausible. New data can strengthen, weaken or remove a prior conclusion.

## Backups and rollback

Before a material app release, preserve the previous stable version in GitHub as a rollback branch. GitHub commit history plus the rollback branch protects the code, while Supabase and CSV export provide separate recovery paths for meal data.

## Pre-bolus timing evidence
From app v2.5.0 onward, include the recorded CGM trend arrow in suitable meal reviews. Analyse starting glucose and trend together with meal type, carbohydrate, fat and actual bolus timing. Do not convert a single social-media formula into a personalised timing rule. Build repeated clean evidence first, then flag any consistent earlier/meal-time/later pattern for discussion with the diabetes team.
