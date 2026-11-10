# While You Were Gone — Since November 10, 2026

The recorded changes establish Sprout as a local, read-only plant-reminder service and then evolve its API, configuration, and plant-data format. The main things you need to account for are the `/api/reminders` route, YAML settings, and a required one-time migration for existing plant data.

## Critical Changes (Must-Read)

- **Update reminder clients:** The reminders endpoint is now `GET /api/reminders`. The old `GET /reminders` path returns 404; other paths also return 404, except `/health`.
- **Migrate existing plant data before startup:** Plant files must use schema version 2 and the `last_watered` field. `load_plants()` rejects files without schema version 2. For v1 data, stop the service and run `python -m sprout.migrate` once. The migration saves the original bytes to a `.json.bak` file before replacing the data file. It skips files already at v2 and raises an error for other unsupported versions.
- **Update settings and install the dependency:** Settings moved from `settings.json` to `settings.yaml`, and the interval key changed from `reminder_days` to `watering_interval_days`. Install dependencies with `python -m pip install -r requirements.txt`; settings loading now uses PyYAML.
- **Check reminder-date behavior:** Plants due exactly today are now included, as are overdue plants. The interval remains seven days in the checked-in sample settings.

## New Features & Additions

- `GET /health` returns HTTP 204 with no body. It returns before the reminder-handling path, so it does not load plant storage.
- The migration command in `sprout.migrate` upgrades v1 plant data. It renames `watered_at` to `last_watered`, sets `schema_version` to 2, writes a temporary file, and replaces the original after creating the backup. Running it again on v2 data returns `False`.
- Reminder tests now cover due-today, overdue, and future plants. Migration tests check backup contents, the field conversion, repeat-run behavior, and that an existing backup is not overwritten. These diffs add tests; they don’t establish that the tests were run.
- The repository’s ignore rules no longer exclude `checkpoints/`, `catchups/`, or `MASTER_CONTEXT.md` by those patterns, so Git can track matching files.

## Refactors & Structural Changes

- The service now has a package structure with reminder logic in `sprout/reminders.py` and HTTP handling in `sprout/server.py`. The server serves JSON for the reminders route and returns 404 for unrecognized paths.
- Plant storage now has an explicit schema version. Reminder calculations read `last_watered` from schema v2 records instead of the old `watered_at` field.
- `due_plants()` reads the interval from `watering_interval_days` and includes plants whose next watering date is today or earlier.
- The checked-in `plants.json` is sample data, not a production database. The service is read-only: the reminders endpoint returns due plants but does not modify plant data.
- The README’s framing changed to describe Sprout as a plant-reminder API and a Checkpoint demo. It points readers to Checkpoint output locations and the upgrade guide, but the documentation change does not verify that those artifacts or a GitHub Actions workflow exist. The README’s endpoint example and some configuration details were removed in one update, so use the upgrade guide for the documented upgrade steps.

## New Dependencies & Config Changes

- `requirements.txt` pins `PyYAML==6.0.3`. `load_settings()` now reads `settings.yaml` by default and parses it with `yaml.safe_load`.
- `settings.yaml` contains `watering_interval_days: 7` and `port: 8080`. The prior `settings.json` was removed. Existing settings files or scripts using `settings.json` or `reminder_days` need updating.
- Plant data now requires `schema_version: 2` and the `last_watered` date field. The tracked sample plant data was updated to that format.
- The server runs with `python -m sprout.server` on `127.0.0.1` using the configured port. The README documents running tests with `python -m unittest discover -s tests`.