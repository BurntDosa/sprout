# While You Were Gone — Since November 10, 2026

Two README-only commits reposition Sprout as a public demo of Checkpoint and update which Checkpoint version the README points to. No application code or GitHub Actions workflow changes are shown.

## Refactors & Structural Changes

- The README now presents Sprout as a Checkpoint demo, rather than leading with the fictional service’s maintenance and setup history. It describes generated outputs in `checkpoints/`, `catchups/`, and `MASTER_CONTEXT.md`, and says the October 2026 commits are fictional while the documents come from live Checkpoint runs.
- The README keeps shorter installation, test, server, and upgrade instructions, but removes detailed background and setup, API, health-check, test, and upgrade notes. You can use `catchups/` and `MASTER_CONTEXT.md` as entry points to the project’s generated summaries and onboarding guide.
- A follow-up README edit replaces the `checkpoint-agent 1.2.6` package link with a link to Checkpoint’s `fix/demo-findings` branch at commit `f3d94ae`. This makes the referenced Checkpoint code more specific; the documentation change does not verify or modify the workflow itself.