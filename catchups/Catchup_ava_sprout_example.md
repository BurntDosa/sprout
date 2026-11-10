# While You Were Gone — Since October 02, 2026

Since October 2, Sprout’s reminder API and configuration changed, and existing plant data now needs a one-time migration before reminders can load it. You also have a lightweight health endpoint, stronger reminder and migration tests, and updated docs that frame the repository as a Checkpoint demo. The latest changes mostly update documentation and allow generated Checkpoint files to be tracked in Git; they do not change application behavior.

## Critical Changes (Must-Read)

- **Migrate plant data before starting reminders.** Plant storage is now schema v2: the top-level data must have `schema_version: 2`, and each plant’s watering date uses `last_watered` instead of `watered_at`. `load_plants()` rejects data that hasn’t been migrated. Stop the service and run `python -m sprout.migrate` once. The migration backs up the original as `.json.bak` and uses a temporary file before replacing it. It accepts v1 or unversioned data, returns `False` for data already at v2, and raises `ValueError` for other schema versions. It will not overwrite an existing backup.

- **Update reminder clients to `GET /api/reminders`.** The old `/reminders` path now returns 404, with no compatibility route shown. Only `/api/reminders` reaches reminder handling; other paths return 404.

- **Update settings and install the new dependency.** Settings moved from `settings.json` to `settings.yaml`, parsed with `yaml.safe_load`. Install dependencies with `python -m pip install -r requirements.txt`; `requirements.txt` pins `PyYAML==6.0.3`. The settings key is now `watering_interval_days`, not `reminder_days`. The documented values remain 7 days and port 8080. Old key names can cause a `KeyError` when reminders read the interval.

- **Due plants are now included on their due date.** The comparison changed from strictly before today to on or before today. Keep this boundary behavior in mind when checking reminder results.

## New Features & Additions

- `GET /health` returns HTTP 204 with no response body. It exits before reminder handling and does not call `due_plants`, `load_plants`, or `load_settings`, so the check does not require plant storage to be readable. Paths other than `/health` and `/api/reminders` still return 404.
- `sprout.migrate` adds a command-line migration path for plant data. Regression tests check that migration preserves the original bytes in the backup, changes `watered_at` to `last_watered`, safely handles a repeat run, and refuses to overwrite an existing backup.
- Reminder tests now cover due-today, overdue, and future plants. With a seven-day interval, the test expects only Fern on October 8, 2026, and Fern and Ivy on October 9.

## Refactors & Structural Changes

- The plant data format is now explicit rather than implicitly v1: storage has a `schema_version`, and the watering-date field is `last_watered`. The sample `plants.json` was updated to match.
- The README was rewritten to present Sprout as a public Checkpoint demo. It points readers to generated material in `checkpoints/`, `catchups/`, and `MASTER_CONTEXT.md`, while retaining shorter installation, test, server, and upgrade instructions. It says the October 2026 commits are fictional and the generated documents come from live Checkpoint runs. The README’s Checkpoint reference now links to a specific commit, `f3d94ae`, rather than the `checkpoint-agent 1.2.6` package page; the changes shown do not modify or verify a GitHub Actions workflow.
- `.gitignore` no longer excludes `checkpoints/`, `catchups/`, or `MASTER_CONTEXT.md`. Git can now notice files at those paths, but removing ignore rules does not automatically add existing files to version control. Python cache files, `.venv/`, and `.env` remain ignored.
- Upgrade notes and README guidance document the settings rename, API route change, PyYAML installation, plant-data migration, and health endpoint behavior.

## New Dependencies & Config Changes

- Add `PyYAML==6.0.3` by installing `requirements.txt`. `load_settings()` now defaults to `settings.yaml` and parses YAML. Custom paths passed to the function must also contain YAML-formatted settings.
- Replace `settings.json` with `settings.yaml`. The configured interval remains seven days and the port remains 8080, but the interval key is `watering_interval_days`.
- Migrate existing `plants.json` data to schema v2 before reminder loading. The v2 format requires `schema_version: 2` and `last_watered`; the migration command preserves the original in a `.json.bak` file.