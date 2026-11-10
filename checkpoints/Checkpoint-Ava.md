## Commit `f15c0ae` — 2026-10-02

## Context
This change starts Sprout as a small, local plant-watering reminder service. The README describes it as a fictional example maintained by Cleo and Ben while Ava is away, with Darren joining, and says it uses no external services. The service reads a tracked sample plant record and settings from JSON files; the README explicitly says `plants.json` is not a production database.

## Changes
- `sprout/reminders.py` separates reminder logic from HTTP handling. `load_settings()` and `load_plants()` read JSON from configurable paths, defaulting to `settings.json` and `plants.json`. `due_plants()` selects plants whose watering date plus the configured `reminder_days` interval is earlier than the supplied date.
- `sprout/server.py` adds the read-only HTTP API. `Handler.do_GET()` returns the due plants as JSON for `/reminders` and sends 404 for other paths. The module entry point starts an `HTTPServer` bound to `127.0.0.1` on the configured port.
- `settings.json` sets a seven-day reminder interval and port 8080. `plants.json` supplies a sample Fern record last watered on 2026-10-01.
- `README.md` documents the server and test commands. `.gitignore` excludes Python cache files, virtual environments, environment files, checkpoint and catch-up directories, and `MASTER_CONTEXT.md`. `sprout/__init__.py` establishes the package.

## Impact
- Confirmed: Running `python -m sprout.server` starts the HTTP service on localhost:8080 with the checked-in settings. `GET /reminders` returns a JSON array of plants due under the configured date rule; other paths receive 404.
- Confirmed: The endpoint only reads plant and settings data; this change adds no write path or external-service integration.
- Likely: A caller can use the endpoint to display reminders, but the service does not itself send notifications or update watering dates.
- The README gives a unittest discovery command, but this diff adds no test files.

## Priority Rating
MEDIUM — This establishes a usable local reminder endpoint, but it is read-only and relies on sample JSON data rather than production storage or notification delivery.
