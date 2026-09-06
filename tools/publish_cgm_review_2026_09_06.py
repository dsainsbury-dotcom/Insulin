from pathlib import Path
import re

index = Path('index.html')
s = index.read_text(encoding='utf-8')

# Visible production-content update: advance patch version only.
s = s.replace('v2.8.2', 'v2.8.3')

pattern = re.compile(
    r'<section class="card"><h2>My CGM progress</h2>.*?</section>\s*'
    r'<section class="card"><h2>Clinical goals</h2>.*?</section>',
    re.S,
)

replacement = '''<section class="card"><h2>My CGM progress</h2><div class="progressGrid"><div class="snapshot"><strong>Latest review - 6 Sep 2026</strong><div class="signalGrid" style="margin-top:10px"><div class="signal"><span>Time in range</span><strong>84%</strong></div><div class="signal"><span>Average glucose</span><strong>7.7</strong></div><div class="signal"><span>GMI</span><strong>6.6%</strong></div><div class="signal"><span>CV</span><strong>29.9%</strong></div></div><div class="reassure"><strong>Coach summary:</strong> control remains strong, although variability has edged up since the 2 Sep review: TIR 85% to 84%, average glucose stays 7.7, GMI stays 6.6% and CV moves 28.8% to 29.9%. All headline AGP goals remain achieved. <strong>ICR verdict:</strong> 1:15 remains the best-supported working baseline. Across the 38 genuine app meal records there is still no six-hour post-meal low signal saying 1:15 is too strong. The poorer excursions are mixed and are more strongly linked to rapid starch, high starting glucose, overlapping eating and delayed/high-fat effects than to one clear global ICR failure.</div></div><div><div class="learning good"><strong>What is working</strong><br>TIR is 84%, GMI 6.6% and CV 29.9%, all inside the AGP goals. In a stricter set of 13 relatively clean grouped eating episodes close to 1:15, there were zero post-meal lows. Recent strong examples include the 5 Sep PizzaExpress meal and 4 Sep fish &amp; chips, both first-bite doses with controlled six-hour outcomes.</div><div class="learning watch"><strong>What to watch</strong><br>Variability has risen slightly and selected rapid-starch or overlapping episodes can still produce large excursions. The 2 Sep Doritos + Hula Hoops entries must be treated as one episode; together they peaked at 18.2 mmol/L before returning to about 7.1 by four hours and 6.4 by six hours. High-fat meals can still show delayed rises even when their overall result is good.</div><div class="learning info"><strong>Data quality</strong><br>Dexcom carb and fast-insulin entries are used as a cross-check, while our app remains the primary meal-context record. Closely spaced app entries are grouped before judging outcomes. The 27 Aug overnight low remains a documented faulty-sensor exception, and the 3 Sep sensor-pull event is also treated as a data-quality exception.</div></div></div></section>
<section class="card"><h2>Clinical goals</h2><div class="goalGrid"><div class="goalItem"><div><strong>Time in range</strong><div class="goalMeta">Goal &gt;70% | Latest 84%</div></div><span class="tick">ACHIEVED</span></div><div class="goalItem"><div><strong>CV</strong><div class="goalMeta">Goal &lt;36% | Latest 29.9%</div></div><span class="tick">ACHIEVED</span></div><div class="goalItem"><div><strong>GMI</strong><div class="goalMeta">Goal &lt;7% | Latest 6.6%</div></div><span class="tick">ACHIEVED</span></div></div></section>'''

s2, n = pattern.subn(replacement, s, count=1)
if n != 1:
    raise SystemExit(f'Expected exactly one CGM Progress + Clinical goals block, replaced {n}')
index.write_text(s2, encoding='utf-8')

changelog = Path('CHANGELOG.md')
ct = changelog.read_text(encoding='utf-8')
entry = '''# v2.8.3 - CGM 3-file review update - 6 Sep 2026
- Processed the complete Dexcom Clarity PDF + raw Dexcom CSV + ICR Meal Dashboard CSV review.
- Updated CGM Progress to TIR 84%, average glucose 7.7 mmol/L, GMI 6.6% and CV 29.9%.
- Kept 1:15 as the evidence-supported working ICR baseline; no six-hour post-meal low signal currently supports winding back to 1:20.
- Added richer analysis using the app as the primary meal-context record and Dexcom meal/insulin entries as corroboration.
- Grouped closely spaced food records into eating episodes before judging ICR response.
- Added review record `reviews/CGM_REVIEW_2026-09-06.md`.
- Rollback branch: `backup/pre-cgm-review-2026-09-06`.
- No change to insulin calculation logic, correction-dose logic, Nightscout analysis or clinical automation.

'''
if not ct.startswith('# v2.8.3'):
    changelog.write_text(entry + ct, encoding='utf-8')

brain = Path('PROJECT_BRAIN.md')
if brain.exists():
    bt = brain.read_text(encoding='utf-8').replace('v2.8.2', 'v2.8.3')
    brain.write_text(bt, encoding='utf-8')
