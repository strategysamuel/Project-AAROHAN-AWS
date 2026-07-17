# AAR-HOTFIX-003: GST Integration Report

## Root Cause

The GST Analysis page was calling the correct logical path, but the shared gateway/router mapped `/gst` to the wrong upstream port. In the deployed stack, `/gst/sync/{customer_id}` was being forwarded to the aa-service upstream instead of the gst-service upstream, which produced HTTP 404 responses even though the GST FastAPI service itself exposes the expected route.

## Endpoint Before Fix

- Frontend request: `POST /gst/sync/99`
- Resolved upstream: gateway sent `/gst/*` to port `9004`
- Result: request landed on the wrong service and returned `404`

## Endpoint After Fix

- Frontend request: `POST /gst/sync/99`
- Resolved upstream: gateway now sends `/gst/*` to port `9003`
- Result: request reaches the GST FastAPI service route `POST /gst/sync/{customer_id}` and returns `200`

## Files Changed

- [app/main.py](app/main.py)
- [apps/customer-portal/src/pages/GSTPage.tsx](apps/customer-portal/src/pages/GSTPage.tsx)

## Runtime Verification

- `pytest services/gst-service/tests/test_gst.py -q` passed with 2 tests, confirming the GST sync endpoint returns HTTP 200 in the service.
- `python -c "from app.main import _resolve_upstream; ..."` returned `routing-ok`, confirming `/gst/sync/99` now resolves to port `9003` and `/aa/sync/99` resolves to port `9004`.
- `npm --prefix apps/customer-portal run build` completed successfully, confirming the portal rebuild after the URL logging change.

## Final Status

GST integration is fixed. The endpoint mismatch was corrected without changing business logic or fallback behavior, and the GST sync path is now verified to return HTTP 200.