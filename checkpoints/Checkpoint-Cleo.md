## Commit `bbfb761` — 2026-11-10

## Context
The commit adds a regression test for storage-free health checks. The test treats opening plant storage during a `/health` request as a failure, matching the intent in the commit message.

## Changes
- `tests/test_health.py`: Adds `HealthTests.test_health_does_not_open_plant_storage`. It creates a `sprout.server.Handler` without running its initializer, sets the request path to `/health`, and mocks response methods. It patches `sprout.server.load_plants` to raise if called, then invokes `handler.do_GET()`. The test asserts that the handler sends status `204` and ends the response headers.

## Impact
- Confirmed: The test fails if `Handler.do_GET()` calls `load_plants` during this `/health` request.
- Confirmed: The test checks that this request responds with `204` and calls `end_headers()` once.
- Likely: This guards health checks against depending on plant storage availability, helping keep them usable when storage cannot be opened.

## Priority Rating
LOW — This is a focused regression test; the diff does not change production behavior.

---

## Commit `bbfb761` — 2026-11-10

## Context
The commit adds a regression test for the `/health` endpoint. The commit message identifies the goal: guard health checks from opening storage. The test verifies that handling this request does not call `load_plants`.

## Changes
- `tests/test_health.py` adds `HealthTests.test_health_does_not_open_plant_storage`.
- The test creates a `Handler` instance without running its initializer, sets its path to `/health`, and mocks `send_response` and `end_headers`.
- It patches `sprout.server.load_plants` to raise an `AssertionError` if called, then invokes `handler.do_GET()`.
- It asserts that the handler sends status `204` and ends the response headers.

## Impact
Confirmed: the test fails if this health-check request attempts to load plant storage, and checks the expected response status and header completion. Likely: this helps prevent storage access from becoming a dependency of health checks during future changes. The diff adds a test only; it does not change the handler implementation.

## Priority Rating
LOW — this is a focused regression test and introduces no production-code changes.

---

## Commit `995d5cd` — 2026-11-10

## Context
The commit frames Sprout as a public demo of Checkpoint running against its fictional project history. The README now says generated commit and PR summaries, returning-author briefings, and onboarding material demonstrate the tool’s output. The change is documentation-only; the diff does not include a workflow or application-code change.

## Changes
- `README.md`: Replaces the fictional project-maintenance introduction with a description of Sprout as a plant-reminder API and links to Checkpoint and `checkpoint-agent 1.2.6`.
- `README.md`: Documents `checkpoints/`, `catchups/`, and `MASTER_CONTEXT.md` as Checkpoint output locations, and identifies the October 2026 history as fictional.
- `README.md`: Keeps installation, test, server, and upgrade instructions, but removes the PyYAML/settings details, the `/api/reminders` request example, the `/health` behavior, and the note about `plants.json`.

## Impact
The README now points readers to the described Checkpoint artifacts and identifies the demo’s fictional history. The diff does not verify that those artifacts or a GitHub Actions workflow exist. Likely: readers returning to the project will rely less on the README for configuration and endpoint details.

## Priority Rating
LOW — This change updates project framing and documentation without changing application behavior.

---

## Commit `ee814c0` — 2026-11-10

## Context
This commit documents upgrade steps for maintainers returning to existing installations. The README now points readers to a dedicated upgrade guide and calls out the migration actions before they resume using the service.

## Changes
- `README.md`: Adds a link to `docs/upgrade.md` and lists the upgrade sequence: rename the interval key, switch clients to `GET /api/reminders`, install PyYAML, then migrate plant data. It also documents that `GET /health` returns 204 without opening the data file. No function or class changes are shown.

## Impact
- Confirmed: The README now directs existing users to the upgrade guide and names the required actions and endpoint.
- Confirmed: The README distinguishes tracked `plants.json` as sample data, not a production database.
- Likely: The checklist helps returning maintainers avoid missing compatibility and dependency changes during an upgrade.

## Priority Rating
LOW — This is documentation-only; it clarifies upgrade steps without changing application behavior.

---

## Commit `277188e` — 2026-11-10

## Context (background on why this change exists — infer from the commit message and diff)

The commit adds focused coverage for the migration behavior named in the message: preserving a backup and safely handling repeated migration. The new tests exercise `sprout.migrate.migrate` against temporary `plants.json` files, so they check these cases without relying on a repository data file. No migration implementation changes are included in this diff; it documents expected behavior through tests.

## Changes (grouped by file with specific function/class names)

- `tests/test_migration.py` adds `MigrationTests`, a `unittest.TestCase` with two tests.
- `MigrationTests.test_backup_and_repeat_are_safe` writes a legacy plant record containing `watered_at`, then checks that `migrate(path)` returns `True`, creates a `.json.bak` file containing the original bytes, and writes `last_watered` as `2026-10-01` in the migrated JSON. It then calls `migrate(path)` again and expects `False`.
- `MigrationTests.test_existing_backup_prevents_overwrite` creates a source file and an existing `.json.bak` containing `keep`. It expects `migrate(path)` to raise `FileExistsError` and verifies that the source file remains unchanged.

Both tests use `tempfile.TemporaryDirectory` and `pathlib.Path` to isolate their files. The first test uses `json.loads` to check the migrated field.

## Impact (confirmed downstream effects from the diff; mark inferred impacts with 'Likely:')

The test suite now checks the return values for first and repeated migration, the backup’s contents, conversion from `watered_at` to `last_watered`, and preservation of the source when a backup already exists. These are assertions in the added tests; the diff does not show a change to `migrate` itself or confirm that the tests have been run.

Likely: these checks will catch regressions that overwrite an existing backup, fail to preserve the original data, or repeat a migration that should be a no-op.

## Priority Rating (one of: CRITICAL / HIGH / MEDIUM / LOW with one sentence justification)

MEDIUM — the tests cover data preservation and repeat-run safety, but the diff adds verification only and does not change migration behavior.

---

## Commit `ef1521b` — 2026-11-10

## Context (background on why this change exists — infer from the commit message and diff)

The commit adds YAML support for the plant-watering service’s settings. Previously, settings were stored in `settings.json` and `load_settings` parsed them as JSON. The change moves the settings file to YAML and adds PyYAML as a project dependency, so developers also need updated setup instructions.

## Changes (grouped by file with specific function/class names)

- `requirements.txt`: Adds the pinned dependency `PyYAML==6.0.3`.
- `settings.json` and `settings.yaml`: Removes the JSON settings file and adds YAML settings with the same values: `watering_interval_days: 7` and `port: 8080`.
- `sprout/reminders.py`: `load_settings` now defaults to `Path('settings.yaml')` and parses the file with `yaml.safe_load` instead of `json.loads`. The module imports `yaml`. `load_plants` is unchanged.
- `README.md`: Documents installing dependencies with `python -m pip install -r requirements.txt` and notes that settings live in `settings.yaml` and require PyYAML.

## Impact (confirmed downstream effects from the diff; mark inferred impacts with 'Likely:')

Confirmed: Calling `load_settings()` now reads `settings.yaml` by default and uses PyYAML to parse it. Installing from `requirements.txt` installs the parser version specified by the project. The documented setup path now includes dependency installation.

Likely: Code or scripts that expect `settings.json`, or call `load_settings` with JSON-formatted settings, will need updating. Deployments must include `settings.yaml` and install the requirements for settings loading to work.

## Priority Rating

MEDIUM — Settings loading and setup documentation change together, but the new dependency and configuration file must be present for the service to load settings successfully.

---

## Commit `3894c30` — 2026-11-10

## Context
`due_plants` in `sprout/reminders.py` checks whether a plant’s watering interval has elapsed. The previous strict comparison excluded plants whose next watering date was exactly today, despite the commit’s goal of including plants due on the current day.

## Changes
- `sprout/reminders.py` — `due_plants`: changed the due-date comparison from `< today` to `<= today`. A plant is now included when `watered_at` plus `watering_interval_days` equals today, as well as when that date is earlier.

## Impact
- Confirmed: `due_plants` returns plants due today alongside overdue plants.
- Likely: Callers that use this function to show or send watering reminders will now include reminders scheduled for today. The diff does not show changes to those callers or their behavior.

## Priority Rating
LOW — This corrects a one-day boundary condition in due-plant selection without changing interval calculation or plant data.

---

## Commit `b26f83c` — 2026-11-10

## Context
The configuration key for the watering reminder interval has been renamed from `reminder_days` to `watering_interval_days`. The configured value remains seven days. The upgrade note makes the required migration explicit: rename the key before starting the service.

## Changes
- `settings.json`: Replaces `reminder_days` with `watering_interval_days`; leaves `port` unchanged.
- `sprout/reminders.py`: In `due_plants`, builds the interval from `settings['watering_interval_days']` instead of `settings['reminder_days']`. The date comparison and plant selection logic are unchanged.
- `docs/upgrade.md`: Adds an upgrade instruction to rename the setting before starting the service.

## Impact
- Confirmed: `due_plants` now reads the renamed setting, and the checked-in configuration uses that name.
- Confirmed: The configured interval and service port values are unchanged.
- Likely: Existing external settings files that still use `reminder_days` will fail when `due_plants` accesses the new key unless they are updated first.

## Priority Rating
MEDIUM — the code and checked-in settings agree, but deployments using the old key need a configuration change before service startup.
