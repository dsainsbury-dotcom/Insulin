## Standing update workflow agreed 20 November 2026

For every future CGM update requested by Darren:
1. Use the three supplied exports through Google Drive. Archive and verify new uploads in the private CGM Review Archives folder. GitHub main remains the source for app code. The old Mac checkout and Downloads originals are unnecessary after verified backup. Temporary processing copies may be needed.
2. Review all app sections against the new evidence, including progress, clinical goals, learning, timeline and version history. Check that live meal memory, reference meal history, patterns, ratio evidence, lows/highs and live learning still refresh from their supported cloud sources. Distinguish live data from dated uploaded reviews.
3. Account explicitly for incomplete meal and insulin logging. Missing entries remain unknown and recorded totals are incomplete. Do not infer dose effectiveness from aggregate glucose alone.
4. Preserve a rollback branch, validate the change and publish the approved update to GitHub Pages. Keep raw medical exports and credentials private.
5. Update the Google Drive production mirror, recovery instructions and dated release archive. Verify the uploaded copies.
6. Fetch the public app and verify its new version, review date and changed content before reporting completion. Continue through recoverable failures. Report any genuine blocker precisely.
7. Remove local originals only after verification and user authorization. Completion means published, backed up and checked live.

# PROJECT_RULES

These are non-negotiable operating rules for continuing the CGM app safely and consistently.

## Source of truth
- GitHub `main` is the authoritative code/documentation source.
- Supabase is the authoritative cloud data source when signed in.
- Google Drive is a disaster-recovery mirror, not a competing live development copy.
- Browser localStorage is only an offline queue/cache.

## Release safety
- Create a rollback branch before meaningful production releases.
- Keep previous rollback branches.
- Update `CHANGELOG.md` and `README.md` when release behaviour changes.
- Do not remove working functionality unless explicitly requested or required by a fix.
- Do not claim something is tested unless it has actually been tested.
- When Darren confirms a feature works in production, record that as a successful live test.

## CGM review protocol
A complete CGM review requires all three:
1. Dexcom Clarity PDF
2. Dexcom raw CSV
3. ICR Meal Dashboard CSV

If one is missing, wait rather than creating a partial 'full review'. Follow `CGM_ANALYSIS_PROTOCOL_v1.0.md`.

## Current insulin context in the app
- Working ICR baseline: 1:15.
- Default target glucose: 8.0 mmol/L.
- Meal-dose calculation only.
- No automatic correction dose.
- Do not automatically add insulin for high-fat meals.
- Dose prefill remains editable because the log must record what was actually taken.
- Any proposed insulin-setting change is evidence for discussion with the diabetes team, not an automatic treatment decision.

## Evidence discipline
- Personalised conclusions must be grounded in verified uploaded data.
- Use evidence states: PROVEN REPEATEDLY, LIKELY, UNDER INVESTIGATION and ANALYSIS RULE.
- One meal is not enough to create a proven personalised food rule.
- Fast-acting insulin with no matching app meal is excluded from clean ICR evidence.
- Documented sensor-error lows contradicted by finger-prick readings are treated as sensor exceptions.
- High-fat/high-carb meals may need review beyond 4 hours because delayed rises can occur.

## Smart Food rules
- Personal cloud food library is checked before Open Food Facts.
- User-confirmed nutrition values take priority over public database values.
- OCR values must be checked/confirmed before use.
- Meal type can be suggested by the app but must remain editable.
- Specific food-name matching has priority over broad nutrition-only inference.
- Keep fat grams separate from meal type.
- Do not invent food-outcome statistics until CGM review evidence supports them.

## Data protection and deletion
- Cloud meal deletion must target the signed-in user's record.
- Remove matching queued copies when deleting so they cannot re-upload.
- Refuse unsafe offline deletion of cloud-only entries when the result could later reappear.
- Preserve user data and avoid migrations that could silently discard existing records.

## Backup rule
After every production release:
1. GitHub contains the new production code, docs, changelog and rollback branch.
2. Google Drive `CGM App Backup` is updated with a current project mirror.
3. A dated/versioned release archive is retained in Drive.
4. The recovery guide and project brain are mirrored too.

If Drive cannot be updated during a release, state that clearly rather than implying the backup exists.
