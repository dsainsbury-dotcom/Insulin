from pathlib import Path
import re

index = Path('index.html')
s = index.read_text(encoding='utf-8')

# Correct production patch version without renaming the existing v2.8.3 history item.
s = s.replace('<title>ICR Meal Dashboard v2.8.3</title>', '<title>ICR Meal Dashboard v2.8.4</title>', 1)
s = s.replace('ICR Meal Dashboard <small style="font-size:.48em;color:#0b5cab">v2.8.3</small>', 'ICR Meal Dashboard <small style="font-size:.48em;color:#0b5cab">v2.8.4</small>', 1)
s = s.replace('<div class="badge">v2.8.3 LIVE</div>', '<div class="badge">v2.8.4 LIVE</div>', 1)

progress_pattern = re.compile(
    r'<section class="card"><h2>My CGM progress</h2>.*?</section>\s*'
    r'<section class="card"><h2>Clinical goals</h2>.*?</section>',
    re.S,
)

progress_replacement = '''<section class="card"><h2>My CGM progress</h2><div class="progressGrid"><div class="snapshot"><strong>Latest review - 6 Sep 2026</strong><div class="signalGrid" style="margin-top:10px"><div class="signal"><span>Time in range</span><strong>84%</strong></div><div class="signal"><span>Average glucose</span><strong>7.7</strong></div><div class="signal"><span>GMI</span><strong>6.6%</strong></div><div class="signal"><span>CV</span><strong>29.9%</strong></div></div><div class="reassure"><strong>Coach summary:</strong> control remains strong, although variability has edged up since the 2 Sep review: TIR 85% to 84%, average glucose stays 7.7, GMI stays 6.6% and CV moves 28.8% to 29.9%. All headline AGP goals remain achieved. <strong>ICR verdict:</strong> 1:15 remains the best-supported working baseline. Across the 38 genuine app meal records there is still no six-hour post-meal low signal saying 1:15 is too strong. The poorer excursions are mixed and are more strongly linked to rapid starch, high starting glucose, overlapping eating and delayed/high-fat effects than to one clear global ICR failure.</div></div><div><div class="learning good"><strong>What is working</strong><br>TIR is 84%, GMI 6.6% and CV 29.9%, all inside the AGP goals. In a stricter set of 13 relatively clean grouped eating episodes close to 1:15, there were zero post-meal lows. Recent strong examples include the 5 Sep PizzaExpress meal and 4 Sep fish &amp; chips, both first-bite doses with controlled six-hour outcomes.</div><div class="learning watch"><strong>What to watch</strong><br>Variability has risen slightly and selected rapid-starch or overlapping episodes can still produce large excursions. The 2 Sep Doritos + Hula Hoops entries must be treated as one episode; together they peaked at 18.2 mmol/L before returning to about 7.1 by four hours and 6.4 by six hours. High-fat meals can still show delayed rises even when their overall result is good.</div><div class="learning info"><strong>Data quality</strong><br>Dexcom carb and fast-insulin entries are used as a cross-check, while our app remains the primary meal-context record. Closely spaced app entries are grouped before judging outcomes. The 27 Aug overnight low remains a documented faulty-sensor exception, and the 3 Sep sensor-pull event is also treated as a data-quality exception.</div></div></div></section>
<section class="card"><h2>Clinical goals</h2><div class="goalGrid"><div class="goalItem"><div><strong>Time in range</strong><div class="goalMeta">Goal &gt;70% | Latest 84%</div></div><span class="tick">ACHIEVED</span></div><div class="goalItem"><div><strong>CV</strong><div class="goalMeta">Goal &lt;36% | Latest 29.9%</div></div><span class="tick">ACHIEVED</span></div><div class="goalItem"><div><strong>GMI</strong><div class="goalMeta">Goal &lt;7% | Latest 6.6%</div></div><span class="tick">ACHIEVED</span></div></div></section>'''

s, n = progress_pattern.subn(progress_replacement, s, count=1)
if n != 1:
    raise SystemExit(f'Expected exactly one CGM Progress + Clinical goals block, replaced {n}')

learn_pattern = re.compile(r'<section class="card"><h2>What I\'ve learned about Darren\'s diabetes</h2>.*?</section>', re.S)
learn_replacement = '''<section class="card"><h2>What I've learned about Darren's diabetes</h2><div class="learnGrid"><div class="learnItem"><span class="evidence ev-proven">PROVEN REPEATEDLY</span><strong>Time in range remains well above the 70% goal across recent reviews.</strong></div><div class="learnItem"><span class="evidence ev-likely">LIKELY</span><strong>1:15 remains the best-supported working ICR. The latest 3-file review still shows no six-hour post-meal low pattern suggesting it is too strong.</strong></div><div class="learnItem"><span class="evidence ev-likely">LIKELY</span><strong>High-fat meals can cause delayed rises, while rapid-starch and overlapping eating episodes are currently more likely to produce the largest excursions.</strong></div><div class="learnItem"><span class="evidence ev-investigate">UNDER INVESTIGATION</span><strong>Rapid starch, bread and snack-type meals may need their own timing or dosing pattern, but there is not yet enough clean repeated evidence to change the global ICR.</strong></div><div class="learnItem"><span class="evidence ev-investigate">UNDER INVESTIGATION</span><strong>Stable-trend first-bite meals are now being tracked more precisely using the new CGM trend and Nightscout context.</strong></div><div class="learnItem"><span class="evidence ev-rule">ANALYSIS RULE</span><strong>Closely spaced foods are grouped into one eating episode before judging ICR response, and Dexcom carb/insulin entries are corroboration while the app remains the primary meal-context record.</strong></div><div class="learnItem"><span class="evidence ev-rule">ANALYSIS RULE</span><strong>Documented sensor faults, unmatched insulin events and unclear nutrition are excluded from clean ratio-setting evidence.</strong></div></div></section>'''
s, n = learn_pattern.subn(learn_replacement, s, count=1)
if n != 1:
    raise SystemExit(f'Expected one learned section, replaced {n}')

timeline_pattern = re.compile(r'<section class="card"><h2>Review timeline - last 5 uploads</h2>.*?</section>', re.S)
timeline_replacement = '''<section class="card"><h2>Review timeline - last 5 uploads</h2><div class="timeline"><div class="review"><div class="reviewDate">6 Sep 2026</div><div class="reviewMetrics"><span class="chip">TIR 84%</span><span class="chip">Avg 7.7</span><span class="chip">GMI 6.6%</span><span class="chip">CV 29.9%</span></div></div><div class="review"><div class="reviewDate">2 Sep 2026</div><div class="reviewMetrics"><span class="chip">TIR 85%</span><span class="chip">Avg 7.7</span><span class="chip">GMI 6.6%</span><span class="chip">CV 28.8%</span></div></div><div class="review"><div class="reviewDate">29 Aug 2026</div><div class="reviewMetrics"><span class="chip">TIR 88%</span><span class="chip">Avg 7.5</span><span class="chip">GMI 6.5%</span><span class="chip">CV 27.1%</span></div></div><div class="review"><div class="reviewDate">28 Aug 2026</div><div class="reviewMetrics"><span class="chip">TIR 88%</span><span class="chip">Avg 7.4</span><span class="chip">GMI 6.5%</span><span class="chip">CV 27.8%</span></div></div><div class="review"><div class="reviewDate">22 Aug 2026</div><div class="reviewMetrics"><span class="chip">TIR 87%</span><span class="chip">Avg 7.5</span><span class="chip">GMI 6.6%</span></div></div></div></section>'''
s, n = timeline_pattern.subn(timeline_replacement, s, count=1)
if n != 1:
    raise SystemExit(f'Expected one timeline section, replaced {n}')

marker = '<div class="versionGrid"><div class="versionItem"><strong>v2.8.3 - Live CGM autofill reliability</strong>'
new_item = '<div class="versionGrid"><div class="versionItem"><strong>v2.8.4 - 6 Sep CGM 3-file review</strong><ul><li>Processed the Dexcom Clarity PDF, raw Dexcom CSV and full ICR Meal Dashboard export together.</li><li>Updated CGM Progress to TIR 84%, average 7.7 mmol/L, GMI 6.6% and CV 29.9%.</li><li>Retained 1:15 as the working evidence-supported ICR because the review still shows no six-hour post-meal low signal.</li><li>Uses the app as the primary meal-context record, groups overlapping food entries into eating episodes, and uses Dexcom meal/insulin logging as corroboration.</li></ul></div><div class="versionItem"><strong>v2.8.3 - Live CGM autofill reliability</strong>'
if marker in s and 'v2.8.4 - 6 Sep CGM 3-file review' not in s:
    s = s.replace(marker, new_item, 1)

index.write_text(s, encoding='utf-8')

changelog = Path('CHANGELOG.md')
ct = changelog.read_text(encoding='utf-8')
ct = ct.replace('# v2.8.3 - CGM 3-file review update - 6 Sep 2026', '# v2.8.4 - CGM 3-file review update - 6 Sep 2026', 1)
changelog.write_text(ct, encoding='utf-8')

brain = Path('PROJECT_BRAIN.md')
if brain.exists():
    bt = brain.read_text(encoding='utf-8')
    bt = re.sub(r'- Current production release: v[^.]+\.[^.]+\.[^.]+\.', '- Current production release: v2.8.4.', bt, count=1)
    brain.write_text(bt, encoding='utf-8')

# Trigger note: final publication pass after workflow verification correction.
