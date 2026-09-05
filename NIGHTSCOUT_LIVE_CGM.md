# Nightscout Live CGM integration - v2.5.1

## Purpose
Use Nightscout as a near-real-time read-only CGM source so a meal can capture the glucose and direction that existed when it was logged.

## Endpoint
`/api/v1/entries.json?count=1&token=<READABLE_TOKEN>`

## Security
Use a dedicated Nightscout subject with role `readable`. Never use or expose `API_SECRET`. The browser stores the site URL and token in localStorage on that device only. Credentials are not written to Supabase meal records and are not committed to GitHub.

## Freshness
A current reading is usable for meal auto-fill only when it is no more than 10 minutes old and has a recognised trend direction. Stale or unrecognised data remains visible as a warning and is not offered as a live meal value.

## Direction mapping
- DoubleUp -> rapidly rising
- SingleUp -> rising
- FortyFiveUp -> slightly rising
- Flat -> stable
- FortyFiveDown -> slightly falling
- SingleDown -> falling
- DoubleDown -> rapidly falling

## Clinical boundary
This is observational/supportive data capture. It does not calculate correction insulin or recommend a pre-bolus interval. Dexcom remains the treatment-decision source. Trend and meal outcome evidence can inform later clinician discussion and the existing pre-bolus evidence protocol.
