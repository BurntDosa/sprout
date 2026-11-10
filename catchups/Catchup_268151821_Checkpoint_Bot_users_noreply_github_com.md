# While You Were Gone — Since November 10, 2026

The changes covered here update the repository’s Checkpoint demo documentation and Git tracking rules. There are no reported application-code, API, or workflow changes, so you don’t need to make a runtime migration.

## Refactors & Structural Changes

The README now presents Sprout as a public Checkpoint demo and points you to the generated documents in `checkpoints/`, `catchups/`, and `MASTER_CONTEXT.md` as entry points. It says the October 2026 commits are fictional and the generated documents come from live Checkpoint runs. The README still includes installation, test, server, and upgrade instructions, but in shorter form than before.

The Checkpoint reference in the README now links to commit `f3d94ae` on the `fix/demo-findings` branch instead of the `checkpoint-agent 1.2.6` package page. This updates the documentation’s reference; the changes do not verify or modify a GitHub Actions workflow.

## New Dependencies & Config Changes

`.gitignore` no longer excludes `checkpoints/`, `catchups/`, or `MASTER_CONTEXT.md`. Git can now detect files at those paths so you can review and commit them. Removing the ignore rules does **not** automatically add existing files to version control.

The remaining ignore rules still cover Python cache files, `.venv/`, and `.env`. No dependencies, environment variables, or application configuration keys changed.