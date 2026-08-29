# Version History

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
