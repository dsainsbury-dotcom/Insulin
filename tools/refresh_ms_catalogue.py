"""Refresh a bounded, public nutrition index from official UK M&S Foodhall pages."""
import concurrent.futures
import datetime
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data/ms-foods.json"
ORIGIN = "https://www.marksandspencer.com"
CATEGORIES = ["ready-to-cook", "bakery-and-cakes", "food-on-the-move"]
EXTRA_URLS = ["/food/products/p/fdp60499837"]


def page_model(path):
    url = urllib.parse.urljoin(ORIGIN, path)
    if urllib.parse.urlparse(url).netloc != "www.marksandspencer.com":
        raise ValueError("Only official M&S pages are accepted")
    request = urllib.request.Request(url, headers={"User-Agent": "CGM-Food-Catalogue/1.0"})
    with urllib.request.urlopen(request, timeout=35) as response:
        html = response.read().decode("utf-8")
    match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if not match:
        raise ValueError("M&S page data unavailable")
    return json.loads(match[1])["props"]["pageProps"]["viewModel"]


def numeric(value):
    # Bounds such as <0.1 must never become an invented exact quantity.
    text = str(value).strip()
    return float(text) if re.fullmatch(r"\d+(?:\.\d+)?", text) else None


def product(path):
    model = page_model(path)
    nutrition = model.get("nutrition") or {}
    categories = nutrition.get("categories", [])
    column = next((i for i, label in enumerate(categories)
                   if re.fullmatch(r"per\s*100\s*g", label, re.I)), None)
    if column is None:
        raise ValueError("No per-100g nutrition column")
    rows = {row[0].strip().lower(): row[column] for row in nutrition.get("values", [])
            if len(row) > column}
    def nutrient(key):
        return numeric(re.sub(r"\s*g$", "", str(rows.get(key, ""))).strip())
    carbs = nutrient("carbohydrate")
    fat = nutrient("fat")
    if any(value is None for value in (carbs, fat, nutrient("protein"), numeric(rows.get("energy kcal", "")))):
        raise ValueError("Exact carbohydrate, fat, protein and energy values required")
    code = str(model.get("upc", ""))
    if not re.fullmatch(r"\d{8,14}", code):
        raise ValueError("Missing official product code")
    weight = str(model.get("weight", ""))
    return {
        "id": str(model["productId"]), "code": code,
        "name": model["productName"], "brand": model.get("brand", ""),
        "pack": weight, "carbs100": carbs, "fat100": fat,
        "protein100": nutrient("protein"), "kcal100": numeric(rows.get("energy kcal", "")),
        "sourceUrl": ORIGIN + "/food/products/p/fdp" + str(model["productId"]),
        "checkedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }


def main():
    previous = json.loads(OUTPUT.read_text()) if OUTPUT.exists() else {"products": []}
    paths = {p["sourceUrl"] for p in previous["products"]}
    paths.update(EXTRA_URLS)
    for category in CATEGORIES:
        model = page_model("/food/l/" + category)
        # Category pages expose the same productLists shape as catalogue search.
        for section in model.values():
            if isinstance(section, dict) and "productLists" in section:
                for products in section["productLists"].values():
                    paths.update(p["seoUrl"] for p in products)
    if not paths:
        raise RuntimeError("No catalogue products discovered")
    records = {p["id"]: p for p in previous["products"]}
    successful = 0
    def fetch(path):
        try:
            return product(path)
        except Exception as error:
            print("Skipped", path, str(error), flush=True)
            return None
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for record in pool.map(fetch, sorted(paths)):
            if record:
                records[record["id"]] = record
                successful += 1
    if successful < max(1, int(len(paths) * 0.5)):
        raise RuntimeError("Too few products refreshed; previous catalogue preserved")
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    payload = {"source": "Official M&S UK Food Catalogue", "generatedAt": now,
               "coverage": "Selected ready-to-cook, bakery and food-on-the-move products",
               "products": sorted(records.values(), key=lambda p: p["name"].lower())}
    OUTPUT.parent.mkdir(exist_ok=True)
    temporary = OUTPUT.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(OUTPUT)
    print("Refreshed", successful, "products;", len(records), "indexed")


if __name__ == "__main__":
    main()
