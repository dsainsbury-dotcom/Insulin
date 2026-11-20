/* Official M&S snapshots are fetched by GitHub, never through a third-party proxy. */
let msCataloguePromise = null;

async function loadMsCatalogue() {
  if (!msCataloguePromise) {
    msCataloguePromise = fetch('data/ms-foods.json', {cache: 'no-store', signal: AbortSignal.timeout(12000)})
      .then(response => {
        if (!response.ok) throw new Error('M&S catalogue unavailable');
        return response.json();
      })
      .then(data => {
        if (!Array.isArray(data.products)) throw new Error('Invalid M&S catalogue');
        return data;
      })
      .catch(error => {
        msCataloguePromise = null;
        throw error;
      });
  }
  return msCataloguePromise;
}

function msCode(value) {
  return String(value || '').replace(/^0+(?=\d)/, '');
}

function msProductCurrent(product) {
  const age = Date.now() - Date.parse(product.checkedAt);
  return Number.isFinite(age) && age >= -86400000 && age <= 7 * 86400000;
}

function msProductMatches(product, term) {
  const words = term.toLowerCase().trim().split(/\s+/).filter(Boolean);
  const text = (product.name + ' ' + product.brand + ' ' + product.code + ' M&S Marks and Spencer').toLowerCase();
  return words.every(word => text.includes(word)) || msCode(product.code) === msCode(term);
}

function useMsProduct(product) {
  if (!msProductCurrent(product)) {
    setNotice('This M&S entry needs refreshing. Check the official product page or scan the packet label.', 'warn');
    return;
  }
  smartMode('manual');
  $('portionMode').value = 'weight';
  prepareNutrition({
    name: product.name + ' - M&S',
    brand: 'Marks & Spencer',
    barcode: product.code,
    source: 'Official M&S catalogue',
    sourceUrl: product.sourceUrl,
    checkedAt: product.checkedAt,
    carbs100: product.carbs100,
    fat100: product.fat100,
    protein100: product.protein100,
    kcal100: product.kcal100
  });
  const note = document.createElement('div');
  note.className = 'notice warn';
  note.id = 'msNutritionNote';
  note.textContent = 'Official M&S values per 100g, checked ' +
    product.checkedAt.slice(0, 10) + '. Pack ' + product.pack +
    '. Compare with your packet and enter the weight you will eat.';
  $('msNutritionNote')?.remove();
  $('nutritionEditor').prepend(note);
  $('smartPanel').scrollIntoView({behavior: 'smooth', block: 'start'});
}

async function lookupMsBarcode(code) {
  // M&S publishes 8-digit product codes. No guessed prefix or suffix matching.
  if (!/^0*\d{8}$/.test(code)) return null;
  const data = await loadMsCatalogue();
  return data.products.find(product =>
    msCode(product.code) === msCode(code) && msProductCurrent(product)) || null;
}

async function renderMsResults() {
  const term = $('msSearch').value.trim();
  $('msOfficialSearch').href = 'https://www.marksandspencer.com/food/search?searchTerm=' +
    encodeURIComponent(term);
  try {
    const data = await loadMsCatalogue();
    // A later keystroke owns the results if loading finished out of order.
    if ($('msSearch').value.trim() !== term) return;
    $('msCatalogueState').textContent = data.products.length +
      ' official products indexed · ' + data.coverage +
      ' · refreshed ' + data.generatedAt.slice(0, 10) +
      '. Entries older than seven days require an official-page or packet check.';
    const matches = data.products.filter(product => msProductMatches(product, term));
    $('msResults').replaceChildren();
    for (const product of matches.slice(0, 40)) {
      const card = document.createElement('div');
      card.className = 'restaurantItem';
      const title = document.createElement('strong');
      title.textContent = product.name + ' · ' + product.pack;
      const details = document.createElement('p');
      details.textContent = 'Per 100g · carbs ' + product.carbs100 + 'g · fat ' +
        product.fat100 + 'g · protein ' + product.protein100 + 'g · ' +
        product.kcal100 + ' kcal · code ' + product.code;
      const link = document.createElement('a');
      link.href = product.sourceUrl;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.textContent = 'Check official M&S page';
      const checked = document.createElement('p');
      checked.className = 'sectionNote';
      checked.textContent = 'Checked ' + product.checkedAt.slice(0, 10);
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'primary';
      button.textContent = msProductCurrent(product) ? 'Check values and choose portion' : 'Entry needs refreshing';
      button.disabled = !msProductCurrent(product);
      button.onclick = () => useMsProduct(product);
      card.append(title, details, link, checked, button);
      $('msResults').append(card);
    }
    if (!matches.length) $('msResults').textContent =
      'No indexed match. Search the official catalogue below, then use the packet or website values in Manual nutrition.';
    else if (matches.length > 40) {
      const hint = document.createElement('p');
      hint.textContent = 'Showing 40 of ' + matches.length + ' matches. Add more words to narrow your search.';
      $('msResults').append(hint);
    }
  } catch (error) {
    $('msCatalogueState').textContent = 'M&S index could not load. Use the official catalogue link or your packet label.';
    $('msResults').replaceChildren();
  }
}

$('msMode').onclick = () => {
  $('msPanel').classList.remove('hidden');
  renderMsResults();
  $('msPanel').scrollIntoView({behavior: 'smooth', block: 'start'});
};
$('closeMs').onclick = () => $('msPanel').classList.add('hidden');
$('msSearch').addEventListener('input', renderMsResults);

function smartNutritionSource() {
  const selected = $('smartSource').value;
  if (selected === 'Official M&S catalogue' && currentSmart?.sourceUrl) {
    return 'Official M&S catalogue · ' + currentSmart.sourceUrl +
      ' · checked ' + currentSmart.checkedAt.slice(0, 10);
  }
  if (selected === 'Personal cloud library' &&
      currentSmart?.nutritionOrigin?.startsWith('Official M&S catalogue')) {
    return currentSmart.nutritionOrigin;
  }
  return selected;
}
