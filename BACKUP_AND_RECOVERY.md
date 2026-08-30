# BACKUP_AND_RECOVERY

## Backup model
- GitHub is the live source of truth for code and documentation.
- Supabase is the live source of truth for cloud meal/food data.
- Google Drive is the independent disaster-recovery mirror.

## Google Drive structure
Recommended root folder: `CGM App Backup`

Inside it keep:
- `Current Production Mirror` - current source and documentation files.
- `Release Archives` - dated/versioned ZIP snapshots.
- `Recovery and Instructions` - PROJECT_BRAIN, PROJECT_RULES, this guide, repository/branch manifest and restore notes.
- `CGM Review Archives` - optional copies of the 3-file review inputs/outputs where appropriate.

## Files that must be mirrored
At minimum mirror every file present on GitHub `main`, including:
- production and beta HTML/JavaScript
- SQL/schema/migration files
- README and CHANGELOG
- CGM analysis protocol
- Smart Food/Smart Meal documentation
- release/backup notes
- PROJECT_BRAIN.md
- PROJECT_RULES.md
- BACKUP_AND_RECOVERY.md

## Release backup procedure
After each production release:
1. Confirm the new release is committed to GitHub `main`.
2. Confirm a rollback branch exists for the prior known-good state when the release is meaningful.
3. Refresh the Google Drive `Current Production Mirror` from GitHub `main`.
4. Create a dated/versioned ZIP snapshot in `Release Archives`.
5. Update the repository manifest with production version, main commit SHA and rollback-branch names.
6. Confirm Drive backup completion explicitly. Do not assume it succeeded.

## Recovery if the live app is lost
1. Read `PROJECT_BRAIN.md` and `PROJECT_RULES.md` first.
2. Restore the current source from GitHub `main` or the latest Drive release archive.
3. Recreate GitHub Pages using `index.html` as the production entry point.
4. Recreate/verify Supabase schema using the SQL files and documented configuration.
5. Test authentication, meal save/sync, Smart Food, CSV export, delete, and CGM Progress display before considering the restore complete.

## Recovery if GitHub is lost
Use the latest Drive `Release Archives` ZIP plus `Recovery and Instructions` to create a new repository. The current production snapshot is sufficient to recreate the app. The branch manifest documents rollback refs that existed at backup time, although full GitHub commit history remains best preserved by GitHub itself unless a full Git bundle/mirror is also stored.

## Recovery if Google Drive is lost
GitHub remains the authoritative code/documentation source. Recreate the Drive backup from the repository using this procedure.

## Database note
Source-code backup does not itself back up Supabase production rows. Database export/backups should be treated as a separate recovery layer. Never put credentials, passwords, private keys or service-role secrets into the public GitHub repository or into plain-text recovery documentation.

## Backup verification
A backup is only considered complete when the files are visibly present in Drive and the dated archive can be identified by version/date.
