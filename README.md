# Sprout

Fictional example: a small plant-watering reminder service. Cleo and Ben maintain
it while Ava is away; Darren is joining the project. No external services.

Install `python -m pip install -r requirements.txt`.
Settings live in `settings.yaml` (requires PyYAML).
Run `python -m sprout.server` and request `GET /api/reminders` on localhost:8080.
Run tests with `python -m unittest discover -s tests`.
The tracked `plants.json` is sample data, not a production database.
