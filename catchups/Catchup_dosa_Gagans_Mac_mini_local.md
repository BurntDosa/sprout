# While You Were Gone — Since November 10, 2026

The available checkpoints cover two commits dated November 10, 2026. They update the README to present Sprout as a Checkpoint demo and change which generated-document paths Git ignores. Neither commit changes application behavior, functions, or classes.

## Refactors & Structural Changes

- The README now leads with Sprout’s role as a public Checkpoint demo using `checkpoint-agent 1.2.6`. It describes the generated files in `checkpoints/`, `catchups/`, and `MASTER_CONTEXT.md`, and says the October 2026 commits are fictional while the generated documents come from live Checkpoint runs.
- The README replaces detailed project background, setup, API, health-check, test, and upgrade notes with a shorter overview. Basic installation, test, server, and upgrade instructions remain.

## New Dependencies & Config Changes

- `.gitignore` no longer excludes `checkpoints/`, `catchups/`, or `MASTER_CONTEXT.md`. Git can now notice files at those paths, so you can review and commit them normally. Removing the rules does **not** automatically add existing files to version control.
- Ignore rules for Python cache files, `.venv/`, and `.env` remain unchanged.
- No dependency or environment-variable changes are recorded.