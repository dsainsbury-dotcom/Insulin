# Live CGM Intelligence v2.6.0

## Purpose
Turn the Nightscout feed into useful personal context rather than a single live glucose number.

## Features
- 3h, 6h, 12h and 24h rolling CGM graph.
- Current glucose/trend and in-range streak.
- Meal markers on the graph.
- Retrospective matched meal outcomes: start, peak, rise, peak time, 2h, 4h, 6h, approximate minutes >10 mmol/L, low observations and delayed-rise flag.
- Personal meal memory for repeated meals.
- Pattern summaries, ICR evidence summary, low/high event counts and personalised learning panel.

## Data behaviour
Nightscout is fetched read-only. Existing meal records remain in Supabase. Derived intelligence is calculated in the browser and can be rebuilt on later visits. New meals with a fresh Nightscout reading receive a source timestamp tag in notes.

## Safety boundary
These features describe observed data. They do not calculate correction insulin, change ICR, or provide autonomous pre-bolus instructions. Possible lows must be checked against known Dexcom sensor-fault context before being interpreted as genuine hypoglycaemia.
