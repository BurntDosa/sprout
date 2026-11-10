# Master Context

Sprout is a small, local plant-watering reminder API. It reads plant records and reminder settings from files, calculates which plants are overdue, and serves the result over HTTP. The service is deliberately narrow: it offers a read-only reminders endpoint and a health check, not a plant-management interface or a production database. The checked-in `plants.json` is sample data. The current README also presents Sprout as a public demo of Checkpoint, a tool that generates commit summaries, returning-author briefings, and onboarding material. Its project history is fictional; the application’s purpose is still to demonstrate a simple reminder service and the generated Checkpoint artifacts.

This repository has two related concerns. The `sprout/` package and `tests/` implement and check the reminder service. The `checkpoints/`, `catchups/`, and `MASTER_CONTEXT.md` files document the fictional project history and Checkpoint output. The README identifies the October 2026 history as fictional. Treat the application’s file-based plant data as demonstration input, not as operational production data.

## Architecture Overview

The application is organized as a small Python package. `sprout/reminders.py` owns settings and plant-data loading, plus the calculation of which plants need watering. `sprout/server.py` provides the HTTP entry point and routes requests. `sprout/migrate.py` handles the plant-data format upgrade. The `tests/` directory covers the health endpoint, reminder calculation, and migration behavior. Configuration and sample data live at the repository root in `settings.yaml` and `plants.json`.

The main reminders flow is:

1. Start the server with `python -m sprout.server`.
2. The server accepts requests on localhost. The README documents the reminders API at localhost:8080.
3. A request to `GET /api/reminders` is handled by `Handler.do_GET()`.
4. The reminders path loads settings and plant data, then calls `due_plants(...)` to identify plants past their configured watering interval.
5. The server returns the due plants as JSON. It does not update the plant records.

The current endpoint is `/api/reminders`. An earlier checkpoint describes `/reminders` and a JSON settings file; later upgrade documentation records the move to `/api/reminders`, a settings-key rename, and installation of PyYAML. Follow the current README and files rather than relying on that earlier interface description.

The calculation uses the plant’s `last_watered` date and the configured reminder interval. A plant is due only when its last-watered date plus the interval is earlier than today. It is not due on the exact threshold date. The schema-v2 data format uses `last_watered`; legacy v1 records use `watered_at`.

`GET /health` is separate from the reminders path. `Handler.do_GET()` responds with HTTP 204 and no body, then returns without loading plant data. This makes the health route a check that the server responds, not a check that the plant file is readable or valid. Requests to paths other than `/health` and `/api/reminders` receive 404.

For existing v1 plant data, `sprout.migrate.migrate()` performs the format change before the service loads the file. It adds `schema_version: 2`, renames each plant’s `watered_at` field to `last_watered`, preserves the original file in a `.json.bak` backup, and replaces the source file through a temporary `.json.tmp` file. The migration command defaults to `plants.json`; running the module invokes the migration. `load_plants()` rejects files that are not schema version 2 and directs operators to migrate them.

The supplied dependency and class-hierarchy diagram settings say diagrams are disabled, and no Mermaid source diagrams were provided. There is no diagram to reproduce here. In practical terms, the core runtime path is `server.py` → `reminders.py` → `settings.yaml` and `plants.json`; migration is a separate command, and tests exercise the endpoints and file-format behavior.

## Key Decision Log

- **Keep reminder calculation apart from HTTP handling.** The checkpoint describes `sprout/reminders.py` as separate from `sprout/server.py`: the former loads data and calculates due plants, while the latter serves HTTP responses. The initial change established a read-only entry point rather than a complete plant-management system. The rationale for this split beyond that scope is not documented.

- **Use local JSON plant data rather than a production persistence layer.** The README and checkpoints identify `plants.json` as sample data, not a production database. The initial service was described as using no external services. This keeps the demo simple, but it means this repository does not provide a production data store. The rationale for choosing JSON specifically is not documented.

- **Version the plant-data schema and require an explicit migration.** Schema v2 adds `schema_version` and changes the date field from `watered_at` to `last_watered`. `load_plants()` rejects older or unversioned data rather than silently accepting it. The upgrade notes require migrating existing v1 data before starting the service. The documented behavior makes incompatible data visible and provides a one-time upgrade path.

- **Back up legacy data before replacing it during migration.** `migrate()` saves the original bytes to a `.json.bak` file before replacing the source through a temporary file. The migration tests check that the backup preserves the original contents, repeat migration is safe, and an existing backup prevents overwrite. The checkpoint presents backup preservation and safe repeated migration as intended behavior.

- **Keep health checks independent of plant storage.** The health route returns 204 before entering the reminders handling path. The checkpoint confirms it does not load plant storage. This allows a check of server responsiveness without depending on the data file; broader health-check rationale is not documented.

## Gotchas & Tech Debt

- **Migrate old plant files before starting the service.** `load_plants()` requires schema version 2. Existing v1 records need `python -m sprout.migrate` first. The migration guide says to stop the service, run the migration once, and then resume using it. Do not assume the service will read an old `watered_at` record.

- **An existing backup blocks migration.** The migration opens the `.json.bak` file exclusively. If that backup already exists, migration raises `FileExistsError` and leaves the source file unchanged. The migration test explicitly checks this behavior. Review the existing backup before deciding what to do; do not delete it blindly.

- **The due-date boundary is strict.** `due_plants()` returns plants whose last-watered date plus the interval is earlier than today. A plant that reaches the threshold today is not included until the following day. This is established behavior, not an inclusive “due on” comparison.

- **The health route does not validate plant data.** A 204 from `/health` confirms that the server handled the health request. It does not show that `plants.json` can be loaded or that reminders can be calculated.

- **Relative data paths can depend on the working directory.** The initial checkpoint notes that default JSON paths are relative and that starting outside the project directory may prevent finding the data and settings files. The current repository has `settings.yaml`; verify the actual path handling if launching the service from another directory.

- **The configuration transition is documented as an upgrade concern.** The README’s upgrade sequence calls out renaming the interval key, using `GET /api/reminders`, installing PyYAML, and migrating plant data. The supplied materials do not identify the old and new interval-key spellings, so check `settings.yaml` and `docs/upgrade.md` before carrying configuration forward.

- **The sample data is not a production database.** The README and checkpoints make this distinction directly. There is no documented production persistence layer or plant-editing API in the supplied structure.

- **The project history and authors are fictional.** The README says the October 2026 commits are fictional and frames the repository as a Checkpoint demo. Do not treat the checkpoint history as evidence of a real deployment or production incident.

## Dependency Map

- **Python standard library:** The service uses Python modules and `unittest`; the migration tests also use temporary directories, paths, and JSON handling. `HTTPServer` is identified in the initial checkpoint as the server implementation. The supplied materials do not state a supported Python version.

- **PyYAML 6.0.3:** This is the sole entry in `requirements.txt`. The upgrade documentation says to install PyYAML, and the current settings file is `settings.yaml`. It is a runtime dependency for YAML settings. The exact settings key names are not stated in the supplied checkpoint excerpts.

- **Local configuration and data files:** `settings.yaml` provides service configuration. `plants.json` contains the sample plant data. These are files, not external services. The checkpoint history says the application started with a JSON settings file and later documents a configuration transition; use the current repository files as the source of truth.

- **HTTP API clients:** Clients call `GET /api/reminders` to retrieve due plants. `GET /health` returns 204 with no response body. The service is documented on localhost:8080. Other paths return 404.

- **Checkpoint and GitHub Actions context:** The README links Checkpoint and `checkpoint-agent 1.2.6`, and describes generated summaries, briefings, and onboarding material. This is the repository’s demo/documentation context, not a runtime dependency of the reminder API. A checkpoint notes that a documentation change did not verify that a GitHub Actions workflow exists; do not assume one from the README alone.

## Getting Started

1. **Check the current files before running commands.** Start with `README.md`, `docs/upgrade.md`, `settings.yaml`, and `plants.json`. The README is the current entry point; earlier checkpoints describe older endpoint and configuration states.

2. **[Verify] Check that your installed Python version is suitable.** The supplied README and dependency manifest do not specify a supported Python version.

3. **Install the declared dependency:**
   ```sh
   python -m pip install -r requirements.txt
   ```

4. **Run the test suite:**
   ```sh
   python -m unittest discover -s tests
   ```
   The repository includes `tests/test_health.py`, `tests/test_migration.py`, and `tests/test_reminders.py`. These cover health behavior, migration behavior, and reminder calculation.

5. **If you are using existing v1 plant data, migrate it before starting the service.** Follow `docs/upgrade.md`. The documented migration command is:
   ```sh
   python -m sprout.migrate
   ```
   It defaults to `plants.json`. It creates a `.json.bak` backup and does not overwrite an existing backup. If you are using the checked-in sample, the checkpoint records it as schema v2; inspect the file before deciding whether migration is needed.

6. **Start the server:**
   ```sh
   python -m sprout.server
   ```
   The README documents the service on localhost:8080. The initial checkpoint says the server binds to `127.0.0.1` using a configured port; check `settings.yaml` if the port differs in your checkout.

7. **Check the endpoints.** Request `GET /health` to confirm the server responds; expect HTTP 204 and no body. Request `GET /api/reminders` to get the due plants as JSON. The health response does not confirm that plant data can be loaded, so exercise the reminders endpoint as well.

8. **When upgrading an existing installation, use the complete documented sequence.** The README calls out the settings interval-key rename, switching clients to `GET /api/reminders`, installing PyYAML, and migrating plant data. **[Verify]** Consult `docs/upgrade.md` for the exact configuration-key change; the supplied materials do not give the key spellings.