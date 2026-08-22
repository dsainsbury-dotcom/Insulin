# ICR Meal Dashboard v2

Static GitHub Pages app.

## Changes in v2
- Removed the ISF/correction-factor field from the normal workflow.
- No correction dose is calculated.
- Default ICR remains 1:15.
- Default target glucose remains 8.0 mmol/L.
- Added optional 'insulin actually taken' field.
- Meal type, carbs, glucose, calculated dose, actual insulin and notes are saved locally.
- CSV export remains available.

## Updating GitHub Pages
Replace the existing `index.html` in the repository with this new file, renamed to `index.html`.
You do not need to delete the whole repository or any GitHub Pages settings.

The browser log is stored locally in localStorage, so replacing the website file should not normally delete your existing saved meal log on the same browser/device and same GitHub Pages URL.

## Safety
This is a personal logging/calculation aid, not a medical device. It does not calculate correction doses or determine insulin settings.
