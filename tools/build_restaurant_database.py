#!/usr/bin/env python3
"""Build v2.8.0 restaurant nutrition data from stable UK sources.

Safety rules:
- Production never depends on a live restaurant site.
- Greggs and PizzaExpress are rebuilt from their published nutrition PDFs.
- Burger King UK is a static verified snapshot transcribed from Burger King UK's
  June 2026 Nutritional Information report as independently indexed on 23 Aug 2026.
- McDonald's is intentionally excluded because its site proved too unreliable for
  a dependable verification pipeline.
- Rows with missing/ambiguous kcal, fat, carbohydrate or protein are never guessed.
"""
import io, json, re, requests
import pdfplumber
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

GREGGS='https://a.storyblok.com/f/94904/x/7dd8489dab/nutritional-information.pdf'
PEX='https://cdn.sanity.io/files/lj3txstz/production/230f6a921a100e32ad47e5f9f92e1fdbd01fef23.pdf'
BK_INFO='https://www.burgerking.co.uk/nutritional-info'
UA={'User-Agent':'Mozilla/5.0 (compatible; CGM-App-menu-verifier/2.8; +https://github.com/dsainsbury-dotcom/Insulin)'}
SESSION=requests.Session(); SESSION.headers.update(UA)
SESSION.mount('https://',HTTPAdapter(max_retries=Retry(total=4,connect=4,read=4,backoff_factor=1.5,status_forcelist=[429,500,502,503,504],allowed_methods=['GET'])))

# Greggs explicitly flagged these as recipe changes after the August guide.
# Until a newer official macro table is published they are omitted rather than stale-guessed.
GREGGS_RECIPE_UPDATE_EXCLUSIONS={
 'Southern Fried Potato Wedges',
 'BBQ Bites Meal Box',
 'Pumpkin Spice Latte with Salted Caramel Drizzle',
 'Iced Pumpkin Spice Latte with Salted Caramel Drizzle',
}

def get(url,timeout=60):
    r=SESSION.get(url,timeout=timeout); r.raise_for_status(); return r

def meal_type(name,cat=''):
    s=(name+' '+cat).lower()
    if 'pizza' in s:return 'Pizza'
    if any(x in s for x in ['fries','chips','wedges','hash brown','potato','onion rings']):return 'Potato / chips'
    if any(x in s for x in ['baguette','sandwich','burger','wrap','roll','toastie','flatbread','whopper','royale']):return 'Bread / sandwich'
    if any(x in s for x in ['cake','doughnut','donut','cookie','brownie','muffin','dessert','ice cream','sweet','danish','biscuit']):return 'Dessert / sweet food'
    if any(x in s for x in ['pasta','lasagna']):return 'Pasta'
    if 'rice' in s:return 'Rice / noodles'
    if 'curry' in s:return 'Curry'
    return 'Balanced / mixed'

def greggs():
    b=get(GREGGS).content; out=[]
    with pdfplumber.open(io.BytesIO(b)) as pdf:
        text='\n'.join(p.extract_text(x_tolerance=1,y_tolerance=3) or '' for p in pdf.pages)
    for ln in text.splitlines():
        ln=' '.join(ln.split())
        m=re.match(r'^(.+?)\s+(\d+(?:\.\d+)?)\s+\d+(?:\.\d+)?\s+\d+(?:\.\d+)?\s+\d+(?:\.\d+)?\s+(\d+(?:\.\d+)?)\s+\d+%\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+\d+%\s+\d+(?:\.\d+)?\s+\d+(?:\.\d+)?\s+\d+%\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+\d+%',ln)
        if not m: continue
        name,portion,kcal,fat100,fat,carb100,carbs=m.groups()
        if name in GREGGS_RECIPE_UPDATE_EXCLUSIONS: continue
        toks=re.findall(r'\d+(?:\.\d+)?%?',ln[len(name):]); plain=[x for x in toks if not x.endswith('%')]
        if len(plain)<15: continue
        try: protein=float(plain[-3])
        except (ValueError,IndexError): continue
        out.append(dict(restaurant='Greggs',category='National menu',name=name,portion=f'1 portion ({portion}g/ml)',carbs=float(carbs),fat=float(fat),protein=protein,kcal=float(kcal),mealType=meal_type(name),source='Greggs official Nutritional Information Guide',sourceDate='2026-08',sourceUrl='https://www.greggs.com/nutrition',evidence='official'))
    print('Greggs parsed',len(out),'excluded recipe-update rows',len(GREGGS_RECIPE_UPDATE_EXCLUSIONS))
    return out

def pizzaexpress():
    b=get(PEX).content; out=[]
    with pdfplumber.open(io.BytesIO(b)) as pdf:
        for p in pdf.pages[2:]:
            text=p.extract_text(x_tolerance=1,y_tolerance=3) or ''
            for ln in text.splitlines():
                ln=' '.join(ln.split())
                m=re.match(r'^(.+?)\s+(\d+(?:\.\d+)?)\s+\d+(?:\.\d+)?\s+(\d+(?:\.\d+)?)\s+\d+(?:\.\d+)?\s+(\d+(?:\.\d+)?)\s+\d+(?:\.\d+)?\s+\d+(?:\.\d+)?\s+(\d+(?:\.\d+)?)\s+\d+(?:\.\d+)?(?:\s|$)',ln)
                if not m: continue
                name,kcal,fat,carbs,protein=m.groups()
                if name.lower().startswith(('energy','per portion','adults need','july 2026')): continue
                out.append(dict(restaurant='PizzaExpress',category='Current menu',name=name,portion='1 published portion',carbs=float(carbs),fat=float(fat),protein=float(protein),kcal=float(kcal),mealType=meal_type(name),source='PizzaExpress official Nutritional Information - England, Wales & Scotland',sourceDate='2026-07',sourceUrl=PEX,evidence='official'))
    print('PizzaExpress parsed',len(out)); return out

def burger_king():
    # Verified Burger King UK snapshot. These values were transcribed from the official
    # June 2026 Nutritional Information report, control version KIT 6 NATIONAL - 18.06.2026 V1,
    # as independently indexed against burgerking.co.uk on 23 Aug 2026.
    raw=[
      ('Beef','Whopper',287,53,30,29,595),
      ('Beef','Double Whopper Cheese',395,50,54,56,914),
      ('Chicken','Chicken Royale',217,52,29,23,568),
      ('Chicken','Chicken Royale Bacon & Cheese',251,54,38,31,690),
      ('Chicken','BBQ Chicken Melts Burger',155,42,19,18,412),
      ('Chicken','BBQ Stacker Chicken Melts Burger Single',185,47,27,21,523),
      ('Chicken','BBQ Steakhouse Crispy Chicken',240,63,28,32,637),
      ('Chicken','Bacon Caesar Crispy Chicken',246,57,45,31,762),
      ('Sides','Fries (regular)',116,36,12,3.6,275),
      ('Sides','Onion Rings 6pc',90,28,9.8,4.6,225),
      ('Chicken','BBQ Chicken Fries 6pc',99,17,16,14,265),
      ('Chicken','BBQ Chicken Fries 20pc',330,56,53,46,884),
      ('Chicken','BBQ Cheese Loaded King Nuggets',189,37,27,22,483),
    ]
    out=[]
    for cat,name,grams,carbs,fat,protein,kcal in raw:
        out.append(dict(restaurant='Burger King',category=cat,name=name,portion=f'1 published portion ({grams}g)',carbs=float(carbs),fat=float(fat),protein=float(protein),kcal=float(kcal),mealType=meal_type(name,cat),source='Burger King UK Nutritional Information report, June 2026 (verified static snapshot)',sourceDate='2026-06-18',sourceUrl=BK_INFO,evidence='official-report-verified-static'))
    print('Burger King static verified rows',len(out)); return out

def dedupe(rows):
    seen=set(); out=[]
    for r in rows:
        k=(r['restaurant'].lower(),r['name'].lower(),r['portion'].lower())
        if k not in seen: seen.add(k); out.append(r)
    return out

rows=dedupe(greggs()+pizzaexpress()+burger_king())
rows.sort(key=lambda r:(r['restaurant'],r['category'],r['name']))
counts={}
for r in rows: counts[r['restaurant']]=counts.get(r['restaurant'],0)+1
print('COUNTS',counts,'TOTAL',len(rows))
if counts.get('Greggs',0)<80 or counts.get('PizzaExpress',0)<60 or counts.get('Burger King',0)<10 or "McDonald's" in counts:
    raise SystemExit('Safety threshold failed')
meta={'verified':'2026-09-05','counts':counts,'notes':['McDonalds intentionally excluded from v2.8.0','Burger King is static verified data; production performs no live restaurant scraping','Known Greggs post-August recipe-change rows are temporarily omitted rather than publishing stale macros'],'items':rows}
open('restaurant_foods_v2.8.0.json','w').write(json.dumps(meta,indent=2,ensure_ascii=False))
open('restaurant_foods_v2.8.0.js','w').write('window.RESTAURANT_FOODS_V280 = '+json.dumps(rows,ensure_ascii=False,separators=(',',':'))+';\n')
