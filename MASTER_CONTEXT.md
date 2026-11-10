# Master Context

Sprout is a small plant-reminder API. It reads plant records and settings from local files, calculates which plants have passed their watering interval, and exposes the result through a local HTTP server. It is deliberately a reminder service, not a full plant-management system: the reminders endpoint is read-only, and the tracked `plants.json` file contains sample data rather than a production database. Sprout’s repository also serves as a public demo of Checkpoint: the README describes generated commit and PR summaries, returning-author briefings, and onboarding material, and identifies the October 2026 project history as fictional. For an engineer joining the application work, the core path is straightforward: understand the file-based inputs, the reminder calculation, the HTTP handler, and the migration required for older plant data.

## Architecture Overview

Sprout has a small, file-backed architecture. The `sprout` package contains the application code: `reminders.py` handles reminder-related logic, `server.py` exposes HTTP routes, and `migrate.py` upgrades plant data. `plants.json` is the tracked sample data file. `settings.yaml` is the configuration file present in the repository, and `requirements.txt` pins PyYAML. The tests live in `tests/`, with separate coverage for reminders and migration.

The main data flow is:

1. The server receives a request.
2. `Handler.do_GET()` checks the requested path.
3. For `GET /api/reminders`, the reminder path loads settings and plant records, then calls `due_plants(...)` to determine which plants are due.
4. The handler returns the resulting data as JSON.
5. For `GET /health`, the handler responds with HTTP 204 and no body. This route returns before the reminder path, so it does not load plant storage.
6. Requests for other paths receive 404.

The reminder calculation has an explicit threshold rule. `due_plants(plants, today, settings)` compares each plant’s `last_watered` date plus the configured reminder interval with `today`. A plant becomes due only when that threshold is earlier than today; it is not due on the exact threshold date. The schema change from v1 to v2 renamed the watering-date field from `watered_at` to `last_watered`. `load_plants` rejects files that are not marked as schema version 2, so the migration step is part of operating an installation with older data.

`migrate.py` provides that upgrade path. Its `migrate` function treats a file without a schema version as v1, converts v1 plant records to the v2 field name, and sets `schema_version` to 2. It returns `False` for data already at v2 and raises `ValueError` for other unsupported versions. For a v1 file, it writes the original bytes to a `.json.bak` backup before replacing the source via a temporary `.json.tmp` file. An existing backup prevents the migration from overwriting it.

The current README says to run the service with `python -m sprout.server`, then request `GET /api/reminders` on localhost:8080. The checkpoints record an earlier route name, `/reminders`, and an earlier settings filename, `settings.json`; use the current README and repository contents rather than those historical details. The current file listing contains `settings.yaml`, and the dependency manifest includes PyYAML.

No Mermaid diagrams were supplied in the provided materials. The dependency graph and class hierarchy are marked as disabled, so the architecture is described here in prose rather than represented with diagrams.

## Key Decision Log

1. **Keep reminder calculation separate from HTTP handling.** `sprout/reminders.py` owns loading and due-date logic, while `sprout/server.py` owns request handling through `Handler`. The checkpoint describes this as separating reminder logic from HTTP handling. The resulting responsibilities are clear: the calculation can be exercised independently, and the server presents it over HTTP. **Rationale:** the checkpoint says this change establishes reminder calculation and a read-only HTTP entry point, rather than a complete plant-management system.

2. **Use a read-only local API over sample JSON files.** The server exposes reminders without modifying plant records, and the README explicitly describes `plants.json` as sample data rather than a production database. The HTTP server listens on `127.0.0.1` in the original implementation; the current README directs readers to localhost:8080. **Rationale:** the initial project description calls Sprout a small local reminder service and says it uses no external services. No rationale for a production persistence layer is documented.

3. **Make the storage schema explicit and require migration.** Plant data now carries `schema_version: 2`, and the watering-date key is `last_watered`. `load_plants` rejects older or unmarked files instead of silently treating them as v2. `migrate` preserves the original bytes in a backup before replacing the file. **Rationale:** the checkpoint says the schema marker and renamed field make the format explicit, and the upgrade notes require existing v1 data to be migrated before the service starts.

4. **Add a health route that bypasses data loading.** `Handler.do_GET()` handles `/health` before the reminders route and returns 204 without a response body. It does not enter the reminder path or open plant storage. **Rationale:** the checkpoint documents the endpoint as a way to report that the server is responding without entering the path that loads plant data.

## Gotchas & Tech Debt

- **Older plant files need migration.** `load_plants` requires schema version 2. A v1 file with `watered_at`, or an unmarked file, must be migrated before the reminders path can load it. The documented procedure is in `docs/upgrade.md`.
- **Migration protects existing backups.** If the `.json.bak` path already exists, `migrate` raises `FileExistsError` rather than overwriting that backup. The migration tests explicitly verify that the source remains unchanged in this case. Check for an existing backup before attempting a migration.
- **The due-date boundary is strict.** A plant is not returned on the exact date when its watering interval expires; it is returned only after that date. `ReminderTests.test_due_today_and_overdue_but_not_future` covers due, overdue, and future cases. Keep this boundary in mind when changing reminder behavior.
- **The health route does not validate plant data.** It confirms that the server responds, but it deliberately bypasses the reminder path and plant storage. A successful health response does not establish that the plant file is readable or migrated.
- **Relative data paths may depend on the working directory.** The initial checkpoint notes that the default JSON paths are relative and that starting outside the project directory may prevent the service from finding its data and settings files. Treat this as a known operational risk when changing how the service is launched.
- **Documentation has changed over time.** Checkpoints describe the original `/reminders` route and `settings.json`; later documentation names `/api/reminders`, and the repository now contains `settings.yaml`. The README’s upgrade checklist also calls out renaming the interval key and installing PyYAML. Confirm the current configuration format before applying instructions written for an older version.

## Dependency Map

- **Python standard library:** The application uses Python’s built-in HTTP server machinery, JSON-backed plant data, and a local filesystem migration. The migration tests also use `tempfile.TemporaryDirectory`, `pathlib.Path`, and JSON parsing to isolate and check test data. There is no documented runtime dependency on a database or a remote plant-data service.
- **PyYAML 6.0.3:** Listed in `requirements.txt`. The README’s upgrade checklist says to install PyYAML, and the repository contains `settings.yaml`. Treat it as the configuration-related external library. The provided materials do not specify the exact current configuration keys.
- **Local HTTP clients:** The service exposes `GET /api/reminders` and `GET /health`. These are the application’s HTTP interface; no remote API provider is documented.
- **Checkpoint and `checkpoint-agent 1.2.6`:** The README describes Checkpoint running in GitHub Actions and identifies `checkpoint-agent 1.2.6`. This is part of the repository’s public demo and generated documentation workflow, not a dependency of the reminder request path.
- **GitHub Actions:** The README says the public demo shows Checkpoint running in GitHub Actions. The provided file structure does not list a workflow file, so its exact configuration is not described here.
- **External runtime services:** The initial checkpoint says Sprout uses no external services. The reminder server’s documented operation is local and file-based.

## Getting Started

1. **Review the project guidance.** Read `README.md` for the current project framing and basic commands. Read `docs/upgrade.md` before working with an existing installation or changing the plant-data format. Treat `checkpoints/` and `catchups/` as generated project-history and briefing material, not as application modules.
2. **Set up Python dependencies.** Run `python -m pip install -r requirements.txt` from the repository. This installs the pinned PyYAML dependency.
3. **Check the local data and configuration.** Inspect `plants.json` and `settings.yaml` before changing reminder behavior. The tracked plant data is sample data, not a production database. The upgrade documentation identifies a configuration interval-key rename, but the exact key names are not present in the provided materials. **[Verify]** Confirm the expected key in the current `settings.yaml` and the loader before editing or creating configuration.
4. **Run the tests.** Use the README command: `python -m unittest discover -s tests`. `tests/test_reminders.py` covers due-date behavior; `tests/test_migration.py` checks backup preservation, repeat migration, and protection against overwriting an existing backup.
5. **Migrate existing v1 data when needed.** If you are working with an older plant file that lacks `schema_version` and uses `watered_at`, stop the service and follow `docs/upgrade.md`. The documented command is `python -m sprout.migrate`; the migration defaults to `plants.json`. It creates a `.json.bak` backup and returns `False` when the data is already v2. Do not assume the tracked sample file represents an installation’s data.
6. **Start the server.** Run `python -m sprout.server` from the project directory. The README documents localhost:8080. Starting from the project directory also avoids the relative-path issue noted in the checkpoint.
7. **Check the endpoints.** Request `GET /api/reminders` on localhost:8080 to exercise the data-loading and reminder calculation path. Request `GET /health` to check server responsiveness; a successful response is HTTP 204 with no body and does not verify that plant data can be loaded.
8. **Before changing compatibility behavior, check the upgrade path.** The documented upgrade sequence calls out the interval-key rename, switching clients to `GET /api/reminders`, installing PyYAML, and migrating plant data. Follow `docs/upgrade.md` for existing installations rather than relying on historical checkpoint descriptions of earlier filenames or routes.