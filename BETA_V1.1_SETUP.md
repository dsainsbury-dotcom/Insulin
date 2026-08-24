# ICR Meal Dashboard v1.1 Beta Setup

This beta adds authenticated cross-device cloud sync while keeping the v1.0 local-storage workflow as a fallback.

## Safety / rollback

- Live/current v1.0 remains on `main`.
- Frozen rollback branch: `backup/v1.0-local`.
- Beta development branch: `v1.1-cloud-sync`.
- The beta saves every new meal to local browser storage first. Cloud sync is an additional copy, not the only copy.

## One-time Supabase setup

1. Create a Supabase project.
2. In the Supabase SQL editor, run `supabase_schema.sql` from this branch.
3. In Authentication settings, enable Email / Magic Link sign-in.
4. Add the beta app URL to the allowed redirect URLs once the beta is hosted.
5. Copy the Project URL and the public anon key from Supabase project settings.
6. Open the beta app, enter the Project URL, public anon key and the same email address on each device.
7. Tap `Email sign-in link` and complete sign-in on each device.
8. Tap `Upload local meals to cloud` once on each device that already contains local v1.0 data. Duplicate rows are prevented by a per-entry client ID.

## Normal use

- Add meals as normal.
- The app writes locally first.
- If cloud sign-in is active, the meal is then upserted to the shared cloud table.
- `Sync now` / `Refresh` pulls the unified cloud history.
- `Export CGM Review CSV` exports the merged view for use alongside the Dexcom PDF and Dexcom CSV.

## Data access model

Row Level Security is enabled. Each authenticated account can read/write only rows whose `user_id` matches the signed-in Supabase user. Never put a Supabase service-role key into the browser app. Only use the public anon key.

## Beta test checklist

- Confirm a meal added on Device A appears on Device B after refresh.
- Confirm existing local history can be uploaded without duplicates.
- Confirm offline/no-cloud saving still creates a local row.
- Confirm a failed cloud write does not lose the local row.
- Confirm CGM Review CSV contains one copy of each meal.
- Confirm TEST ONLY rows remain identifiable in Notes and can be excluded during analysis.

Do not merge this beta into `main` until cross-device behaviour has been tested for several days and the rollback branch has been verified.
