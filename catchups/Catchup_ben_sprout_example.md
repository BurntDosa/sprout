# While You Were Gone — Since November 10, 2026

Sprout now has a local, read-only reminder service, with reminder logic separated from its HTTP handler. The main things to check before you run or upgrade it are the settings-file migration and a mismatch between the documented API path and the route shown in the application changes.

## Critical Changes (Must-Read)

- **Settings format and key changed.** `load_settings()` now reads `settings.yaml` by default using PyYAML. The interval key is `watering_interval_days` (still 7 days), replacing `reminder_days`. Update existing configuration and install the pinned dependency with `python -m pip install -r requirements.txt`.
- **Check the reminder URL before changing clients.** The initial server change shows `GET /reminders`, while the upgrade instructions tell clients to switch to `GET /api/reminders`. The checkpoints show no server-route change to implement that new path. Confirm the route in the current server code before updating clients.
- **Reminder selection now includes plants due today.** `due_plants()` uses an inclusive date comparison, so a plant is returned when its watering interval ends today as well as when it is overdue.
- **Plant-data migration is part of the documented upgrade path.** The upgrade notes instruct you to migrate plant data. Added tests specify a backup-preserving migration from `watered_at` to `last_watered`, but the test commit itself does not change the migration implementation or confirm the tests have run.
- **The service is still described as local and read-only.** The initial implementation serves reminder data and returns 404 for other paths; it does not modify plant data. The tracked `plants.json` is sample data, not a production database.

## New Features & Additions

- `sprout/server.py` adds a `Handler` for JSON reminder responses and starts an HTTP server on `127.0.0.1` using the configured port. The initial route is `GET /reminders`; other paths return 404. The initial settings specify port `8080`.
- `sprout/reminders.py` provides `load_settings()`, `load_plants()`, and `due_plants()`. Plant data comes from the `plants` array in `plants.json`. The reminder calculation compares each plant’s watering date plus the configured interval with the current date.
- `tests/test_migration.py` adds isolated tests using temporary files. They check that migration backs up the original bytes, changes `watered_at` to `last_watered`, returns `False` on a repeat migration, and raises `FileExistsError` rather than overwriting an existing backup.
- The README frames Sprout as a Checkpoint demo and describes `checkpoints/`, `catchups/`, and `MASTER_CONTEXT.md` as output locations. It identifies the project history as fictional; the documentation does not verify that those artifacts or a GitHub Actions workflow exist.

## Refactors & Structural Changes

- Reminder calculation is separated from HTTP handling: `sprout/reminders.py` owns settings, plant loading, and due-date logic; `sprout/server.py` owns the request handler and server startup.
- Due-date selection changed from strict to inclusive. A plant whose next watering date equals today is now included.
- The upgrade documentation lays out a sequence: rename the interval key, switch clients to `GET /api/reminders`, install PyYAML, and migrate plant data. Treat the endpoint step with care: the provided application changes show `/reminders`, not an implemented `/api/reminders` route.
- The migration tests add coverage, not migration behavior. The checkpoints do not confirm that the tests have been run.

## New Dependencies & Config Changes

- `requirements.txt` pins `PyYAML==6.0.3`. Install the requirements before loading YAML settings.
- Settings move from `settings.json` to `settings.yaml`. `load_settings()` defaults to `Path('settings.yaml')` and parses it with `yaml.safe_load`. The YAML config retains the 7-day interval and port `8080`, with the interval key named `watering_interval_days`.
- The initial setup uses relative paths for settings and plant data. Likely: starting the service outside the project directory may prevent it from finding those files.