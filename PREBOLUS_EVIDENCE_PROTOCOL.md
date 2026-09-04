# Pre-bolus Evidence Protocol v1.0

## Purpose

Capture enough real-world information to learn whether meal-time bolus timing should vary for Darren based on current CGM glucose, CGM trend direction, meal type, carbohydrate, fat and later Dexcom response.

## Current phase

Observation only. Do not use the app to generate a specific number of pre-bolus minutes yet.

Darren continues to record the timing actually used. The current usual timing remains `At first bite / eating time` unless his diabetes team advises otherwise.

## New CGM trend field

Record the Dexcom direction at meal logging using one of:

- `↑↑ Rapidly rising`
- `↑ Rising`
- `↗ Slightly rising`
- `→ Stable`
- `↘ Slightly falling`
- `↓ Falling`
- `↓↓ Rapidly falling`
- `Not recorded`

The value is stored in the meal notes using the machine-readable tag `[CGM trend: ...]` so it survives the existing Supabase schema and is included in CSV exports without requiring a database migration.

## Review method

For suitable matched meals, review:

- Current glucose in mmol/L
- CGM trend direction
- Meal type
- Carbohydrate grams
- Fat grams or fat category
- Actual insulin
- ICR used
- Bolus timing actually used
- 1h/2h/4h/6h glucose pattern where available
- Peak and rise from starting glucose
- Time above 10 mmol/L
- Any post-meal low
- Late rise
- Activity, alcohol, illness, sensor issues and other confounders

## Evidence rule

Do not recommend a personalised pre-bolus timing rule from one or two examples. Look for repeated clean patterns. Starting glucose and trend arrow must be considered together. High-fat/high-carb meals must be treated separately because delayed digestion can make an earlier bolus less appropriate even when carbohydrate is high.

If future evidence consistently supports earlier, meal-time or later timing for a defined situation, flag it clearly as a discussion point with Darren's diabetes team before turning it into prescriptive app advice.

## Safety

The app must not currently calculate a correction dose, tell Darren to stack insulin, or automatically change insulin timing. Falling glucose, active insulin, uncertain carbohydrate, high-fat delayed meals and sensor problems are reasons for caution and should be interpreted in the full context.
