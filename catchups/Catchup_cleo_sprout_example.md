# While You Were Gone — Since November 10, 2026

The available checkpoints record two low-priority updates dated November 10, 2026. Neither changes application behavior, APIs, dependencies, or the GitHub Actions workflow; the main practical change is that Git can now track generated Checkpoint documents.

## Critical Changes (Must-Read)

- `.gitignore` no longer excludes `checkpoints/`, `catchups/`, or `MASTER_CONTEXT.md`. Git can now notice files in those locations, so you can review and commit generated documents through normal Git changes. Removing the ignore rules does **not** automatically add existing files to version control.
- No breaking changes or API changes are recorded. The remaining ignore rules still cover Python cache files, `.venv/`, and `.env`.

## New Features & Additions

- Generated documents under `checkpoints/` and `catchups/`, along with `MASTER_CONTEXT.md`, can now be tracked in Git. This enables sharing them through commits; it does not change how they are generated.
- The README now links to Checkpoint’s `fix/demo-findings` branch at commit `f3d94ae` instead of the `checkpoint-agent 1.2.6` package page. Its description of the generated documents is unchanged. This makes the README’s Checkpoint reference explicit, but the change does not verify or alter the workflow.