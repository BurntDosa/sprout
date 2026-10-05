# Upgrade notes

Rename `reminder_days` to `watering_interval_days` before starting the service.
Clients must use `GET /api/reminders`; `/reminders` now returns 404.
