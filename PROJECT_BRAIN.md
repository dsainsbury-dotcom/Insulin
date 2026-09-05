# PROJECT_BRAIN

## Purpose
This repository is the authoritative source for Darren's personal CGM/meal-analysis app. A fresh developer or AI agent should be able to continue the project from this repository without relying on an old chat thread.

## Current production state
- Current production release: v2.5.0.
- Live app entry point: `index.html` on `main` via GitHub Pages.
- `smart-meal.html` contains the Smart Meal Assistant test/standalone implementation.
- Supabase is the cloud source of truth for meal and food-library data when signed in.
- Browser localStorage is only an offline queue/cache.
- GitHub `main` is the code/documentation source of truth.
- Rollback branches preserve known-good states before significant releases.

## Core product goal
Build a personal diabetes learning and logging tool that combines meal details, insulin, Smart Food nutrition capture and Dexcom review evidence. It should learn from Darren's own verified data rather than make generic assumptions.

## Current main features
- Meal logging with carbs, fat, meal type, starting glucose, ICR, actual insulin, bolus timing and notes.
- Default ICR 1:15 and target glucose 8.0 mmol/L.
- Meal-dose calculation only. No correction dose is calculated.
- Whole-unit dose prefill remains editable to record the actual dose taken.
- Cloud meal storage in Supabase plus safe offline queueing.
- Unified cloud/offline meal log and CSV export.
- Delete-meal action with confirmation and cloud/local queue protection.
- Smart Food System: barcode, Open Food Facts lookup, nutrition-label OCR, manual nutrition, portion calculation and personal cloud food library.
- Smart Food suggests meal type from food name and actual portion nutrition while keeping the choice editable.
- Favourite foods quick-use panel and All/Favourites library filter provide fast reuse of cloud-synced saved foods.
- Favourite foods quick access and cloud-persisted favourite/unfavourite controls.
- CGM Progress dashboard uses verified 3-file reviews only.

## Meal type categories
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

Food-name matches should take priority over broad nutrition-only inference. Fat grams remain separate from meal type so later analysis can distinguish food category from fat effect.

## CGM evidence workflow
A full review requires all three files:
1. Dexcom Clarity PDF
2. Dexcom raw CSV
3. ICR Meal Dashboard CSV

Do not complete a full review if one is missing. Follow `CGM_ANALYSIS_PROTOCOL_v1.0.md`.

Evidence labels used in the app:
- PROVEN REPEATEDLY
- LIKELY
- UNDER INVESTIGATION
- ANALYSIS RULE

Do not turn one meal outcome into a proven response pattern.

## Current verified CGM baseline
Latest verified review is 2 Sep 2026 for 20 Aug-2 Sep 2026: TIR 85%, average glucose 7.7 mmol/L, GMI 6.6%, CV 28.8%, very high 1%.
- TIR 88%
- Average glucose 7.5 mmol/L
- GMI 6.5%
- CV 27.1%
- Very high 0%

The current clean meal evidence supports 1:15 as the working baseline. Any insulin-setting change should remain a discussion point for the diabetes team rather than an automatic app decision.

## Important analysis rules
- Fast-acting insulin in Dexcom with no matching app meal is treated as unknown/best-guess nutrition dosing and excluded from clean ICR evidence.
- Documented sensor lows contradicted by finger-prick readings are sensor exceptions, not genuine hypos.
- High-fat meals may show delayed/extended rises. Review the full trace beyond the standard 4-hour meal card where relevant.
- Smart Food/OCR/barcode nutrition must be user-confirmed before being treated as reliable.
- Do not invent glucose outcomes or personalised rules that are not supported by the uploaded evidence.

## First verified Smart Food live case
29 Aug 2026 nutrition-label OCR case:
- App: 44.4 g carbs, 3 U fast-acting, 12:28 BST.
- Dexcom: 44 g carbs, 3 U fast-acting, 12:28 BST.
This verifies the scanner-to-meal-log workflow end to end. It is one glucose-response observation, not a proven food-response rule.

## Architecture
### Front end
Currently a lightweight static HTML/JavaScript app. `index.html` is the production app and still contains much of the application logic in one file.

### Cloud data
Supabase stores meal entries and the personal food library. Existing SQL setup/migrations in this repository must be kept with the project backup.

### Hosting
GitHub Pages serves the production site from the repository.

### Version control
GitHub `main` is production. Create a rollback branch before meaningful production changes. Update README/CHANGELOG when publishing a release.

## Development rules
- Read this file, `PROJECT_RULES.md`, `README.md`, `CHANGELOG.md` and the relevant feature/protocol documents before making major changes.
- Preserve existing working behaviour unless the requested change requires otherwise.
- Create a rollback branch before a meaningful production release.
- Do not silently rewrite data models or break Supabase compatibility.
- Keep UI language plain and practical.
- Treat data accuracy as more important than visual novelty.
- Never claim a release is tested unless the relevant behaviour was actually tested.
- Record successful real-world tests when Darren confirms them.

## Backup policy
GitHub remains the live source. Google Drive is the disaster-recovery mirror. After each production release, mirror the current repository files and recovery documentation into the CGM App Backup folder in Google Drive and retain a dated release archive. See `BACKUP_AND_RECOVERY.md`.

## Longer-term direction
Gradually move away from hard-coded CGM Progress values toward stored review records and an evidence database. Future goals include food outcomes, repeated-meal comparisons, confidence grading, automated review imports and personalised pattern detection. Do this incrementally without risking the stable working app.

## Pre-bolus evidence phase
From v2.5.0, every new meal can record the current Dexcom trend arrow. Continue treating `At first bite / eating time` as the usual observed timing unless Darren records something different. Do not infer a fixed pre-bolus formula yet. Future reviews should combine starting glucose, CGM trend, meal type, carbohydrate, fat, actual timing and later Dexcom response. See `PREBOLUS_EVIDENCE_PROTOCOL.md`.

## v2.5.1 live Nightscout
- Live Nightscout API access was proven on 5 Sep 2026 using `/api/v1/entries.json?count=1&token=...` and repeated 5-minute SGV data.
- Production app now supports a per-device Nightscout URL + dedicated readable token held in browser localStorage only.
- Live readings supply mmol/L, Nightscout direction and reading age. Supported direction mapping: DoubleUp, SingleUp, FortyFiveUp, Flat, FortyFiveDown, SingleDown, DoubleDown.
- A reading older than 10 minutes is stale and must not be auto-filled into a meal.
- Manual glucose/trend entry remains available and takes precedence when the user edits it.
- Do not place Nightscout `API_SECRET` or readable tokens in public GitHub source or Supabase meal records.
- This feature is data capture/supportive only. Dexcom remains the treatment-decision source.

## v2.6.0 Live CGM Intelligence
- Nightscout history now powers rolling trend visualisation and retrospective meal-response analysis.
- Recent meals can be matched to CGM history for start, peak, peak rise/time, 2h/4h/6h, approximate time >10, low observations and delayed rises.
- Repeated meals build personal meal-memory summaries.
- Pattern, ICR and low/high panels are evidence summaries only, not dosing recommendations.
- Sensor faults, overlapping meals, alcohol, exercise and other confounders remain review exclusions.
- Browser closure does not prevent later outcome reconstruction because Nightscout retains history.
