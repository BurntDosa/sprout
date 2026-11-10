## Commit `995d5cd` — 2026-11-10

## Context
The commit message says this change runs Checkpoint on Sprout’s history. The README now presents Sprout as a public demo of Checkpoint in GitHub Actions, using `checkpoint-agent 1.2.6`, rather than leading with the fictional service’s maintenance and setup history.

## Changes
- `README.md`: Replaces the project background and detailed installation, configuration, API, health-check, test, and upgrade notes. It describes Checkpoint’s outputs in `checkpoints/`, `catchups/`, and `MASTER_CONTEXT.md`, and says the October 2026 commits are fictional while the generated documents come from live Checkpoint runs. It retains installation, test, server, and upgrade instructions in shorter form. No functions or classes are changed.

## Impact
- Confirmed: README readers are directed to the Checkpoint-generated summaries and onboarding guide, and can still find basic run and upgrade instructions.
- Likely: Returning contributors will use `catchups/` and `MASTER_CONTEXT.md` as their entry points instead of relying on the removed project-history details.
- The diff changes documentation only; it does not show a GitHub Actions workflow or application-code changes.

## Priority Rating
LOW — This is a README-only change that explains the Checkpoint demo without altering application behavior.

---

## Commit `ee814c0` — 2026-10-08

## Context
The commit documents the upgrade path for maintainers returning to an existing installation. The README now calls out configuration, API, dependency, and plant-data steps, and clarifies that `plants.json` is sample data rather than a production database.

## Changes
- `README.md`: Adds upgrade guidance pointing to `docs/upgrade.md`: rename the interval key, switch clients to `/api/reminders`, install PyYAML, and migrate plant data. It also documents that `GET /health` returns 204 without opening the data file. No functions or classes are changed in this diff.

## Impact
The README now directs existing-installation maintainers to the stated upgrade steps and records the health endpoint’s behavior. The diff does not implement those steps or change endpoint behavior; it only documents them. Likely: this will help returning maintainers identify migration work before running the updated service.

## Priority Rating
LOW — This is a documentation-only change; it does not alter application code or introduce runtime behavior.

---

## Commit `277188e` — 2026-10-08

## Context

The commit adds regression tests for migration behavior, as indicated by `test: verify migration backup and idempotency`. The tests exercise `sprout.migrate.migrate` against temporary `plants.json` files. They cover two cases: a successful migration that preserves the original file as a backup and can be run again safely, and an existing backup that must not be overwritten. The diff changes tests only; it does not show the migration implementation.

## Changes

- `tests/test_migration.py` adds `MigrationTests`, a `unittest.TestCase` class with two tests.
- `MigrationTests.test_backup_and_repeat_are_safe` writes a plant record with `watered_at` to a temporary file, then checks that `migrate(path)` returns `True`. It verifies that the `.json.bak` file contains the exact original bytes, that the migrated JSON has `last_watered` set to `2026-10-01`, and that a second call returns `False`.
- `MigrationTests.test_existing_backup_prevents_overwrite` creates both a source file and a `.json.bak` file containing `keep`. It checks that `migrate(path)` raises `FileExistsError` and that the source file remains unchanged.

## Impact

- Confirmed: The new tests specify expected behavior for backup creation, migration of the `watered_at` field to `last_watered`, repeat-call handling, and refusal to overwrite an existing backup.
- Confirmed: These checks use temporary directories, so the test fixtures do not write their plant files into the working tree.
- Likely: The tests make regressions in backup safety or repeated migration easier to detect when the test suite runs; the diff does not show whether or how the suite is run in CI.

## Priority Rating

MEDIUM — The tests protect data-preservation and repeat-run behavior, but the diff adds no migration implementation changes.

---

## Commit `ef1521b` — 2026-10-07

## Context

The commit adds YAML support for the plant-watering service’s settings. Before this change, `settings.json` held the watering interval and HTTP port, and `sprout/reminders.py` parsed it as JSON. The commit replaces that settings file with `settings.yaml` and adds PyYAML as a project dependency. The README now documents how to install dependencies and where settings live.

## Changes

- **`requirements.txt`** — Adds the pinned dependency `PyYAML==6.0.3`, providing the YAML parser used by the service.
- **`settings.json`** — Removes the JSON settings file, which contained `watering_interval_days: 7` and `port: 8080`.
- **`settings.yaml`** — Adds those same two settings in YAML format, preserving their values.
- **`sprout/reminders.py`** — Updates `load_settings` to default to `Path('settings.yaml')` instead of `Path('settings.json')`. The function now parses the file with `yaml.safe_load` rather than `json.loads`. The separate `load_plants` function and its `plants.json` default are unchanged.
- **`README.md`** — Adds the dependency installation command, `python -m pip install -r requirements.txt`, and explains that settings are in `settings.yaml` and require PyYAML. The existing server, API, and test commands remain in place.

## Impact

- **Confirmed:** A no-argument call to `load_settings` now reads `settings.yaml` and returns its contents parsed as YAML. The service’s settings values remain 7 days and port 8080.
- **Confirmed:** The documented setup now installs PyYAML before running the service; `settings.json` is no longer present in the diff.
- **Likely:** Callers that pass a custom path to `load_settings` must now provide YAML-formatted content, since parsing uses `yaml.safe_load` regardless of the path.
- **Likely:** Environments that run the service without installing `requirements.txt` will fail to import `sprout/reminders.py` if PyYAML is unavailable.

## Priority Rating

LOW — The change is limited to settings format, dependency setup, and documentation, while preserving the existing configuration values and run instructions.

---

## Commit `3894c30` — 2026-10-06

## Context
The reminder date check excluded plants whose watering date landed exactly on `today`: `due_plants` required the calculated date to be strictly earlier. The commit message identifies the intended correction: include plants due on the current day.

## Changes
- `sprout/reminders.py` — In `due_plants(plants, today, settings)`, the comparison changed from `< today` to `<= today`. The function still calculates the due date by adding `settings['watering_interval_days']` to each plant’s `watered_at` date.

## Impact
- Confirmed: `due_plants` now returns a plant when its calculated watering date equals `today`, as well as when that date has passed.
- Likely: Any reminder behavior driven by `due_plants` will now include plants on their due date, preventing them from being omitted until the following day.

## Priority Rating
LOW — This is a focused boundary-condition fix that makes current-day-due plants eligible without changing the date calculation or settings.

---

## Commit `b26f83c` — 2026-10-05

## Context
The commit renames the watering reminder interval setting to `watering_interval_days`. The new name describes what the value controls more specifically than `reminder_days`. The upgrade note tells operators to rename the setting before starting the service.

## Changes
- `settings.json`: Renames `reminder_days` to `watering_interval_days`; the configured value remains 7, and `port` remains 8080.
- `sprout/reminders.py`: `due_plants()` now reads `settings['watering_interval_days']` when building the `timedelta`. The due-date comparison is unchanged.
- `docs/upgrade.md`: Adds an upgrade instruction to rename the old setting before starting the service.

## Impact
`due_plants()` now requires callers to provide `watering_interval_days` in `settings`; with the updated configuration, the interval remains seven days. **Likely:** Deployments still using `reminder_days` will raise a `KeyError` when `due_plants()` accesses the missing key.

## Priority Rating
MEDIUM — The rename requires a configuration update, but the upgrade note documents the required step and the default interval is unchanged.
