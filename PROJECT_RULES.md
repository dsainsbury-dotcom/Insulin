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
