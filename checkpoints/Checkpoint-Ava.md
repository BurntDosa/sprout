## Commit `f15c0ae` — 2026-11-10

## Context (background on why this change exists — infer from the commit message and diff)

The commit starts Sprout, a small local plant-watering reminder service. The README describes it as a fictional project maintained by Cleo and Ben while Ava is away, with Darren joining, and says it uses no external services. The tracked plant data is explicitly sample data, not a production database. This change establishes the reminder calculation and a read-only HTTP entry point, rather than a complete plant-management system.

## Changes (grouped by file with specific function/class names)

- `sprout/reminders.py` separates reminder logic from HTTP handling. `load_settings()` reads `settings.json`, and `load_plants()` reads the `plants` array from `plants.json`. `due_plants(plants, today, settings)` returns plants whose `watered_at` date plus `reminder_days` is earlier than `today`; a plant is not returned on the exact threshold date.
- `sprout/server.py` adds the `Handler` class. Its `do_GET()` serves JSON for `/reminders` and returns 404 for other paths. The module entry point starts `HTTPServer` on `127.0.0.1` using the configured port.
- `settings.json` sets the reminder interval to 7 days and port to 8080. `plants.json` provides a sample Fern watered on 2026-10-01.
- `README.md` documents how to start the server and run `python -m unittest discover -s tests`. The diff adds no test files.
- `sprout/__init__.py` establishes the package. `.gitignore` excludes Python cache files, virtual environments, `.env`, and named local context directories/files.

## Impact (confirmed downstream effects from the diff; mark inferred impacts with 'Likely:')

Running `python -m sprout.server` starts a local HTTP server, and `GET /reminders` returns a JSON array of plants past the configured watering interval. Requests to other paths receive 404. The endpoint does not modify plant data. Likely: because the default JSON paths are relative, starting the service outside the project directory may prevent it from finding its data and settings files.

## Priority Rating

MEDIUM — This provides a working local reminder endpoint, but it is read-only and uses sample JSON data rather than a production persistence layer.
