# CGM Review - 6 Sep 2026

## Review set
Complete 3-file review using:
- Dexcom Clarity PDF covering 24 Aug 2026 through 6 Sep 2026
- Dexcom raw CSV export dated 6 Sep 2026
- ICR Meal Dashboard CSV export dated 6 Sep 2026

The Dexcom meal/carb and fast-insulin entries are treated as a useful cross-check. The ICR Meal Dashboard export remains the primary meal record because it contains the richer real-world context including food description, meal type, fat, calculated dose, actual dose, ICR, bolus timing, CGM trend, Nightscout source and notes.

The app export contains 39 rows. The TEST row is excluded, leaving 38 genuine meal records. Closely spaced entries are grouped into eating episodes where needed so the same glucose excursion is not counted as multiple independent ICR observations.

## Headline Dexcom metrics
- Time in range: 84%
- Average glucose: 7.7 mmol/L
- GMI: 6.6%
- CV: 29.9%
- Very high: 2%
- High: 13%
- Low: 1%
- Very low: <1%
- CGM active: 98.4%

Compared with the previous app review dated 2 Sep: TIR moved 85% to 84%, average glucose stayed 7.7 mmol/L, GMI stayed 6.6%, and CV moved 28.8% to 29.9%. Very high time moved 1% to 2%; high time stayed 13%.

Compared with Dexcom's preceding 14-day period (10-23 Aug): TIR moved 87% to 84%, average glucose 7.5 to 7.7 mmol/L, GMI 6.5% to 6.6%, and CV 27.5% to 29.9%.

This is a modest deterioration in variability/TIR, not a collapse in control. The headline AGP goals remain achieved.

## Sensor-quality exception
The 27 Aug overnight low period must not be treated as genuine hypoglycaemia evidence. The Dexcom record explicitly documents a faulty sensor and a finger-prick glucose of 8.0 mmol/L while the sensor was reading low.

The 3 Sep record also documents that the sensor was accidentally pulled off. This is a data-quality event and should be considered when interpreting that day's trace around the replacement period.

## ICR verdict
Current working ICR remains 1:15.

This review still does not support winding back to 1:20, and it does not provide clean repeated evidence to strengthen the global ratio either.

Key evidence:
- Across the 38 genuine app meal records, no post-meal glucose below 3.9 mmol/L was found in the six-hour outcome windows in the raw Dexcom trace.
- In a stricter subset of 13 relatively clean grouped eating episodes that were close to a 1:15 dose, started in range, had no new app meal for at least four hours, and had a usable six-hour trace, there were zero post-meal lows.
- Four of those 13 cleaner episodes had at least roughly one hour above 10 mmol/L, so the signal is not that 1:15 is globally too strong.
- The weaker outcomes are mixed. Some are linked to rapid starch, high starting glucose, closely spaced meals, sweets, or delayed/high-fat effects rather than one consistent global under-dosing pattern.

Any insulin-setting change remains a discussion point for the diabetes team, not an automatic app adjustment.

## Meal evidence and reconstruction
### Stronger recent examples
- 5 Sep PizzaExpress Bruschetta Originale + Lasagna Classica: 104.8 g carbs, 47.8 g fat, 7 U, stable starting trend, first-bite dosing. Raw Dexcom start was about 6.4 mmol/L, peak about 9.2, 2 h about 6.2, 4 h about 8.8, 6 h about 6.9, with no reading above 10 and no low. This is useful evidence that a sizeable high-fat restaurant meal can still land well on the current approach.
- 4 Sep Fish & chips: 150 g carbs, 10 U, stable trend, first-bite dosing. Start about 4.8, peak about 9.0, 2 h about 7.3, 4 h about 6.9 and 6 h about 8.9. No low and no time above 10 in the raw trace. A delayed rise was present, which fits the known high-fat pattern, but the excursion remained controlled.
- 3 Sep burger: 72 g carbs, 68 g fat, 5 U. Start about 6.2 and peak about 8.8 with no low and no time above 10 over the six-hour window.
- 3 Sep Juicy lobster: 60 g carbs, 4 U. Start about 8.0 and the subsequent six-hour trace stayed below the starting level, with no low.

### Important confounded or caution examples
- 2 Sep Doritos + Hula Hoops were logged about one minute apart and must be treated as one eating episode: 49.4 g carbs and 3 U combined. The trace peaked at 18.2 mmol/L at about 99 minutes and spent about 175 minutes above 10 before returning to about 7.1 by four hours and 6.4 by six hours. This is a poor outcome, but it is one rapid-starch/snack episode and is not enough by itself to change the global ICR.
- 31 Aug pasty, pad thai and sweets occurred in a compressed afternoon/evening period with high starting glucose and overlapping food. The resulting prolonged high cannot be assigned cleanly to one meal or one ICR decision.
- 1 Sep ribs and gyoza were close together while glucose was already above 10, so they are not clean ratio-setting observations.
- 29 Aug Selfridges and Chinese episodes were high-fat and less than three hours apart, so delayed digestion and overlap make the individual outcomes difficult to separate.
- 24 Aug evening meal and chocolate were only about 85 minutes apart. They should not be treated as independent ICR trials.

## Timing evidence
The newest app records now include the CGM trend and, for some meals, the Nightscout source timestamp. This materially improves future analysis.

Current evidence still does not justify a blanket move away from first-bite dosing. Several first-bite meals produced strong outcomes, including the 5 Sep PizzaExpress meal and 4 Sep fish & chips. Other meals produced highs, but they are not yet clean or consistent enough to establish a universal pre-bolus rule in the post-Whipple context.

## Current interpretation
- PROVEN REPEATEDLY: headline control remains above the standard AGP targets, including TIR >70%, GMI <7% and CV <36%.
- LIKELY: 1:15 remains the best-supported working global baseline.
- LIKELY: high-fat/high-carb meals can produce delayed rises, but the size of that effect varies considerably by meal.
- LIKELY: rapid starch and closely spaced eating episodes are currently more important sources of poor excursions than evidence of a globally weak ICR.
- UNDER INVESTIGATION: whether particular rapid-starch/bread/snack meals need their own timing or dosing approach.
- UNDER INVESTIGATION: whether stable-trend first-bite meals continue to outperform enough times to become a stronger personal rule.
- ANALYSIS RULE: group closely spaced foods into one eating episode before judging the response.
- ANALYSIS RULE: use Dexcom carb/insulin entries as corroboration, but use the ICR Meal Dashboard as the primary meal-context record.
- ANALYSIS RULE: exclude documented sensor faults and unmatched/unclear insulin events from clean ICR evidence.

## App progress summary
For the CGM Progress tab:
- Latest review: 6 Sep 2026
- TIR: 84%
- Average glucose: 7.7 mmol/L
- GMI: 6.6%
- CV: 29.9%
- Working ICR verdict: keep 1:15 as the evidence-supported baseline for now
- Main watch area: variability and selected rapid-starch/overlapping meal excursions, not a post-meal low signal
