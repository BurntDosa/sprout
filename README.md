# Sprout

Sprout is a small plant-reminder API with fictional authors and history. This public demo shows [Checkpoint](https://github.com/BurntDosa/Checkpoint) running in GitHub Actions with [Checkpoint `fix/demo-findings` at `a0f2e5c`](https://github.com/BurntDosa/Checkpoint/commit/a0f2e5c5688e4e924f691252e94cb4ceaa07a1df).

Checkpoint writes commit and PR summaries to [`checkpoints/`](checkpoints/), returning-author briefings to [`catchups/`](catchups/), and the onboarding guide to [`MASTER_CONTEXT.md`](MASTER_CONTEXT.md). The October 2026 commits are fictional; the generated documents come from live Checkpoint runs.

Install with `python -m pip install -r requirements.txt`, then run `python -m unittest discover -s tests`. Run `python -m sprout.server` and request `GET /api/reminders` on localhost:8080. Existing installations should follow [`docs/upgrade.md`](docs/upgrade.md).
