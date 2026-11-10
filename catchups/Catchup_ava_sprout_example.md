# While You Were Gone — Since October 02, 2026

Sprout’s compatibility changes now include a new reminders route, YAML settings, and a required one-time migration of existing plant data to schema v2. You also have a health endpoint, reminders that include plants due today, migration test coverage, and updated upgrade instructions. The README now presents Sprout as a public Checkpoint demo and points to its generated artifacts. Before starting an existing installation, handle the settings and data migrations and update clients to the new route.

## Critical Changes (Must-Read)

- **Migrate existing plant data before startup.** `load_plants` now rejects files without `schema_version: 2`. Run `python -m sprout.migrate` once on existing v1 data. The migration renames each plant’s `watered_at` field to `last_watered`, adds the schema marker, saves the original bytes to a `.json.bak` file, and replaces the data through a temporary file. It skips v2 files; unsupported schema versions raise `ValueError`. The upgrade guide says to stop the service before migrating.
- **Update reminders clients.** The accepted route is now `GET /api/reminders`; `GET /reminders` returns 404. Other paths also return 404, except for the new `/health` endpoint.
- **Update settings before running the service.** Rename `reminder_days` to `watering_interval_days`. Settings are now read from `settings.yaml`, not `settings.json`, and parsing requires PyYAML. Install the project requirements and ensure the YAML file is present.
- **Check existing Git ignore behavior.** The repository no longer ignores files solely because they are under `checkpoints/` or `catchups/`, or because they are named `MASTER_CONTEXT.md`. Matching local files may now show up in `git status` and can be staged unless another ignore rule excludes them.

## New Features & Additions

- `GET /health` returns HTTP 204 with no response body. The server handles it before the reminders route and does not load plant storage, so it can check server responsiveness without depending on plant data.
- Reminder selection now includes plants due today as well as overdue plants. The due-date comparison changed from strict “before today” to “today or earlier.” New test coverage checks the due-today, overdue, and future-date cases. The test uses a seven-day interval and checks plants last watered on October 1, 2, and 3, 2026: for October 8 it expects only Fern, and for October 9 it expects Fern and Ivy.
- `python -m sprout.migrate` provides the one-time v1-to-v2 data migration. Added tests cover a successful migration, preservation of the original file in the backup, safe repeated migration, and refusing to overwrite an existing backup. The tests check that the first migration returns `True`, a repeated migration returns `False`, and an existing backup causes `FileExistsError` without changing the source. The checkpoints describe added tests, not whether they have been run.

## Refactors & Structural Changes

- Plant storage now has an explicit schema version. The checked-in sample data and reminder tests use `schema_version: 2` and `last_watered`; `due_plants` reads `last_watered` when calculating reminder dates. **Update:** v1 data used `watered_at` and must be migrated before `load_plants` accepts it.
- Settings moved from `settings.json` to `settings.yaml`. The YAML file retains the existing values: a seven-day watering interval and port 8080. **Update:** `load_settings()` now defaults to `settings.yaml` and parses it with `yaml.safe_load`.
- The README now presents Sprout as a plant-reminder API and a public demo of Checkpoint, and points to generated Checkpoint artifacts and the upgrade guide. It links to Checkpoint and `checkpoint-agent 1.2.6`, and identifies the October 2026 project history as fictional. The README no longer includes some endpoint, settings, and data details, so use `docs/upgrade.md` for upgrade steps. The documentation change does not verify that the described artifacts or a GitHub Actions workflow exist.
- The new Git ignore behavior allows Checkpoint-related documents to be tracked. The commit changes ignore rules only; it does not alter application or CI behavior.

## New Dependencies & Config Changes

- `requirements.txt` now pins `PyYAML==6.0.3`. Install dependencies with `python -m pip install -r requirements.txt`; `load_settings()` defaults to `settings.yaml` and parses it with `yaml.safe_load`.
- Replace `settings.json` with `settings.yaml` and use `watering_interval_days` instead of `reminder_days`. The configured interval remains seven days, and the port remains 8080.
- The README’s upgrade sequence is to rename the setting, switch clients to `GET /api/reminders`, install PyYAML, then migrate plant data. It also clarifies that tracked `plants.json` is sample data, not a production database.