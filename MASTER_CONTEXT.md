# Master Context

Sprout is a small, read-only plant-watering reminder API. It loads plant records and reminder settings from local files, calculates which plants are due, and exposes the results over HTTP. It does not send notifications or update watering dates. Its checked-in plant data is a sample, not a production database.

The repository also serves a second purpose: it is a public demo of Checkpoint running in GitHub Actions. Checkpoint produces commit and PR summaries in `checkpoints/`, returning-author briefings in `catchups/`, and this onboarding guide in `MASTER_CONTEXT.md`. The README says the October 2026 project history is fictional; the generated documents come from live Checkpoint runs. Treat the service and its history as a demo, and use the current README and upgrade notes when operating it.

The core path through the application is deliberately small: configuration and plant records go into reminder logic; an HTTP handler exposes that logic; tests cover reminder calculation and migration. There is no documented write API, notification integration, production storage layer, or external service required to run the reminder API.

## Architecture Overview

The source package is `sprout/`. Its responsibilities are split across three modules:

- `sprout/reminders.py` owns data loading and reminder calculation. The checkpoint history names `load_settings()` and `load_plants()` as the loaders, and `due_plants()` as the function that selects records due for watering. Keeping these operations outside the HTTP handler gives the calculation and file-loading logic a place to be tested independently of HTTP.
- `sprout/server.py` provides the HTTP interface. Its `Handler.do_GET()` serves the health and reminder routes. The module entry point starts the server; the documented run command is `python -m sprout.server`.
- `sprout/migrate.py` upgrades plant data from the older storage format. Its `migrate(path=Path('plants.json'))` function handles the file conversion, and running the module directly invokes the migration.

At a high level, the reminder request flow is:

```text
GET /api/reminders
        |
        v
sprout.server: Handler.do_GET()
        |
        v
sprout.reminders: load settings and plant records
        |
        v
sprout.reminders: due_plants(...)
        |
        v
JSON response
```

The health check takes a separate, shorter path. `GET /health` returns HTTP 204 with no body and exits without calling `due_plants()`, `load_plants()`, or `load_settings()`. That means the route checks whether the HTTP server responds, not whether configuration and plant storage are readable. Requests to paths other than `/health` and `/api/reminders` return 404, according to the checkpoint history.

The data flow is file-based. The repository contains `plants.json` and `settings.yaml`. The checkpoint history documents `plants.json` as the plant-record file and describes the reminder settings as loaded from a configurable path. Earlier revisions used `settings.json`; the current tree has `settings.yaml`, and the README’s upgrade guidance says to install PyYAML. Confirm the current settings format and keys when changing configuration rather than assuming the historical JSON format still applies.

Plant storage has an explicit version boundary. Version 2 uses a top-level `schema_version` and the plant date field `last_watered`. The prior v1 shape used `watered_at`; unversioned files are treated as v1 by the migration. `load_plants()` requires schema version 2, so old data must be migrated before the reminder service can load it. `due_plants()` compares each plant’s `last_watered` date against the configured reminder interval and the supplied date. The checkpoint history records a seven-day interval in an earlier settings file; consult the current configuration for the active value.

`sprout/migrate.py` is deliberately separate from serving reminders. For v1 input, it makes a `.json.bak` copy of the original bytes, writes converted data through a `.json.tmp` file, and replaces the source. It returns `False` if the file is already v2 and raises `ValueError` for unsupported schema versions. Tests in `tests/test_migration.py` cover the backup, repeat-call, and existing-backup behavior. Reminder calculation tests live in `tests/test_reminders.py`.

There are no Mermaid diagrams in the supplied material. The dependency and class-hierarchy diagrams are explicitly disabled in the provided configuration, so the flow above is a text summary rather than a generated diagram.

## Key Decision Log

1. **Keep reminder logic separate from HTTP handling.** `sprout/reminders.py` contains loading and due-date logic; `sprout/server.py` handles requests. The checkpoint describes this separation as the structure of the service. It makes the HTTP layer a consumer of the reminder logic rather than the owner of it. Rationale for this separation is documented as separating reminder logic from HTTP handling.

2. **Expose reminders through a read-only HTTP API.** The API returns due plants but does not provide a documented write route or notification delivery. The initial checkpoint explicitly confirms that the endpoint only reads data and adds no write path or external-service integration. The README documents `GET /api/reminders` as the route to use. Rationale not documented.

3. **Version plant data and require migration before loading old files.** The v2 format adds `schema_version` and renames `watered_at` to `last_watered`. The loader rejects data that has not been migrated. The upgrade notes say to stop the service and run the migration once, avoiding the service reading storage during replacement. This gives maintainers a clear upgrade step and leaves a backup of the original file. Rationale for stopping the service during replacement is documented in the upgrade guidance.

4. **Use a lightweight health endpoint that bypasses storage.** `GET /health` returns 204 without loading settings or plant records. The checkpoint describes this as allowing a health response without reading plant storage. Rationale not documented beyond the stated behavior.

5. **Keep the plant file as demo data, not production storage.** The README and checkpoint describe the sample record as an example and explicitly say `plants.json` is not a production database. Rationale not documented.

## Gotchas & Tech Debt

- **Old plant files will not load until migrated.** `load_plants()` requires `schema_version == 2`. Older v1 or unversioned files need `python -m sprout.migrate` before the reminder service can use them. The migration changes `watered_at` to `last_watered`.

- **Plan the migration as an offline step.** The upgrade notes say to stop the service before running the migration. The migration writes a backup and a temporary file before replacing the source; do not treat it as a live, concurrent update.

- **A pre-existing backup blocks migration.** The migration tests specify that an existing `.json.bak` file must not be overwritten: `migrate()` raises `FileExistsError`, and the source remains unchanged. Resolve that situation deliberately rather than deleting a backup without checking it.

- **The health check is not a storage check.** `/health` can return 204 even when plant data or settings cannot be loaded, because the route bypasses those loaders. A successful health response does not establish that `/api/reminders` will succeed.

- **The API path changed.** The README points callers to `/api/reminders`. Checkpoint history records an earlier `/reminders` path and subsequent upgrade guidance to switch clients to `/api/reminders`. Do not assume the historical path remains valid.

- **Configuration has changed across revisions.** The history describes an earlier `settings.json` and documents a settings rename; the current repository tree contains `settings.yaml`, and the README says to install PyYAML. Check the current file and upgrade notes before carrying forward older configuration or scripts.

- **Sample data is not an operational database.** `plants.json` is tracked sample data. The service is read-only, so it does not record watering actions or provide notification delivery. Any workflow needing those capabilities must not assume they exist here.

- **The demo’s automation description is not proof of workflow contents.** The README presents the repository as a Checkpoint demo in GitHub Actions. A checkpoint notes that its documentation diff did not show a GitHub Actions workflow. The supplied file tree also does not list a workflow file, so this document cannot describe its implementation.

## Dependency Map

- **Python standard library:** The service uses Python’s HTTP server, JSON handling, and test tooling as described by the checkpoints and README. `python -m sprout.server` starts the API; `python -m unittest discover -s tests` runs the tests. No separate application server dependency is listed.

- **PyYAML 6.0.3:** `requirements.txt` pins `PyYAML==6.0.3`. The README’s upgrade guidance specifically says to install PyYAML. Its role is associated with the current YAML settings file; verify the exact loading behavior in the current source before changing configuration.

- **Local plant storage:** `plants.json` holds the sample plant records. It is not an external service and is explicitly not a production database. The migration module also defaults to this path.

- **Local settings:** `settings.yaml` is present in the repository. Settings determine reminder behavior, and the checkpoint history documents a configurable interval and port. Confirm the current keys and values in the file before relying on historical settings details.

- **Checkpoint:** The README links to Checkpoint’s `fix/demo-findings` branch at commit `f3d94ae` and says Checkpoint runs in GitHub Actions to produce repository documents. That is the demo/documentation side of the repository, not a runtime dependency of the plant reminder API. The supplied files do not describe the workflow’s implementation.

- **External services and notification APIs:** None are required or documented for the reminder API. The checkpoint confirms that the service adds no external-service integration and does not itself send notifications.

## Getting Started

1. **Check the project instructions.** Read `README.md` and `docs/upgrade.md` before running or changing an existing installation. The README identifies the service as a demo and points maintainers to the upgrade guide.

2. **Use a Python environment.** The repository’s ignore rules, as described by the checkpoint, exclude `.venv/`. Create and activate a virtual environment using your team’s usual Python workflow. **[Verify]** The supplied README does not specify a Python version or provide environment-creation commands.

3. **Install dependencies.** Run the documented command:

   ```sh
   python -m pip install -r requirements.txt
   ```

   This installs the pinned PyYAML dependency. **[Verify]** The supplied materials do not state a Python version constraint.

4. **Inspect the current data and settings.** Look at `plants.json` and `settings.yaml` before starting the server. Confirm that plant data has `schema_version` 2 and uses `last_watered`. Check the settings file for the active interval and port rather than copying values from an older checkpoint.

5. **Migrate old plant data if needed.** If an existing plant file is v1 or unversioned, stop the service and run:

   ```sh
   python -m sprout.migrate
   ```

   The migration creates a `.json.bak` backup and refuses to overwrite an existing backup. Review `docs/upgrade.md` and preserve the backup according to your operational practices.

6. **Run the tests.** Use the README command:

   ```sh
   python -m unittest discover -s tests
   ```

   The suite includes `tests/test_reminders.py` for reminder behavior and `tests/test_migration.py` for migration safety.

7. **Start the API.** Run:

   ```sh
   python -m sprout.server
   ```

   The documented default is localhost on port 8080. **[Verify]** The available checkpoint describes that default for an earlier configuration revision; confirm the active port in `settings.yaml`.

8. **Check the routes.** Request `GET /api/reminders` on localhost:8080 to retrieve the due plants as JSON. Request `GET /health` to get a 204 response without a body. Other paths return 404. **[Verify]** If you changed the configured port, use that port instead of 8080.

9. **When upgrading, update clients and configuration deliberately.** The README points to `docs/upgrade.md` for the interval-key rename, the `/api/reminders` path, the PyYAML dependency, and plant-data migration. Apply those notes to existing installations rather than assuming files and clients from an earlier revision remain compatible.