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

## Required files for a full review

A full CGM and ICR review should use three files:

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
   - Primary source of truth for meal and dose information
   - Meal description
   - Meal type
   - Carbohydrate grams
   - Fat level
   - Estimated fat grams when known
   - ICR used
   - Calculated dose
   - Actual insulin taken
   - Bolus timing
   - Notes and confounders

## Important workflow rule

Do not perform detailed meal-by-meal or ICR analysis from Dexcom Clarity alone when the ICR Meal Dashboard CSV is missing.

If Dexcom files are uploaded without the ICR Meal Dashboard CSV:

- Overall Dexcom control may still be reviewed.
- Before calculating detailed meal performance or judging the current ICR, ask for the latest ICR Meal Dashboard CSV.

The ICR Meal Dashboard CSV is the primary meal source. Do not double-count or duplicate meals by independently treating Dexcom meal entries as a second meal log when the app CSV is available.

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

## Sensor-quality rules

Known sensor artefacts must not be used as evidence that the ICR is too strong or that true hypoglycaemia occurred.

Important examples include:

- Compression lows labelled CL
- Faulty sensor periods labelled FCGM or noted as faulty
- First 24 hours after a new sensor (NCGM), which may be noisier or over-read
- The false-low period overnight 10-11 August 2026, including Dexcom around 2.2-3.3 mmol/L while finger-prick was 8.3 mmol/L

Dexcom's official headline statistics may still contain those readings. Where raw data allows, calculate or describe a cleaned interpretation separately if the artefact materially affects the result.

## Other context to retain

- Fasting glucose is logged in Dexcom's fasting glucose field on waking.
- Historic entries before that field was used can generally be interpreted with long-acting insulin taken on waking unless otherwise noted.
- Ketone note spellings such as ketones, keytones and keystones should all be recognised as ketone readings.
- High-fat/high-carb meals require review beyond the standard 4-hour meal card where relevant.
- Avoid unsafe insulin stacking. Off-plan extra doses are data points for clinician discussion, not evidence to encourage repetition.

## Standard review output

Future reviews should normally contain:

### 1. Overall control
- GMI
- Average glucose
- Time in Range
- High / Very High
- Low / Very Low
- CV / variability
- AGP and time-of-day patterns
- Change versus the previous comparable Dexcom period

### 2. Meal performance
- Best and worst-performing meals
- Meal-by-meal peak and duration above 10 mmol/L
- 2h / 4h / 6h response where data quality permits
- Late-rise patterns
- Meal-type and fat-content patterns

### 3. ICR assessment
A clear conclusion such as:

- 1:15 looks appropriate
- 1:15 looks too weak
- 1:15 looks too strong
- 1:15 works for normal meals but not certain meal types
- More clean data is needed before changing the ratio

The conclusion must be supported by the actual meal data, not just headline TIR.

### 4. Context and exceptions
- Sensor faults
- New sensor days
- Exercise
- Alcohol
- Ketones
- Illness or steroid exposure
- Other relevant confounders

### 5. Questions for the diabetes team
Only include clinically useful questions arising from the data, especially around ICR, high-fat meals, delayed rises, correction rules and safety.

## Quarterly surgery update

Approximately every 90 days, prepare a concise, easy-to-read Dexcom summary for the GP surgery/diabetes nurse because the surgery does not have direct Dexcom access.

The quarterly summary should focus on:

- 90-day headline Dexcom metrics
- Change from the previous 90-day Dexcom period
- Current ICR and whether the data supports it
- Key meal/fat patterns
- Relevant sensor artefacts and clinical exceptions
- Short questions or actions for the diabetes team

## Data-quality principle

Accuracy comes before completeness. Do not invent missing meal details, fat estimates, insulin doses, timings or glucose responses. If information is missing or ambiguous, state that clearly.

## Version

CGM Analysis Protocol v1.0
Created: 23 August 2026
Repository: dsainsbury-dotcom/Insulin
