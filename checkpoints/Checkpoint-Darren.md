## Commit `f5b09a2` — 2026-11-10

## Context
The reminder tests already cover collections containing plants with different watering schedules. The commit adds coverage for the empty-collection case, checking that there are no reminders when there are no plants to evaluate.

## Changes
- `tests/test_reminders.py`: Adds `ReminderTests.test_empty_collection_has_no_reminders`. It calls `due_plants` with an empty list, a fixed date, and a seven-day watering interval, then asserts the result is an empty list.

## Impact
- Confirmed: The test will fail if `due_plants` returns anything other than `[]` for an empty plant collection.
- Likely: This guards against regressions in reminder generation for users with no plants, without changing reminder behavior or production code.

## Priority Rating
LOW — This is a focused test-only change that covers an edge case without modifying application behavior.
