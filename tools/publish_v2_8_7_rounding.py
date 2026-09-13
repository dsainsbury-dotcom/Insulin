from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path, old, new):
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected exactly one match in {path}, found {count}: {old[:100]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


# Production UI version markers. Keep restaurant_foods_v2.8.6.js because that filename is the
# current verified restaurant dataset asset, not the application release number.
replace_once("index.html", "<title>ICR Meal Dashboard v2.8.6</title>", "<title>ICR Meal Dashboard v2.8.7</title>")
replace_once("index.html", "ICR Meal Dashboard <small style=\"font-size:.48em;color:#0b5cab\">v2.8.6</small>", "ICR Meal Dashboard <small style=\"font-size:.48em;color:#0b5cab\">v2.8.7</small>")
replace_once("index.html", "<div class=\"badge\">v2.8.6 LIVE</div>", "<div class=\"badge\">v2.8.7 LIVE</div>")

# Dose prefill: use conventional nearest-whole-unit rounding. Actual insulin remains editable.
old_dose = "const d=c/i,r=Math.ceil(d);$('liveDose').textContent=`${d.toFixed(2)} U (round up to ${r} U)`;$('calc').textContent=`${c} g / ${i} = ${d.toFixed(2)} U calculated meal dose. No correction dose is calculated.`;if(!actualEdited)$('actualInsulin').value=r"
new_dose = "const d=c/i,r=Math.round(d);$('liveDose').textContent=`${d.toFixed(2)} U (nearest whole unit: ${r} U)`;$('calc').textContent=`${c} g / ${i} = ${d.toFixed(2)} U calculated meal dose. Whole-unit prefill rounds 0.00-0.49 down and 0.50-0.99 up. No correction dose is calculated.`;if(!actualEdited)$('actualInsulin').value=r"
replace_once("index.html", old_dose, new_dose)

# Correct the 11 Sep CGM interpretation: headline percentages are rounded and do not mean no lows occurred.
replace_once(
    "reviews/CGM_REVIEW_2026-09-11.md",
    "Compared with the 8 Sep review, TIR improves from 85% to 86%, average glucose remains 7.6 mmol/L, GMI remains 6.6%, and CV improves slightly from 30.4% to 30.0%. The current 14-day window records 0% low and 0% very low. All headline AGP goals remain achieved.",
    "Compared with the 8 Sep review, TIR improves from 85% to 86%, average glucose remains 7.6 mmol/L, GMI remains 6.6%, and CV improves slightly from 30.4% to 30.0%. The 14-day headline rounds low and very low to 0%, but the detailed daily/hourly statistics still contain low readings. All headline AGP goals remain achieved."
)
replace_once(
    "reviews/CGM_REVIEW_2026-09-11.md",
    "The earlier provisional concern about a possible 7 Sep evening low is not supported strongly enough to use as evidence that 1:15 is too strong. The updated 14-day Clarity summary records 0% low and 0% very low. Keep watching future clean meals, but do not change the global ratio on this basis.",
    "The 7 Sep evening low caution remains because the detailed Clarity statistics include low readings, including evening minima around 3.7 mmol/L. However, that evening involved about 50 g carbohydrate with 5 U within minutes, an effective dose around 1:10, plus overlapping earlier insulin/food. This is a caution about stronger/stacked dosing and whole-unit rounding, not evidence that the 1:15 baseline is globally too strong."
)
replace_once(
    "reviews/CGM_REVIEW_2026-09-11.md",
    "- Low / very low: 0% / 0%",
    "- Low / very low headline: 0% / 0% (rounded; detailed statistics still contain low readings)"
)

# Project continuity and release notes.
replace_once("PROJECT_BRAIN.md", "- Current production release: v2.8.4.", "- Current production release: v2.8.7.")
replace_once(
    "PROJECT_BRAIN.md",
    "- Whole-unit dose prefill remains editable to record the actual dose taken.",
    "- Whole-unit dose prefill remains editable to record the actual dose taken. From v2.8.7, calculated doses use nearest-whole-unit rounding: 0.00-0.49 down and 0.50-0.99 up."
)
replace_once(
    "PROJECT_BRAIN.md",
    "- Low 0%\n- Very low 0%",
    "- Low 0% headline (rounded; detailed statistics include low readings)\n- Very low 0% headline (rounded)"
)

changelog = ROOT / "CHANGELOG.md"
text = changelog.read_text(encoding="utf-8")
release = """# v2.8.7 - Nearest whole-unit meal-dose rounding\n\n- Changed the editable meal-dose prefill from always rounding up to conventional nearest-whole-unit rounding.\n- Calculated fractions 0.00-0.49 round down; 0.50-0.99 round up.\n- Working ICR remains 1:15 and the app still calculates meal dose only; no correction dose is added.\n- Actual insulin remains editable so the logged dose is always the dose actually taken.\n- Corrected the 11 Sep CGM review wording: the headline 0% low figure is rounded and detailed statistics still contain low readings.\n- Retained the 7 Sep low as a safety caution for stronger/stacked dosing rather than evidence that 1:15 is globally too strong.\n- Rollback branch: `backup/pre-v2.8.7-rounding-2026-09-13`.\n\n"""
if not text.startswith("# v2.8.7 - Nearest whole-unit meal-dose rounding"):
    changelog.write_text(release + text, encoding="utf-8")

# Also correct the stale 11 Sep changelog sentence if it is still present.
p = ROOT / "CHANGELOG.md"
text = p.read_text(encoding="utf-8")
text = text.replace(
    "- Current 14-day window records 0% low and 0% very low; all headline AGP goals remain achieved.",
    "- Headline 14-day low and very-low values round to 0%; detailed daily/hourly statistics still contain low readings, while headline AGP goals remain achieved."
)
p.write_text(text, encoding="utf-8")

# Lightweight release assertions.
index = (ROOT / "index.html").read_text(encoding="utf-8")
for marker in ["v2.8.7 LIVE", "Math.round(d)", "0.00-0.49 down and 0.50-0.99 up"]:
    if marker not in index:
        raise SystemExit(f"Missing release marker: {marker}")

# Expected whole-unit behaviour around the threshold.
for dose, expected in [(3.01, 3), (3.49, 3), (3.50, 4), (3.99, 4), (4.00, 4)]:
    rounded = int(dose + 0.5)
    if rounded != expected:
        raise SystemExit(f"Rounding assertion failed: {dose} -> {rounded}, expected {expected}")

print("v2.8.7 publication changes applied successfully")
