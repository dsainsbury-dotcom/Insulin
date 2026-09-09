from pathlib import Path
import json

ROOT=Path('.')
old=ROOT/'restaurant_foods_v2.8.0.js'
raw=old.read_text()
prefix='window.RESTAURANT_FOODS_V280 = '
assert raw.startswith(prefix)
base=json.loads(raw[len(prefix):].rstrip().rstrip(';'))

menu_url='https://www.subway.com/en-gb/menu/category/436'
jan_url='https://www.subway.com/en-gb/-/media/emea/europe/uk/nutrition/2026/ukiandroinutritionalinformationjan2026.pdf'
foot_rule='https://www.subway.com/en-gb/-/media/emea/europe/uk/nutrition/tuki-builds-and-ingredients-nutritional-information-november-2025-website.pdf'

def item(cat,name,portion,carbs,fat,protein,kcal,source,source_date,url,evidence='official'):
    return {'restaurant':'Subway','category':cat,'name':name,'portion':portion,'carbs':float(carbs),'fat':float(fat),'protein':float(protein),'kcal':float(kcal),'mealType':'Bread / sandwich' if 'Sub' in cat else ('Potato / chips' if 'Side' in cat or 'Jacket' in cat else 'Dessert / sweet food'),'source':source,'sourceDate':source_date,'sourceUrl':url,'evidence':evidence}

sub6=[
 item('Subs - 6 inch','Chicken Tikka','1 published 6-inch portion (185g)',42,3.7,26,302,'Subway UK live product nutrition page, checked Sep 2026','2026-09-09','https://www.subway.com/en-gb/menu/product/4966/'),
 item('Subs - 6 inch','Honey Mustard BBQ','1 published 6-inch portion (258g)',44,15,28,430,'Subway UK live product nutrition page, checked Sep 2026','2026-09-09','https://www.subway.com/en-gb/menu/product/13447/'),
 item('Subs - 6 inch','Garlic Cheese Steak','1 published 6-inch portion (272g)',51,27,24,539,'Subway UK live product nutrition page, checked Sep 2026','2026-09-09','https://www.subway.com/en-gb/menu/product/12176/'),
 item('Subs - 6 inch','Tex Mexan','1 published 6-inch portion (260g)',58,21,32,556,'Subway UK live product nutrition page, checked Sep 2026','2026-09-09','https://www.subway.com/en-gb/menu/product/11086/'),
 item('Subs - 6 inch','Veggie Delite','1 published 6-inch build (163g)',42,2.4,8.3,227,'Subway UK official nutrition PDF, Jan 2026; item confirmed on current Sep 2026 UK menu','2026-01-01',jan_url),
 item('Subs - 6 inch','Classic B.M.T.','1 published 6-inch build (139g)',41,16,20,386,'Subway UK official nutrition PDF, Jan 2026; item confirmed on current Sep 2026 UK menu','2026-01-01',jan_url),
 item('Subs - 6 inch','Spicy Italian','1 published 6-inch build (186g)',43,27,22,498,'Subway UK official nutrition PDF, Jan 2026; item confirmed on current Sep 2026 UK menu','2026-01-01',jan_url),
 item('Subs - 6 inch','Tuna Mayo','1 published 6-inch build (208g)',51,16,19,427,'Subway UK official nutrition PDF, Jan 2026; item confirmed on current Sep 2026 UK menu','2026-01-01',jan_url),
]
foot=[]
for x in sub6:
    y=dict(x)
    y['category']='Subs - Footlong'
    y['name']=x['name']+' - Footlong'
    y['portion']='1 Footlong (2 x published 6-inch serving)'
    for k in ('carbs','fat','protein','kcal'): y[k]=round(x[k]*2,1)
    y['source']=x['source']+'; Footlong values doubled using Subway UK official rule: one Footlong = two 6-inch servings'
    y['sourceUrl']=foot_rule
    y['evidence']='official-derived'
    foot.append(y)

extras=[
 item('Jacket Potatoes','Chicken Breast & Cheese Jacket Potato','1 published portion (395g)',53,18,30,498,'Subway UK live product nutrition page, checked Sep 2026','2026-09-09','https://www.subway.com/en-gb/menu/product/13627/'),
 item('Sides','Nacho Chicken Bites - 6 pieces','1 published portion (162g)',32,19,24,405,'Subway UK official nutrition PDF, Jan 2026','2026-01-01',jan_url),
 item('Sides','Doritos Lightly Salted Nachos','1 published portion (207g)',60,30,19,590,'Subway UK official nutrition PDF, Jan 2026','2026-01-01',jan_url),
 item('Sides','Doritos Tangy Cheese Nachos','1 published portion (207g)',55,34,19,615,'Subway UK official nutrition PDF, Jan 2026','2026-01-01',jan_url),
 item('Sides','Doritos Chilli Heat Wave Nachos','1 published portion (206g)',57,34,19,611,'Subway UK official nutrition PDF, Jan 2026','2026-01-01',jan_url),
 item('Cookies & Treats','Chocolate Chunk Cookie','1 cookie (45g)',28,10,2.3,214,'Subway UK live product nutrition page, checked Sep 2026','2026-09-09','https://www.subway.com/en-gb/menu/product/5323'),
]
for e in extras:
    if e['category']=='Jacket Potatoes': e['mealType']='Potato / chips'

# Replace any prior Subway rows, then append the verified starter set.
base=[x for x in base if x.get('restaurant')!='Subway'] + sub6 + foot + extras
new=ROOT/'restaurant_foods_v2.8.6.js'
new.write_text('window.RESTAURANT_FOODS_V280 = '+json.dumps(base,separators=(',',':'),ensure_ascii=False)+';\n')

p=ROOT/'index.html'
s=p.read_text()
s=s.replace('ICR Meal Dashboard v2.8.5','ICR Meal Dashboard v2.8.6')
s=s.replace('v2.8.5</small>','v2.8.6</small>')
s=s.replace('v2.8.5 LIVE','v2.8.6 LIVE')
s=s.replace('restaurant_foods_v2.8.0.js','restaurant_foods_v2.8.6.js')
s=s.replace('Greggs, PizzaExpress & Burger King UK','Greggs, PizzaExpress, Burger King & Subway UK')
s=s.replace('.restaurantChains{display:grid;grid-template-columns:repeat(3,1fr)', '.restaurantChains{display:grid;grid-template-columns:repeat(4,1fr)')
p.write_text(s)

c=ROOT/'CHANGELOG.md'
cs=c.read_text()
entry='''# v2.8.6 - Subway UK restaurant foods\n\n- Added Subway UK to the restaurant-food browser.\n- Added verified 6-inch Sub entries and Footlong versions using Subway's published rule that a Footlong is two 6-inch servings.\n- Added a current Chicken Breast & Cheese Jacket Potato, Subway sides and Chocolate Chunk Cookie.\n- Live/current product-page values are used where available; older official 2026 UK nutrition snapshots are clearly source-dated in the app.\n- Current Subway UK menu presence was checked before inclusion.\n- No insulin, ICR, correction-dose, Nightscout or CGM analysis logic changed.\n\n'''
if not cs.startswith('# v2.8.6'):
    c.write_text(entry+cs)

b=ROOT/'PROJECT_BRAIN.md'
bs=b.read_text()
entryb='''\n\n## v2.8.6 - Subway UK restaurant foods (9 Sep 2026)\n- Subway added to the restaurant browser with a verified starter set.\n- Includes 6-inch Subs, derived Footlong versions, a Jacket Potato, sides and Chocolate Chunk Cookie.\n- Current product pages are preferred; other entries retain explicit official-source dates.\n- Footlong values use Subway UK's published 2 x 6-inch serving rule.\n- No dosing or clinical logic changed.\n'''
if '## v2.8.6 - Subway UK restaurant foods' not in bs:
    b.write_text(bs.rstrip()+entryb+'\n')
