# ICR Meal Dashboard v2.4

Live GitHub Pages app for cloud-synced meal and insulin logging, personalised Dexcom review history and Smart Food nutrition lookup.

## Live version
- v2.4 is the current production version on the repository root.
- Meal Tracker remains the default view; CGM Progress is a separate tab.
- Supabase provides authenticated cross-device meal storage.
- Entries are cached locally first and then synced to cloud when signed in.
- CSV export remains available as a user-controlled backup/export option.

## Smart Food System v2.4
- Barcode camera scanning plus manual barcode entry.
- Open Food Facts lookup for product name and nutrition per 100 g.
- Nutrition-label photo OCR using Tesseract.js in the browser.
- OCR values must be checked/confirmed before use.
- Manual nutrition mode for packet labels, restaurant websites and foods not found by barcode.
- Portion mode supports exact weight eaten or number of servings, including 0.5 servings.
- Calculates carbohydrate, fat and protein for the amount actually eaten.
- One-tap transfer into the normal meal tracker.
- Nutrition source is written into the meal notes with a structured SFS marker for later CGM review context.
- Personal food library remembers used products and recent/usual portion sizes on the device.
- Food report cards do not invent CGM outcomes. Glucose-response statistics will only be added when real review matching supports them.

See `SMART_FOOD_SYSTEM_v2.4.md` for implementation and data-quality rules.

## Meal logging
- Default ICR is 1:15.
- Default target glucose is 8.0 mmol/L.
- No correction dose is calculated.
- Meal dose updates live as carbohydrate or ICR changes.
- The exact calculated meal dose is shown and the actual-insulin field is pre-filled by rounding up to the next whole unit; it remains editable to record what was actually taken.
- Fat is either entered as grams when known or as a Low / Medium / High / Very high estimate when grams are unknown.

## CGM progress dashboard
- Latest verified review metrics and change versus prior period.
- Clinical Goals use the real Dexcom/AGP targets rather than an invented score.
- What I've Learned About Darren's Diabetes separates PROVEN REPEATEDLY, LIKELY, UNDER INVESTIGATION and ANALYSIS RULE statements.
- Review Timeline keeps the latest five verified upload summaries visible.
- Version History records major app releases.

## 3-file review rule
A complete review requires:
1. Dexcom Clarity PDF
2. Dexcom raw CSV
3. ICR Meal Dashboard CSV

If any one is missing, the full review waits until all three are available.

See `CGM_ANALYSIS_PROTOCOL_v1.0.md` for the detailed workflow.

## Data and rollback
- Supabase is the central cross-device meal store.
- Browser localStorage remains a local-first safety cache.
- CSV export provides an additional manual backup.
- `backup/v2.3-pre-v2.4` preserves the pre-Smart-Food release.
- Earlier rollback branches and GitHub commit history remain available.

## Safety
This is a personal logging/calculation and review aid, not a medical device. Barcode and OCR nutrition values must be checked before use. It does not calculate correction doses or independently determine insulin settings. Treatment decisions should follow the user's agreed diabetes-team plan.
