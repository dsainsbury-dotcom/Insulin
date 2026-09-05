# v2.7.0 - Restaurant Foods
- Added a clean mobile restaurant-food browser inside Smart Food.
- Starter UK chains: Greggs, PizzaExpress and McDonald's.
- Added restaurant and category filters plus menu search.
- Restaurant item cards show portion carbs, fat, protein, kcal, source and source date.
- One tap copies meal description, carbs, fat and suggested meal type into Add meal.
- Restaurant nutrition is kept in a separate versioned dataset so future chains can be added without bloating the personal food library.
- No change to ICR, dose calculation, Nightscout or CGM intelligence logic.

## v2.6.2 - Collapsible food library
- Collapsed the full My food library section by default to reduce page length on mobile.
- Added Show library / Hide library and a tappable section header.
- The library open/closed state is remembered on the device.
- Favourite quick access remains separate and unchanged.

# Version History


## v2.6.1 - 5 Sep 2026
- Collapsed Nightscout connection settings by default after setup, with a manual Connection settings toggle.
- Added favourite search, recently-used ordering, top-six quick view, Show all favourites, and a persistent Hide favourites control.
- No changes to Live CGM Intelligence, Nightscout analysis, insulin calculations, or clinical logic.

## v2.5.0 - 4 Sep 2026
- Added required CGM trend-arrow capture at meal logging: rapidly rising, rising, slightly rising, stable, slightly falling, falling or rapidly falling.
- Trend is stored in a machine-readable notes tag for compatibility with the current Supabase schema and exported as a dedicated `cgm_trend` CSV column.
- Added `PREBOLUS_EVIDENCE_PROTOCOL.md`.
- Pre-bolus timing remains observation-only. No automated timing or correction advice is generated yet.
- Future reviews will test whether timing should vary by starting glucose, trend arrow, meal type, carbohydrate, fat and later Dexcom response.
- Rollback branch: `backup/v2.4.9-pre-v2.5.0`.


## v2.4.9 - 2 Sep 2026
- Processed the complete Dexcom PDF + raw CSV + app CSV review for 20 Aug-2 Sep.
- Updated CGM Progress: TIR 85%, average glucose 7.7 mmol/L, GMI 6.6%, CV 28.8%.
- All headline AGP goals remain achieved.
- ICR verdict remains 1:15 as the working baseline. No clear post-meal low signal supports winding back to 1:20; current evening highs are too confounded to justify strengthening the global ratio.
- Added whole-unit round-up on small-carb meals as a specific safety-monitoring rule.
- Added review record `reviews/CGM_REVIEW_2026-09-02.md`.
- Created rollback branch `backup/v2.4.8-pre-v2.4.9`.


## v2.4.8 - 31 Aug 2026
- Fixed Favourite toggles being overwritten by the previous saved food state.
- Favourite/unfavourite changes now write directly to Supabase when online.
- Offline favourite changes are queued and immediately reflected locally.
- Created rollback branch `backup/v2.4.7-pre-v2.4.8` before publication.

## v2.4.7 - 31 Aug 2026
- Added a dedicated Favourite foods quick-use panel.
- Added one-tap Use actions for starred foods.
- Added All foods / Favourites filtering in My food library.
- Favourite state remains cloud-synced across signed-in devices.
- Created rollback branch `backup/v2.4.6-pre-v2.4.7` before publication.

## v2.4.6 - 30 Aug 2026
- Added a Delete action to every row in the Unified meal log.
- Added a confirmation prompt before deletion.
- Queued/offline-only entries can be deleted locally.
- Cloud entries require an active signed-in online session before deletion.
- Cloud deletion targets the current user's meal by `user_id` and `client_id`.
- The matching local queue entry is also removed so deleted meals cannot be re-uploaded on the next sync.
- Offline cloud deletion is refused rather than allowing an entry to reappear later.
- Created rollback branch `backup/v2.4.5-pre-v2.4.6` before publication.

## v2.4.5 - 30 Aug 2026
- Replaced the generic Normal mixed meal default with analysis-focused meal categories.
- Added Pasta, Rice / noodles, Bread / sandwich, Potato / chips, Pizza, Curry, High-fat + high-carb, Very high-carb, Lower-carb, Dessert / sweet food, Snack and Other / unknown.
- Smart Food now suggests meal type from product/food name and actual portion nutrition.
- Specific food-name matches take priority over broad nutrition-based classification.
- Suggested meal type remains editable before saving.
- Fat grams remain separate from meal type for future CGM analysis.
- Created rollback branch `backup/v2.4.4-pre-v2.4.5` before publication.

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

## v2.5.1 - 2026-09-05
- Added live read-only Nightscout CGM integration.
- Current glucose, trend direction and reading age are retrieved from the latest SGV endpoint.
- Fresh live readings can populate the meal glucose and CGM trend fields with manual override retained.
- Nightscout site URL and readable token are stored only in local browser storage, not GitHub or Supabase.
- Readings older than 10 minutes are treated as stale and are not used for meal auto-fill.

## v2.6.0 - 2026-09-05
- Added Live CGM Intelligence dashboard and rolling Nightscout CGM graph.
- Added retrospective meal outcome calculation from Nightscout history.
- Added personal meal memory, repeated-pattern detection, ICR evidence dashboard, low/high event summary and personalised learning panel.
- Added live Nightscout source timestamp tagging to new meal records.
- Analysis remains observational and does not calculate correction insulin or issue autonomous pre-bolus instructions.
