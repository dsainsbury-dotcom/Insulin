# Version History

## v2.4.4 - 29 Aug 2026
- Processed the complete 3-file review set through 29 Aug 2026.
- Updated production CGM Progress to TIR 88%, average glucose 7.5 mmol/L, GMI 6.5% and CV 27.1%.
- Recorded improvement versus the prior 14 days: TIR 85% to 88%, average glucose 7.6 to 7.5, GMI 6.6% to 6.5%, CV 27.8% to 27.1%.
- Current clean meal evidence continues to support 1:15 as the working ICR baseline.
- Recorded the first verified real-world Smart Food nutrition-label OCR case: app 44.4 g carbs / 3 U at 12:28, Dexcom 44 g / 3 U at 12:28.
- Added the first OCR meal glucose outcome as UNDER INVESTIGATION rather than claiming a proven response pattern.
- Flagged the documented 27 Aug faulty-sensor lows as a sensor exception.
- Created rollback branch `backup/v2.4.3-pre-v2.5` before publication.
- Added repository-level project continuity documentation and detailed review record.

## v2.4.3 - 29 Aug 2026
- Added Smart Meal Assistant meal-dose display inside Smart Food.
- Exact carbohydrate/ICR calculation is shown before transfer.
- Whole-unit rounded-up pre-fill is shown before transfer.
- High-fat meals receive a delayed-rise context reminder only, with no automatic extra insulin.
- Existing cloud-first storage, barcode lookup, label OCR, manual nutrition, portion calculation and CGM Progress remain unchanged.

## v2.4.2 - 29 Aug 2026
- Removed manual refresh controls from normal use.
- Added last-refresh and queue health indicators.
- Fixed cloud-food queue ordering to reduce cross-device conflicts.
- Added direct cloud barcode check before public lookup.
- Added legacy v2.4 food-library migration into cloud storage.
- Added favourites and food-library search.
- Improved duplicate-barcode handling and error reporting.
- Added rollback branch `backup/v2.4.1-pre-v2.4.2`.

## v2.4.1 - 29 Aug 2026
- Moved the Smart Food library to a Supabase cloud-first design.
- Supabase becomes the source of truth when signed in.
- Browser storage is reduced to an offline queue/cache only.
- Added automatic retry of queued meal and food changes after reconnecting.
- Added automatic refresh on app focus, reconnect, visibility change and periodic background checks.
- Personal food library is checked before Open Food Facts for barcode scans.
- User-confirmed nutrition values take priority over public database values on future scans.
- Added cross-device food-library sync for barcode, nutrition, serving weight, usual portion, use count and source.
- Added visible cloud-readiness status for the food library.
- Added Supabase migration `supabase_food_library_v2.4.1.sql` with row-level security.
- Added rollback branch `backup/v2.4-pre-v2.4.1`.

## v2.4 - 29 Aug 2026
- Added Smart Food System to the Meal Tracker.
- Added barcode camera scanning with manual barcode fallback.
- Added Open Food Facts product lookup.
- Added nutrition-label photo OCR with manual confirmation.
- Added manual nutrition entry fallback.
- Added portion calculation by exact grams eaten or servings eaten, including half servings.
- Added automatic carbohydrate, fat and protein calculation for the actual portion.
- Added one-tap transfer into the standard meal form.
- Added nutrition-source tracking in meal notes for later CGM matching.
- Added a personal food library with use count and usual-portion history.
- Kept food outcome report cards evidence-only; no CGM response statistic is shown until a review has matched real glucose data.
- Added rollback branch `backup/v2.3-pre-v2.4`.

## v2.3 - 29 Aug 2026
- Separated Meal Tracker and CGM Progress into top-level tabs.
- Meal Tracker is the default view so food entry no longer requires scrolling through CGM history.

## v2.2 - 28 Aug 2026
- Added Clinical Goals using real Dexcom/AGP targets instead of an arbitrary score.
- Added "What I've Learned About Darren's Diabetes" with evidence-status labels.
- Added the strict 3-file review protocol to the app and repository documentation.
- Added the unmatched fast-acting insulin rule for restaurant/best-guess doses.
- Added sensor-error interpretation guidance.
- Kept the latest five upload summaries and progress timeline.
- Added a formal rollback branch: `backup/v2.1-pre-v2.2`.

## v2.1 - 28 Aug 2026
- Added My CGM Progress.
- Added five-upload Review Timeline.
- Added latest review summary, progress signals and sensor context.

## v2.0 - Aug 2026
- Added Supabase cloud storage and cross-device sync.
- Added email/password authentication.
- Added fat grams plus estimated fat-level logging.
- Added live dose calculation and whole-unit round-up prefill.
- Added local-first save and CSV backup export.

## v1.0
- Original local meal and ICR calculator.
