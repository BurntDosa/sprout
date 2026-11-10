## Commit `8fc5265` — 2026-11-10

## Context
The `ci: track generated Checkpoint documents` commit removes ignore rules that prevented generated Checkpoint-related documents from appearing in Git. This lets the repository track those documents instead of treating them as local-only files.

## Changes
- `.gitignore`: Removed the `checkpoints/` and `catchups/` directory patterns and the `MASTER_CONTEXT.md` pattern. No functions or classes changed.

## Impact
Git no longer ignores files solely because they are under `checkpoints/` or `catchups/`, or named `MASTER_CONTEXT.md`. Those files can now be staged and committed. Likely: existing untracked files matching these patterns will appear in `git status`, unless another ignore rule excludes them.

## Priority Rating
LOW — This changes which generated files Git can track, but the diff does not alter application or CI behavior.

---

## Commit `33cf8bc` — 2026-11-10

## Context
The change adds a dedicated health endpoint, as stated in the commit message. Before this change, `Handler.do_GET` only accepted `/api/reminders`; other paths returned 404. The new route can report that the server is responding without entering the reminders path that loads plant data.

## Changes
- `sprout/server.py` — `Handler.do_GET` now checks for `/health` first. It responds with HTTP 204, ends the headers, and returns before the existing path check and reminder handling.

## Impact
- Confirmed: `GET /health` returns 204 with no response body and does not call the reminder-handling path or load plant storage.
- Confirmed: Requests to paths other than `/health` and `/api/reminders` still receive 404.
- Likely: Health checks can verify server responsiveness without depending on plant storage being available.

## Priority Rating
LOW — This adds a small, isolated endpoint and leaves the existing reminders route unchanged.

---

## Commit `b9d8436` — 2026-11-10

## Context
Plant storage previously used an implicit v1 format: `plants.json` had no schema marker and stored watering dates as `watered_at`. The commit introduces explicit schema v2, with a `schema_version` field and the renamed `last_watered` date. The upgrade notes require existing v1 data to be migrated before the service starts; `load_plants` now rejects files without schema version 2.

## Changes
- **`sprout/migrate.py` — `migrate`:** Adds the migration command, defaulting to `plants.json`. It leaves schema v2 files untouched by returning `False`, treats a missing version as v1, and raises `ValueError` for other unsupported versions. For v1, it renames each plant’s `watered_at` field to `last_watered`, sets `schema_version` to 2, writes the original bytes to a `.json.bak` file opened exclusively, then replaces the data file via a temporary `.json.tmp` file. Running the module invokes `migrate()`.
- **`sprout/reminders.py` — `load_plants`:** Checks for schema version 2 and raises an error directing operators to run the migration otherwise. **`due_plants`** now reads `last_watered` when calculating which plants are due.
- **`plants.json`:** Updates the sample data to schema v2 and `last_watered`.
- **`tests/test_reminders.py` — `ReminderTests.test_due_today_and_overdue_but_not_future`:** Updates test plant records to use `last_watered`.
- **`docs/upgrade.md`:** Documents stopping the service, running `python -m sprout.migrate` once on existing v1 data, and the backup and already-migrated-file behavior. It also retains instructions for the settings rename and reminder endpoint change.

## Impact
Confirmed: v1 storage must be migrated before `load_plants` accepts it; reminder calculations use the renamed field, and the checked-in sample and reminder test data match that format. The migration creates a backup before replacing the source. Likely: deployments that start without migrating existing plant files will fail during plant loading rather than silently reading the old format.

## Priority Rating
MEDIUM — Existing data requires a one-time migration before startup, but the command backs up the source and skips files already at v2.

---

## Commit `24153c1` — 2026-11-10

## Context
The `test: cover overdue and due-today reminder boundaries` commit adds coverage for how `due_plants` handles reminder dates. The test checks the boundary between plants that are due or overdue and plants whose watering date is still in the future.

## Changes
- `tests/test_reminders.py`: Adds `ReminderTests.test_due_today_and_overdue_but_not_future`. It calls `due_plants` with a seven-day watering interval and three plants last watered on October 1, 2, and 3, 2026. For October 8, it expects only Fern; for October 9, it expects Fern and Ivy.

## Impact
- Confirmed: The test verifies that a plant due on the supplied date is included, overdue plants remain included, and a plant due later is excluded.
- Confirmed: The diff adds test coverage only; it does not change `sprout.reminders` implementation.
- Likely: This test will help catch regressions in reminder-date boundary handling.

## Priority Rating
LOW — The change adds focused regression coverage without altering application behavior.

---

## Commit `af60d81` — 2026-11-10

## Context

The service previously exposed reminders at the root-level path `/reminders`. This change moves the endpoint into an `/api` namespace, as indicated by the commit message. The upgrade notes make the compatibility break explicit: clients must switch to `GET /api/reminders`, because the old path now returns 404. The existing `reminder_days` to `watering_interval_days` setting rename remains part of the upgrade guidance.

## Changes

- `README.md`: Updates the example request to `GET /api/reminders` on localhost:8080. The server command and test command are unchanged.
- `docs/upgrade.md`: Adds a migration note directing clients to `GET /api/reminders` and stating that `/reminders` returns 404. The existing setting-rename instruction is retained.
- `sprout/server.py`: In `Handler.do_GET`, changes the accepted path from `/reminders` to `/api/reminders`. Requests to any other path still call `send_error(404)` and return. For the accepted path, the existing calls to `load_settings()` and the reminder-handling flow remain in place.

## Impact

- Confirmed: `GET /api/reminders` is now the accepted reminders path; `GET /reminders` receives a 404 response.
- Confirmed: The README and upgrade notes document the new route, including the required client migration.
- Confirmed: The diff does not change the server startup command, test command, or reminder data/settings logic.
- Likely: Existing clients configured for `/reminders` will need a URL update before they can retrieve reminders.

## Priority Rating

MEDIUM — The route change is a client-visible breaking change, but the upgrade notes identify the required URL migration.
