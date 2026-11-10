## Overview

PR #1 adds a regression test for `/health` requests that guards against opening plant storage. It exists to catch a health-check path that depends on `load_plants`, while confirming that the request returns status `204` and ends the response headers.

## Changes by Area

- **Health-check regression coverage — `tests/test_health.py`**
  - Adds `HealthTests.test_health_does_not_open_plant_storage`.
  - The test constructs a `sprout.server.Handler` instance with `Handler.__new__(Handler)`, sets its path to `/health`, and replaces `send_response` and `end_headers` with mocks.
  - It patches `sprout.server.load_plants` to raise an `AssertionError` if called, then invokes `handler.do_GET()`.
  - It asserts that `send_response` is called once with `204` and that `end_headers` is called once with no arguments.
  - The test does not change production code. Its failure condition is specifically a call to `load_plants` during this request.

## Commit Walkthrough

1. **`bbfb7610` — `test: guard storage-free health checks`**
   - Adds the regression test in `tests/test_health.py`.
   - The test makes storage access observable by replacing `load_plants` with a function that raises, then checks the expected response calls for `/health`.
   - This is the only commit listed for the PR, so there are no later commits to describe.

## Architectural Impact

- **Confirmed:** The diff adds test coverage only. It does not modify `Handler`, `Handler.do_GET`, `load_plants`, or any production interface.
- **Confirmed:** The test treats a call to `sprout.server.load_plants` during the `/health` request as a failure. It also checks that the handler sends status `204` and calls `end_headers`.
- **Likely:** This guard helps keep health checks usable when plant storage cannot be opened, provided the test’s storage-loading function is the relevant access path.
- **Likely:** The test documents a separation expectation: responding to `/health` should not require loading plant data. The diff adds no runtime mechanism to enforce that expectation; enforcement comes from the regression test being run.
- The test uses a handler created without its initializer. This keeps setup focused on the request path and mocked response methods, but means the test does not cover behavior that might depend on attributes normally set during initialization.

## Review Notes

- Confirm that `Handler.do_GET()` routes `/health` through the behavior this test is intended to protect. The test calls `do_GET()` directly, so it does not exercise HTTP server dispatch or a live server.
- Check that `sprout.server.load_plants` is the storage-loading boundary relevant to health checks. The test detects calls to this patched name; it will not detect other storage access paths.
- Consider whether constructing the handler with `Handler.__new__(Handler)` is sufficient for the `/health` branch. It deliberately bypasses normal initialization, so the test will expose missing attributes used by that branch, but it does not validate initialization itself.
- Review the response assertions against the intended contract: the test checks a single `204` response and one `end_headers()` call. It does not assert response headers, response body, or behavior for other request paths.
- Run the test with the project’s usual test command and verify that the patch target resolves to the function used by `Handler.do_GET()`. If the handler’s storage access is later routed through a different name or module, this guard may need updating.
- The main risk is limited test coverage rather than a production behavior change: no implementation is changed by this PR, and the regression test protects only the specific storage call and response behavior it asserts.

## Priority Rating

LOW — The PR adds a focused regression test and makes no production changes. It provides useful protection against `/health` calling `load_plants`, but does not broaden coverage to other storage paths or exercise a live HTTP request.