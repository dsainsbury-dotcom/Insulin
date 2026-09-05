#!/usr/bin/env python3
import json
from pathlib import Path

DATA = Path('restaurant_foods_v2.8.0.js')
MANIFEST = Path('restaurant_foods_v2.8.0_verification.json')
PREFIX = 'window.RESTAURANT_FOODS_V280 = '

raw = DATA.read_text(encoding='utf-8').strip()
if not raw.startswith(PREFIX) or not raw.endswith(';'):
    raise SystemExit('Unexpected v2.8.0 restaurant data format')
rows = json.loads(raw[len(PREFIX):-1])


def find(restaurant, name, category=None):
    matches = [r for r in rows if r.get('restaurant') == restaurant and r.get('name') == name and (category is None or r.get('category') == category)]
    if len(matches) != 1:
        suffix = f' / {category}' if category else ''
        raise SystemExit(f'Expected exactly one row for {restaurant} / {name}{suffix}, found {len(matches)}')
    return matches[0]

# Greggs current-source corrections/checks, 5 Sep 2026.
wedges = find('Greggs', 'Southern Fried Potato Wedges')
wedges.update({
    'portion': '1 portion (150g)', 'carbs': 42, 'fat': 9.6, 'protein': 4.0, 'kcal': 278,
    'source': 'Greggs official current product page', 'sourceDate': '2026-09-05',
    'evidence': 'official-current-product-page', 'status': 'core',
    'sourceUrl': 'https://www.greggs.com/menu/product/southern-fried-potato-wedges-1001012'
})

bbq = find('Greggs', 'BBQ Bites Meal Box')
bbq.update({
    'carbs': 64, 'fat': 23, 'protein': 23, 'kcal': 566,
    'source': 'Greggs official current nutrition guide', 'sourceDate': '2026-09-05',
    'evidence': 'official-current-guide', 'status': 'core',
    'sourceUrl': 'https://www.greggs.com/nutrition'
})

# Add currently verified autumn products only where Greggs publishes full macros.
def upsert(row):
    for i, existing in enumerate(rows):
        if existing.get('restaurant') == row['restaurant'] and existing.get('name') == row['name']:
            rows[i] = row
            return
    rows.append(row)

upsert({
    'restaurant': 'Greggs', 'category': 'Savouries', 'name': 'Steak & Stilton® Bake',
    'portion': '1 bake (152g)', 'carbs': 30, 'fat': 30, 'protein': 17, 'kcal': 465,
    'mealType': 'Balanced / mixed meal', 'source': 'Greggs official current product page',
    'sourceDate': '2026-09-05', 'evidence': 'official-current-product-page', 'status': 'limited',
    'sourceUrl': 'https://www.greggs.com/menu/product/steak-stilton-bake-1003649'
})
upsert({
    'restaurant': 'Greggs', 'category': 'Hot Drinks',
    'name': 'Regular Pumpkin Spice Latte with Salted Caramel Drizzle',
    'portion': '1 regular (368.5g)', 'carbs': 29, 'fat': 7.4, 'protein': 8.1, 'kcal': 214,
    'mealType': 'Balanced / mixed meal', 'source': 'Greggs official current product page',
    'sourceDate': '2026-09-05', 'evidence': 'official-current-product-page', 'status': 'limited',
    'sourceUrl': 'https://www.greggs.com/menu/product/regular-pumpkin-spice-latte-with-salted-caramel-drizzle-1001487'
})

# Static-source verification. McDonald's is deliberately verified from the frozen UK dataset,
# not by live scraping, because their site repeatedly times out from GitHub Actions.
checks = [
    ('Greggs', 'Southern Fried Potato Wedges', None, 278, 42, 9.6, 4.0),
    ('Greggs', 'BBQ Bites Meal Box', None, 566, 64, 23, 23),
    ('Greggs', 'Steak & Stilton® Bake', None, 465, 30, 30, 17),
    ('PizzaExpress', 'Margherita', 'Pizza - Classic', 711, 91.7, 22.1, 35.1),
    ("McDonald's", 'McCrispy', None, 484, 53, 18, 26),
    ("McDonald's", 'Big Mac', None, 509, 41, 25, 27),
]
verified = []
for restaurant, name, category, kcal, carbs, fat, protein in checks:
    r = find(restaurant, name, category)
    actual = (r.get('kcal'), r.get('carbs'), r.get('fat'), r.get('protein'))
    expected = (kcal, carbs, fat, protein)
    if actual != expected:
        raise SystemExit(f'Spot-check failed for {restaurant} / {name}: {actual} != {expected}')
    verified.append({'restaurant': restaurant, 'name': name, 'category': category, 'kcal': kcal, 'carbs': carbs, 'fat': fat, 'protein': protein})

counts = {}
for r in rows:
    for key in ('restaurant','name','carbs','fat','protein','kcal','source','sourceDate','sourceUrl','evidence'):
        if key not in r or r[key] in (None, ''):
            raise SystemExit(f'Missing required field {key}: {r}')
    counts[r['restaurant']] = counts.get(r['restaurant'], 0) + 1

minimums = {'Greggs': 120, 'PizzaExpress': 100, "McDonald's": 60}
for restaurant, minimum in minimums.items():
    if counts.get(restaurant, 0) < minimum:
        raise SystemExit(f'{restaurant} count {counts.get(restaurant,0)} below safety minimum {minimum}')

rows.sort(key=lambda r: (r['restaurant'], r.get('category',''), r['name']))
DATA.write_text(PREFIX + json.dumps(rows, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
MANIFEST.write_text(json.dumps({
    'release': 'v2.8.0',
    'verifiedDate': '2026-09-05',
    'status': 'stable-baseline',
    'method': 'verified static UK nutrition data; no live McDonalds scrape required',
    'counts': counts,
    'spotChecks': verified,
    'notes': [
        'Greggs Southern Fried Potato Wedges refreshed from current official product page.',
        'Greggs BBQ Bites Meal Box rechecked against the current official nutrition guide.',
        'Greggs Steak & Stilton Bake and Regular Pumpkin Spice Latte added from current official product pages.',
        'McDonalds UK dataset is frozen/static and spot-checked against official UK product nutrition; live scraping is not a release gate.'
    ]
}, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print('v2.8.0 static verification passed', counts)
