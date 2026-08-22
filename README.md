# ICR Meal Dashboard

A single-file, static web app designed for GitHub Pages.

## What it does

- Logs carbohydrate amount, meal type and current glucose
- Uses a baseline ICR of **1:15** by default
- Uses a target glucose of **8.0 mmol/L** by default
- Lets you enter a different ICR for an individual entry
- Optional correction calculation **only when you enter your own clinician-agreed ISF**
- Saves meal entries in the browser using `localStorage`
- Exports saved meal data to CSV
- Tracks meal type so later Dexcom analysis can compare categories

The app deliberately **does not automatically change ICR by meal type**. The meal categories are stored for later analysis.

## Publish with GitHub Pages

1. Create a new GitHub repository, e.g. `icr-meal-dashboard`
2. Upload `index.html`
3. Commit the file
4. Open **Settings → Pages**
5. Under **Build and deployment**, choose **Deploy from a branch**
6. Select the `main` branch and `/ (root)`
7. Save

GitHub will provide a Pages URL shortly afterwards.

## Data privacy

All meal data is stored in the browser on the device being used. Nothing is sent to a server by this app.

Export the CSV regularly if you want a backup or want to analyse the records elsewhere.

## Medical safety

This project is a personal calculation and logging aid, not a medical device. It does not determine insulin settings. Only use ICR, target and ISF values agreed with your diabetes team. Avoid insulin stacking and follow your own sick-day/ketone guidance.
