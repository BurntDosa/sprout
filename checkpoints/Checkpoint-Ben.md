## Commit `8fc5265` — 2026-11-10

## Context
The commit message says the repository should track generated Checkpoint documents. The existing `.gitignore` rules excluded the `checkpoints/` and `catchups/` directories and `MASTER_CONTEXT.md`, preventing Git from noticing untracked files at those paths.

## Changes
- **`.gitignore`**: Removed ignore patterns for `checkpoints/`, `catchups/`, and `MASTER_CONTEXT.md`. The remaining rules still ignore Python cache files, `.venv/`, and `.env`. No functions or classes changed.

## Impact
Git will no longer ignore files under `checkpoints/` or `catchups/`, or the `MASTER_CONTEXT.md` file, so they can be added and committed. Removing these rules does not automatically add existing files to version control. **Likely:** Future generated Checkpoint documents can now be reviewed and shared through normal Git changes.

## Priority Rating
LOW — This enables tracking generated documents without changing application behavior or existing ignore rules for environments and Python caches.

---

## Commit `33cf8bc` — 2026-10-08

## Context
The commit adds a health endpoint that can respond without reading plant storage. Previously, `Handler.do_GET` only accepted `/api/reminders`; other paths returned 404. The new route exits before reminder handling.

## Changes
- `sprout/server.py` — `Handler.do_GET` now recognizes `/health`, sends HTTP 204, ends the response, and returns. The route does not call `due_plants`, `load_plants`, or `load_settings`.

## Impact
- Confirmed: `GET /health` returns 204 with no response body and bypasses the reminder route’s storage-related work.
- Confirmed: requests to paths other than `/health` and `/api/reminders` still receive 404.
- Likely: monitoring or deployment checks can test server responsiveness without requiring plant storage to be readable.

## Priority Rating
LOW — This adds a lightweight health check without changing reminder behavior.

---

## Commit `b9d8436` — 2026-10-07

## Context
Plant storage previously used an implicit v1 shape: a top-level `plants` list with each plant’s watering date in `watered_at`. The commit makes the format explicit by adding `schema_version` and moving to v2, where the date field is `last_watered`. The reminder loader now rejects files that have not been migrated, so existing data must be upgraded before the service starts. The upgrade notes specify stopping the service and running the migration once; this avoids the service reading storage during replacement.

## Changes
- `sprout/migrate.py`: Adds `migrate(path=Path('plants.json'))`. It returns `False` without changing a file already marked v2, accepts v1 or unversioned data as v1, and raises `ValueError` for other schema versions. For v1, it renames each plant’s `watered_at` field to `last_watered`, sets `schema_version` to 2, writes the original bytes to a `.json.bak` file, then replaces the source via a `.json.tmp` file. Running the module directly invokes `migrate()`.
- `sprout/reminders.py`: `load_plants()` now requires `schema_version == 2` and gives an instruction to run the migration otherwise. `due_plants()` reads `last_watered` when determining which plants are due.
- `plants.json`: Updates the sample data to schema v2 and uses `last_watered`.
- `tests/test_reminders.py`: Updates `test_due_today_and_overdue_but_not_future` fixtures to use `last_watered`.
- `docs/upgrade.md`: Documents the migration command and backup behavior, and retains the existing settings rename and reminder endpoint upgrade notes.

## Impact
Confirmed: v1 storage no longer loads through `load_plants()` until migrated; v2 data is the required input for reminders. Migration preserves the original file in a backup and uses a temporary file before replacing it. The due-date calculation still uses the configured `watering_interval_days`, now with the renamed date field. Likely: deployments with existing plant data need a planned stop-and-migrate step to avoid startup failure.

## Priority Rating
MEDIUM — Existing installations must migrate storage before startup, but the change includes a migration command and backup path.

---

## Commit `24153c1` — 2026-10-06

## Context
The `test: cover overdue and due-today reminder boundaries` commit adds a regression test for how `due_plants` handles watering dates at and around the reminder threshold. The test checks both the day a plant becomes due and the following day, while ensuring a plant with a later due date is excluded.

## Changes
- `tests/test_reminders.py`: Adds `ReminderTests.test_due_today_and_overdue_but_not_future`. It passes three plants watered on October 1, 2, and 3, 2026, to `due_plants` with a seven-day watering interval. For October 8, it expects only Fern; for October 9, it expects Fern and Ivy.

## Impact
- Confirmed: The test asserts that a plant due on the supplied date is included, an overdue plant remains included, and a plant due in the future is excluded.
- Likely: These assertions will help catch regressions in the reminder date-boundary behavior.

## Priority Rating
LOW — This adds focused test coverage without changing production code.

---

## Commit `af60d81` — 2026-10-05

## Context

The reminder service’s public route is moving from `/reminders` to `/api/reminders`, as stated in the commit message. The diff updates the server and both pieces of user-facing documentation to use the new path. It does not show a compatibility route for the old path, so clients must change their requests.

## Changes

- `sprout/server.py`: `Handler.do_GET` now accepts only `GET /api/reminders`. Requests with any other path receive a 404 before settings or plant data are loaded.
- `README.md`: The run instructions now tell developers to request `GET /api/reminders` on localhost:8080.
- `docs/upgrade.md`: The upgrade notes explicitly tell clients to use `GET /api/reminders` and state that `/reminders` returns 404.

## Impact

- Confirmed: The server no longer serves reminders at `/reminders`; that path follows the handler’s 404 branch. The new `/api/reminders` path proceeds through the existing settings and plant-loading flow.
- Confirmed: The README and upgrade notes document the new route and the old route’s failure behavior.
- Likely: Any client or test that still requests `/reminders` will need to be updated to avoid 404 responses. The diff does not show changes to client code or tests.

## Priority Rating

MEDIUM — The route change is a breaking interface change for callers of `/reminders`, but the upgrade notes document the required migration.
