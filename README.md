# ICR Meal Dashboard v2.4.1

Live GitHub Pages app for cloud-synced meal and insulin logging, personalised Dexcom review history and Smart Food nutrition lookup.

## Live version
- v2.4.1 is the current production version on the repository root.
- Meal Tracker remains the default view; CGM Progress is a separate tab.
- Supabase is the source of truth when signed in.
- Browser storage is used only as an offline queue/cache for unsynced changes.
- CSV export remains available as a user-controlled backup/export option.

## Smart Food System v2.4.1
- Barcode camera scanning plus manual barcode entry.
- Personal Supabase food library is checked before Open Food Facts.
- Once a product has been confirmed, the user's saved nutrition values take priority on future scans.
- Open Food Facts is used only when the barcode is not already in the personal library.
- Nutrition-label photo OCR using Tesseract.js in the browser.
- OCR values must be checked/confirmed before use.
- Manual nutrition mode for packet labels, restaurant websites and foods not found by barcode.
- Portion mode supports exact weight eaten or number of servings, including 0.5 servings.
- Calculates carbohydrate, fat and protein for the amount actually eaten.
- One-tap transfer into the normal meal tracker.
- Nutrition source is retained with the meal for later CGM review context.
- Food library, usual portion, serving weight, source, barcode and nutrition are cross-device once the Supabase `food_library` table is enabled.
- Offline food changes are queued and retried automatically when connectivity returns.
- Food report cards do not invent CGM outcomes. Glucose-response statistics will only be added when real review matching supports them.

## Supabase setup for food-library sync
Run `supabase_food_library_v2.4.1.sql` once in the Supabase SQL Editor. This creates the `food_library` table, row-level security policies and updated-at trigger.

The app checks whether the table is available and shows the status in the Smart Food System panel. Until the migration is run, meal cloud sync continues to work but food-library cross-device sync cannot be treated as active.

## Meal logging
- Default ICR is 1:15.
- Default target glucose is 8.0 mmol/L.
- No correction dose is calculated.
- Meal dose updates live as carbohydrate or ICR changes.
- The exact calculated meal dose is shown and the actual-insulin field is pre-filled by rounding up to the next whole unit; it remains editable to record what was actually taken.
- Fat is either entered as grams when known or as a Low / Medium / High / Very high estimate when grams are unknown.

## CGM progress dashboard
- Latest verified review metrics and change versus prior period.
- Clinical Goals use real Dexcom/AGP targets rather than an invented score.
- What I've Learned About Darren's Diabetes separates PROVEN REPEATEDLY, LIKELY, UNDER INVESTIGATION and ANALYSIS RULE statements.
- Review Timeline keeps recent verified upload summaries visible.
- Version History records major app releases.

## 3-file review rule
A complete review requires:
1. Dexcom Clarity PDF
2. Dexcom raw CSV
3. ICR Meal Dashboard CSV

If any one is missing, the full review waits until all three are available.

See `CGM_ANALYSIS_PROTOCOL_v1.0.md` for the detailed workflow.

## Data and rollback
- Supabase is the central cross-device store for meals and, after the v2.4.1 migration, the food library.
- Browser localStorage is only an offline queue/cache.
- CSV export provides an additional manual backup.
- `backup/v2.4-pre-v2.4.1` preserves the pre-cloud-food-library release.
- Earlier rollback branches and GitHub commit history remain available.

## Safety
This is a personal logging/calculation and review aid, not a medical device. Barcode and OCR nutrition values must be checked before use. It does not calculate correction doses or independently determine insulin settings. Treatment decisions should follow the user's agreed diabetes-team plan.
