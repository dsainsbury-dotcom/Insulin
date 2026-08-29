# Smart Food System v2.4

## Purpose

The Smart Food System reduces manual meal entry while preserving a clear record of where nutrition values came from.

## Features

- Barcode lookup using Open Food Facts.
- Camera barcode scanning with manual barcode fallback.
- Nutrition-label photo OCR using Tesseract.js in the browser.
- Manual nutrition entry when lookup/OCR is unavailable.
- Portion handling by weight or servings.
- Automatic carbohydrate and fat calculation for the amount actually eaten.
- One-tap transfer into the meal tracker.
- Personal food library stored locally and rebuilt from structured meal-source markers where possible.
- Usual portion tracking from prior uses.
- Nutrition source written into the meal notes so later CGM reviews can distinguish verified packaging/database values from estimates.
- Food report cards show usage/portion history only until CGM outcome matching is added during review processing.

## Safety and data quality

- Barcode results are shown for confirmation before use.
- OCR results are never silently trusted. The extracted text is shown and carbohydrate/fat per 100 g remain editable before transfer.
- If serving size is missing or ambiguous, use weight mode.
- Restaurant/unknown meals should continue to use manual estimates and are not treated as clean evidence for changing ICR.

## Nutrition source labels

Meal notes may include a structured marker beginning with `SFS:`. This records the food name, barcode where available, nutrition source, per-100 g values and portion used. It is used for future personal-food history and review context.
