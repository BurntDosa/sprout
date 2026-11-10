## Commit `8a0fe7f` — 2026-11-10

## Context
The README described the demo as using `checkpoint-agent 1.2.6`, while the commit message says the change is to use a fixed Checkpoint workflow. The update replaces the package-version reference with a link to a specific Checkpoint commit, likely to make the demo’s Checkpoint version explicit and reproducible.

## Changes
- `README.md`: The opening project description now links to Checkpoint’s `fix/demo-findings` branch at commit `f3d94ae` instead of linking to the `checkpoint-agent 1.2.6` package page. The following description of generated documents in `checkpoints/`, `catchups/`, and `MASTER_CONTEXT.md` is unchanged.

## Impact
- Confirmed: README readers are directed to the specified Checkpoint commit rather than the PyPI release page.
- Likely: The README now better reflects the Checkpoint code used for the demo, though this diff does not change or verify the GitHub Actions workflow itself.

## Priority Rating
LOW — This is a documentation link and version-reference change; it does not modify application or workflow code.
