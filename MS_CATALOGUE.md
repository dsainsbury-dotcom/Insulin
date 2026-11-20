## v2.11.0 · Official M&S nutrition source · 20 November 2026

Foods now includes official M&S catalogue search by product name or exact M&S product code. The selected catalogue covers ready-to-cook, bakery and food-on-the-move categories plus a reference product. This is a bounded snapshot. Every entry retains the official URL, pack size and check date. Confirmed cloud foods keep priority, followed by indexed M&S product codes and Open Food Facts.

Review the matching pack, per-100g values and eaten weight before use. Pack weight is not assumed to be a serving. Entries older than seven days cannot be selected. Missing or bounded nutrition values are excluded. Source URL and date are retained in nutrition provenance and meal notes using existing fields. Per-100ml foods are excluded from the grams-based editor.

The GitHub workflow refreshes official pages daily, preserves the previous catalogue on broad failure and requests a Pages rebuild. Schedules can be delayed or disabled by GitHub. Source/schema failures remain visible in Actions and freshness is visible in the app. Search more products opens the official catalogue.

Rollback branch backup/pre-v2.11.0-ms-catalogue. Clinical calculations and CGM matching are preserved. Recovery requires the full release ZIP including ms_catalogue.js, data/ms-foods.json, tools/refresh_ms_catalogue.py and its refresh workflow.

