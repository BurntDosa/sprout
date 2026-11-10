# While You Were Gone — Since November 10, 2026

Sprout started as a local, read-only plant-watering reminder service using sample JSON data, then added a health check and updated its API and plant-data format. The main things to handle before running or integrating it are migrating existing plant data to schema v2 and switching clients to `GET /api/reminders`. The project uses no external services.

## Critical Changes (Must-Read)

- **Migrate plant data before startup.** `load_plants()` now requires schema v2 and the `last_watered` field. For existing v1 data, stop the service and run `python -m sprout.migrate` once. The migration backs up the original file as `.json.bak` before replacing it; it leaves v2 files unchanged and rejects unsupported versions.
- **Update reminder clients.** The reminders route is now `GET /api/reminders`; the old `/reminders` path returns 404. Update any clients using the previous URL. **Update:** The service initially exposed `/reminders`; the API namespace change makes `/api/reminders` the accepted path.
- **Update the settings key as directed by the upgrade notes.** They retain instructions to rename `reminder_days` to `watering_interval_days`. The checkpoints don’t specify further details of that settings change.
- **Reminder-date boundary is covered by a new test.** A plant due on the supplied date is included; overdue plants stay included, while plants due later are excluded. **Update:** The initial reminder logic described the threshold as earlier than `today`; the test added later confirms that a plant due exactly on the supplied date is included.

## New Features & Additions

- `GET /health` returns HTTP 204 with no body. It responds before the reminders path, so the health check does not load plant storage. Other paths besides `/health` and `/api/reminders` still return 404.
- The service provides a read-only JSON reminders endpoint. Run it with `python -m sprout.server`; it listens on `127.0.0.1` using the configured port. The README documents this command and `python -m unittest discover -s tests`.
- A test now checks due-today, overdue, and future reminder cases using a seven-day interval.
- Upgrade instructions document the data migration and reminder-route change.
- The README describes Sprout as a fictional project, says it uses no external services, and identifies the tracked plant data as sample data rather than a production database. The initial sample is a Fern watered on 2026-10-01.
- **Update:** The initial reminders endpoint was `GET /reminders`; it was later replaced by `GET /api/reminders`. The server still starts with `python -m sprout.server`, and the README’s test command remains `python -m unittest discover -s tests`.
- **Likely:** The JSON paths are relative, so starting the service outside the project directory may prevent it from finding its settings and plant data files.

## Refactors & Structural Changes

- Reminder logic lives in `sprout/reminders.py`, separate from HTTP handling in `sprout/server.py`. The `Handler` class serves the API, while `load_settings()`, `load_plants()`, and `due_plants()` handle settings, plant data, and reminder selection.
- Plant storage now has an explicit schema version. The migration command converts v1 records from `watered_at` to `last_watered`; the checked-in sample data and reminder test records use the v2 format.
- `.gitignore` no longer excludes `checkpoints/`, `catchups/`, or `MASTER_CONTEXT.md`. Matching files can now appear in `git status` and be staged, unless another ignore rule applies.
- **Update:** The initial storage format had no schema marker and used `watered_at`; `load_plants()` now rejects files without schema version 2, and `due_plants()` reads `last_watered`.

## New Dependencies & Config Changes

- No new dependencies are stated in the checkpoints.
- The sample settings specify a seven-day watering interval and port `8080`. The upgrade notes require the settings-key rename from `reminder_days` to `watering_interval_days`.
- The checked-in `plants.json` sample now includes `schema_version: 2` and uses `last_watered`. The initial setup uses local JSON files and documents no external services.