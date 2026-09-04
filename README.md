# ICR Meal Dashboard v2.5.0

## v2.5.0 - CGM trend capture
Meal logging now records the Dexcom trend arrow alongside current glucose. This starts the evidence-gathering phase for a future personalised pre-bolus timing assistant. The app continues to record the timing Darren actually used and does not yet prescribe a specific pre-bolus interval. See `PREBOLUS_EVIDENCE_PROTOCOL.md`.


## v2.4.9 review update - 2 Sep 2026
- Latest 14-day Dexcom metrics: TIR 85%, average 7.7 mmol/L, GMI 6.6%, CV 28.8%.
- 1:15 remains the working ICR. Current data does not show a clear post-meal low signal that would support winding back to 1:20, and does not yet justify a stronger global ratio.
- Evening/high-fat/overlapping meals remain the main watch area.
- Full evidence record: `reviews/CGM_REVIEW_2026-09-02.md`.


Live GitHub Pages app for cloud-synced meal and insulin logging, personalised Dexcom review history and Smart Food nutrition lookup.

## Live version
- v2.4.8 is the current production version on the repository root.
- Meal Tracker remains the default view; CGM Progress is a separate tab.
- Supabase is the source of truth when signed in.
- Browser storage is used only as an offline queue/cache for unsynced changes.
- Automatic sync runs at sign-in, app focus/return, reconnect and every 60 seconds while open.
- CSV export remains available as a user-controlled backup/export option.
- The 29 Aug 2026 complete 3-file CGM review is the latest verified progress snapshot.

## Favourite persistence fix v2.4.8
- Fixed a bug where tapping Favourite changed the value but the general food save path restored the previous favourite state.
- Favourite/unfavourite now writes the changed food directly to Supabase when online.
- Offline changes are queued and reflected in the local library immediately.
- Rollback branch: `backup/v2.4.7-pre-v2.4.8`.

## Favourite foods v2.4.7
- Starred foods now appear in a dedicated Favourite foods quick-use panel.
- Each favourite has a one-tap Use action that opens the saved nutrition and usual portion.
- The food library now has All foods and Favourites filters.
- Favourite state continues to sync through Supabase across signed-in devices.
- Rollback branch: `backup/v2.4.6-pre-v2.4.7`.

## Meal log deletion v2.4.6
- Every Unified meal log row now has a Delete action.
- A confirmation prompt is required before deletion.
- Offline/queued-only entries are removed from the local queue immediately after confirmation.
- Cloud entries require an active signed-in online session and are deleted from Supabase using the current user's ID plus the meal client ID.
- The local queue is also cleared for the same client ID so a deleted entry cannot be re-uploaded by the sync process.
- If a cloud delete is attempted while offline, the app refuses rather than pretending the deletion succeeded.
- Rollback branch: `backup/v2.4.5-pre-v2.4.6`.

## Smart Food System
- Barcode camera scanning plus manual barcode entry.
- Personal Supabase food library is checked before Open Food Facts.
- Confirmed saved nutrition values take priority on future scans.
- Nutrition-label photo OCR uses Tesseract.js and requires user confirmation before use.
- Manual nutrition mode supports packet labels, restaurant websites and foods not found by barcode.
- Portion calculation supports exact weight or servings.
- Carbohydrate, fat and protein are calculated for the amount actually eaten.
- Nutrition source is retained with the meal for later CGM review matching.
- Food library, usual portion, serving weight, source, barcode and nutrition are cross-device.
- Favourites, search, offline queueing and retry are included.
- Food outcome claims remain evidence-only.

## Smarter meal types v2.4.5
Smart Food suggests a useful meal type instead of defaulting every entry to Normal mixed meal.

Current categories:
- Balanced / mixed meal
- Pasta
- Rice / noodles
- Bread / sandwich
- Potato / chips
- Pizza
- Curry
- High-fat + high-carb
- Very high-carb (100g+)
- Lower-carb meal
- Dessert / sweet food
- Snack
- Other / unknown

The suggestion uses the food/product name first, then portion carbohydrate and fat where useful. The user can always change the suggested type before saving. Fat grams remain a separate field so later CGM analysis can distinguish food category from fat effect.

### First verified real-world Smart Food case
On 29 Aug 2026 the nutrition-label OCR workflow produced a real meal record that matched Dexcom closely:
- App: 44.4 g carbohydrate, 3 U fast-acting, 12:28 BST.
- Dexcom: 44 g carbohydrate, 3 U fast-acting, 12:28 BST.
- App nutrition source: `Nutrition label OCR - confirmed`.
- This verifies the scanner-to-meal-log workflow end to end. It is one glucose-response observation, not enough by itself to define a food-response rule.

## Smart Meal Assistant
- Shows exact carbohydrate/ICR calculation before transfer.
- Shows the whole-unit rounded-up pre-fill before transfer.
- High-fat meals receive a delayed-rise context reminder only. No automatic extra insulin is added.

## Meal logging
- Default ICR is 1:15.
- Default target glucose is 8.0 mmol/L.
- No correction dose is calculated.
- Meal dose updates live as carbohydrate or ICR changes.
- Actual insulin remains editable so the app records what was actually taken.
- Fat is recorded in grams when known, otherwise by estimate.

## Latest CGM review - 29 Aug 2026
Period: 16-29 Aug 2026.
- Time in range: 88%.
- Average glucose: 7.5 mmol/L.
- GMI: 6.5%.
- CV: 27.1%.
- Very high: 0%.
- Compared with the prior 14 days, TIR improved from 85% to 88%, average glucose from 7.6 to 7.5 mmol/L, GMI from 6.6% to 6.5%, and CV from 27.8% to 27.1%.
- The current clean meal set continues to support 1:15 as the working baseline.
- High-fat/delayed rises remain the main meal pattern to watch.
- Documented overnight lows on 27 Aug were contradicted by finger-prick glucose and are treated as a faulty-sensor exception.

See `LATEST_CGM_REVIEW_2026-08-29.md` for the detailed review record.

## CGM progress dashboard
- Latest verified review metrics and change versus prior period.
- Clinical Goals use real Dexcom/AGP targets.
- Learned-insight statuses are PROVEN REPEATEDLY, LIKELY, UNDER INVESTIGATION and ANALYSIS RULE.
- Review Timeline keeps the latest five upload summaries visible.

## 3-file review rule
A complete review requires:
1. Dexcom Clarity PDF
2. Dexcom raw CSV
3. ICR Meal Dashboard CSV

If any one is missing, the full review waits until all three are available. See `CGM_ANALYSIS_PROTOCOL_v1.0.md`.

## Project continuity
`PROJECT_BRAIN.md` is the repository-level project memory for future development threads. GitHub is the authoritative source for architecture, current release state, protocol, rollback points and major decisions.

## Data and rollback
- Supabase is the central cross-device store for meals and the food library.
- Browser localStorage is only an offline queue/cache.
- CSV export provides an additional manual backup.
- `backup/v2.4.5-pre-v2.4.6` preserves the stable state immediately before meal-log deletion was added.
- Earlier rollback branches and GitHub commit history remain available.

## Safety
This is a personal logging/calculation and review aid, not a medical device. Barcode and OCR nutrition values must be checked before use. It does not calculate correction doses or independently determine insulin settings. Treatment decisions should follow the agreed diabetes-team plan.
