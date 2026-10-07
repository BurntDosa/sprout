# Upgrade notes

Stop the service and run `python -m sprout.migrate` once on existing v1 data.
It backs up `plants.json` before replacing `watered_at` with `last_watered`.
Schema v2 is required; an already migrated file is left untouched.

Rename `reminder_days` to `watering_interval_days` before starting the service.
Clients must use `GET /api/reminders`; `/reminders` now returns 404.
