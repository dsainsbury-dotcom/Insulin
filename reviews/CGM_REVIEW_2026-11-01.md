# CGM review - 1 November 2026

Published in app v2.10.8 on 2 November 2026. All three supplied files reviewed: Clarity PDF, Clarity CSV and icr-cgm-review-2026-11-01.csv. Raw personal exports are not committed.

## Comparison
19 Oct-1 Nov versus 5-18 Oct, each 14 days, from Clarity PDF page 19:
- TIR 85% versus 83%; mean 7.9 versus 8.2 mmol/L.
- GMI 6.7% versus 6.9%; CV 24.8% versus 25.6%.
- High 15% versus 16%; very high 0% rounded versus 1%.
- Low 0% rounded and very low <1% in both periods.
- Sensor active overview 97% versus 100%; latest AGP reports 97.9%.
Earlier raw glucose is absent, so earlier meal outcomes cannot be independently reconstructed.

## Raw and meal evidence
Latest CSV: 3,873 EGV readings, mean 7.8823, population CV 24.861%; 21 below 3.9, including 9 below 3.0; 4 above 13.9. LOW is encoded as 2.2 for this check, not a precise blood glucose measurement. Export ends 1 Nov 17:35 local. Dashboard timestamps converted from UTC to Europe/London across the 25 Oct clock change.
Latest window: 28 meals, 1 context. Earlier window: 30 meals. All meals use 1:15 and first-bite timing. Latest logged carbs 1,379.6g and actual meal insulin 89U; earlier 1,629.8g and 109U. These are incomplete logged totals, not verified intake or administered totals. 25/28 latest doses are within 0.5U of carbs/15; the other three record zero insulin.

## Interpretation
1:15 remains the working baseline for discussion; no global ratio, basal, correction, split-dose or timing change is supported here. Afternoon highs centre on 14:00-17:00. Delayed responses include 28 Oct rice/pork dinner (33g carbs, 44.8g fat, 2U; CGM 5.9 start, 8.3 at ~2h, 10.9 at ~4h, 8.7 at ~6h) and 29 Oct pizza (108.5g carbs, 52.9g fat, 7U; CGM 8.2 start, 7.7 at ~2h, 10.1 at ~4h, 8.9 at ~6h). These are observations, not proven mechanisms or clean isolated ratio tests. Overlapping meals on 27/28 Oct and zero-insulin snacks confound attribution.

## Sensor and safety
22 Oct 00:10: sensor LOW contradicted by finger-prick 7.0. 25 Oct ~20:11-20:39: sensor ~2.7-3.2 contradicted by finger-pricks 6.8-7.3. Associated low runs account for 18/21 low readings. Remaining isolated 3.7-3.8 readings on 19,22,23 Oct are unconfirmed, not automatically false. Preserve raw metrics. Discuss sensor reliability, low alert 3.3 and disabled signal-loss alert with team. No settings changed.

## Logging rules
Preserve [CONTEXT_EVENT], unknown carbs, test exclusions, unmatched estimated-dose exclusion and FP sensor-exception meaning. Curry context entered 1 Nov 02:39 refers to 7:30pm, not a known 02:39 meal. Dashboard remains primary structured meal source. McDonald's breakfast is 65g in app versus 55g in Clarity; 24 Oct sausage-roll/bread timing differs by ~21min. Missing insulin logs do not establish missed injections. Post-Whipple Type 3c context requires clinician-led interpretation of digestion and hypoglycaemia risk.
