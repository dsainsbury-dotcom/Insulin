# Smart Meal Assistant v2.4.3

The Smart Food portion calculator now shows the meal-dose calculation before the meal is transferred into the main tracker.

## Behaviour
- Uses the current meal ICR from the tracker, defaulting to 1:15.
- Shows exact calculated meal dose from carbohydrate / ICR.
- Shows the whole-unit rounded-up amount that will pre-fill `Insulin actually taken` when `Use in meal` is pressed.
- Does not calculate or add a correction dose.
- High-fat portions show a delayed-rise context reminder only. The app does not automatically add insulin because of fat.
- Barcode, nutrition-label OCR and manual Smart Food entries all use the same Smart Meal Assistant calculation.
- The user can still overwrite the actual-insulin field to record what was genuinely taken.

## Safety
This is a meal-dose calculator using the user's current agreed ICR, not an automated insulin dosing system or medical device. Nutrition estimates and OCR/barcode values must be checked before use, and treatment settings should remain aligned with the diabetes-team plan.
