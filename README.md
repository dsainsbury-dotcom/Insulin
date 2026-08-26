# ICR Meal Dashboard v2.0

Live GitHub Pages app for cloud-synced meal and insulin logging used alongside Dexcom CGM review.

## Live version
- v2.0 is the current production version on the repository root.
- Supabase provides authenticated cross-device meal storage.
- Authentication uses email + password rather than repeated magic-link sign-ins.
- The existing Supabase user can create/reset a password through the one-off password recovery flow in the app.
- Entries are cached locally first and then synced to cloud when signed in.
- Cloud data refreshes automatically when the page opens, regains focus, comes back online, and periodically while open.
- CSV export remains available as a user-controlled backup/export option.

## Meal logging
- Default ICR is 1:15.
- Default target glucose is 8.0 mmol/L.
- No correction dose is calculated.
- Meal dose updates live as carbohydrate or ICR changes.
- The exact calculated meal dose is shown, while the 'Insulin actually taken' field is pre-filled by rounding the calculated dose up to the next whole unit. The field can be changed to record the true dose used.
- Fat is either entered as grams when known or as a Low / Medium / High / Very high estimate when grams are unknown. The alternative field is disabled to avoid double entry.
- Meal description, meal type, carbohydrate, fat, starting glucose, ICR, actual insulin, bolus timing, target glucose and notes are retained for later CGM matching.

## Data and rollback
- Supabase is the central cross-device store.
- Browser localStorage remains a local-first safety cache.
- CSV export provides an additional manual backup.
- The frozen local-only v1.0 remains available on branch `backup/v1.0-local` as a rollback copy.
- The `/beta/` directory is retained as historical v1.1 cloud-sync test material and is not the production app.

## CGM review
See `CGM_ANALYSIS_PROTOCOL_v1.0.md` for the agreed analysis workflow. Dexcom provides the glucose outcome while the ICR Meal Dashboard provides the structured meal and dosing context.

## Safety
This is a personal logging/calculation aid, not a medical device. It does not calculate correction doses or determine insulin settings. Insulin ratios and treatment decisions should follow the user's agreed diabetes-team plan.