# ICR Meal Dashboard v2.2

Live GitHub Pages app for cloud-synced meal and insulin logging, personalised Dexcom review history and evidence-based diabetes learning.

## Live version
- v2.2 is the current production version on the repository root.
- Supabase provides authenticated cross-device meal storage.
- Authentication uses email + password.
- Entries are cached locally first and then synced to cloud when signed in.
- Cloud data refreshes automatically when the page opens, regains focus, comes back online and periodically while open.
- CSV export remains available as a user-controlled backup/export option.

## Meal logging
- Default ICR is 1:15.
- Default target glucose is 8.0 mmol/L.
- No correction dose is calculated.
- Meal dose updates live as carbohydrate or ICR changes.
- The exact calculated meal dose is shown, while the 'Insulin actually taken' field is pre-filled by rounding the calculated dose up to the next whole unit. The field can be changed to record the true dose used.
- Fat is either entered as grams when known or as a Low / Medium / High / Very high estimate when grams are unknown. The alternative field is disabled to avoid double entry.
- Meal description, meal type, carbohydrate, fat, starting glucose, ICR, actual insulin, bolus timing, target glucose and notes are retained for later CGM matching.

## v2.2 progress dashboard
- My CGM Progress shows the latest verified review metrics and change versus the prior period.
- Clinical Goals uses the real Dexcom/AGP targets rather than an invented score.
- What I've Learned About Darren's Diabetes separates PROVEN REPEATEDLY, LIKELY, UNDER INVESTIGATION and ANALYSIS RULE statements.
- Review Timeline keeps the latest five verified upload summaries visible in the app.
- The 3-file review protocol is shown inside the app.
- Version History records major app releases and why they changed.

## 3-file review rule
A complete review requires:
1. Dexcom Clarity PDF
2. Dexcom raw CSV
3. ICR Meal Dashboard CSV

If any one is missing, the full review should wait until all three are available.

See `CGM_ANALYSIS_PROTOCOL_v1.0.md` for the detailed workflow, including the unmatched fast-acting insulin rule, sensor-error handling, ICR review method, app update steps and review email format.

## Data and rollback
- Supabase is the central cross-device store.
- Browser localStorage remains a local-first safety cache.
- CSV export provides an additional manual backup.
- `backup/v2.1-pre-v2.2` preserves the stable app immediately before the v2.2 release.
- The frozen local-only v1.0 remains available on `backup/v1.0-local`.
- GitHub commit history provides an additional source-code recovery path.

## Safety
This is a personal logging/calculation aid and review dashboard, not a medical device. It does not calculate correction doses or independently determine insulin settings. Insulin ratios and treatment decisions should follow the user's agreed diabetes-team plan.
