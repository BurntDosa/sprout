## Overview

This PR adds a regression test for the `/health` endpoint in `tests/test_health.py`. It verifies that the endpoint returns `204` without calling `sprout.server.load_plants`, guarding against health checks becoming dependent on plant storage being available.

## Changes by Area

- **Health-check regression coverage — `tests/test_health.py`**
  - Adds `HealthTests.test_health_does_not_open_plant_storage`.
  - The test creates a `sprout.server.Handler` instance with `Handler.__new__`, sets its path to `/health`, and mocks `send_response` and `end_headers`.
  - It patches `sprout.server.load_plants` to raise an `AssertionError` if called, then invokes `handler.do_GET()`.
  - It asserts that the handler sends status `204` and calls `end_headers()` once. Together, these checks make the expected health-check response explicit and fail the test if the request tries to load plant data.

No production code is changed in the combined diff. The change adds a test around the existing `Handler.do_GET()` behavior rather than modifying that behavior.

## Commit Walkthrough

1. **`bbfb7610` — `test: guard storage-free health checks`**
   - Adds `tests/test_health.py` with a focused regression test. The test treats any call to `load_plants` during `/health` handling as a failure and checks the expected status and response-header completion.

## Architectural Impact

- **Confirmed:** The diff changes the test suite only. It adds no production interfaces, storage operations, request-routing code, or response behavior.
- **Confirmed:** The new test encodes an expectation that handling `/health` does not call `sprout.server.load_plants` and responds with status `204`, followed by `end_headers()`.
- **Likely:** This regression check will help keep the health-check path independent of plant-storage loading as `Handler.do_GET()` evolves. That can make failures in plant storage less likely to affect this particular health response, but the test itself does not change runtime behavior or establish broader availability guarantees.
- **Confirmed scope limitation:** The test exercises `do_GET()` directly on a minimally constructed handler. It does not demonstrate behavior through a live HTTP server, validate response headers beyond the call to `end_headers()`, or cover other paths and request methods.

## Review Notes

- Check that the assertion matches the intended `/health` contract: status `204`, no plant-storage load, and a call to `end_headers()`. If the endpoint’s intended response changes, this test will need to change with it.
- Confirm that patching `sprout.server.load_plants` is the right seam for detecting plant-storage access in `Handler.do_GET()`. The test specifically catches calls through that imported name; it does not detect storage access through a different function or module.
- Review the use of `Handler.__new__(Handler)`. It deliberately bypasses initialization so the test can call `do_GET()` with only the fields and methods it sets up. If `do_GET()` later starts relying on additional initialized state, this test may fail; that could signal a behavior change or require a more complete handler setup.
- Consider the coverage boundary before treating this as an end-to-end health check. The test calls the handler method directly and mocks response methods, so it does not verify socket behavior, HTTP serialization, or integration with server initialization.
- The patched `load_plants` raises immediately if called. That is appropriate for detecting an unwanted dependency, but the test does not check behavior for other storage failures or validate health-check behavior for paths other than `/health`.

## Priority Rating

**LOW** — This is a focused regression test with no production-code changes. It improves coverage of the health-check storage-isolation expectation, but does not alter application behavior or introduce runtime risk.