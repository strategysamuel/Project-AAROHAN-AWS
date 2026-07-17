# AAR-HOTFIX-004: Gateway Verification Report

## Route Verification Summary

| Route | Backend Service | Port | Status | Fix Applied |
|---|---|---:|---|---|
| `/auth/*` | auth-service | 9000 | Verified | Updated gateway mapping to documented auth port |
| `/customers/*` | onboarding-service | 9001 | Verified | Updated gateway mapping to documented onboarding port |
| `/ckyc/*` | ckyc-service | 9011 | Verified | Updated gateway mapping to documented CKYC port |
| `/gst/*` | gst-service | 9003 | Verified | Retained GST fix from prior hotfix; confirmed correct upstream |
| `/aa/*` | aa-service | 9004 | Verified | Confirmed upstream mapping |
| `/epfo/*` | epfo-service | 9013 | Verified | Updated gateway mapping to documented EPFO port |
| `/mca/*` | mca-service | 9012 | Verified | Updated gateway mapping to documented MCA port |
| `/fhc/*` | fhc-service | 9005 | Verified | Updated gateway mapping to documented FHC port |
| `/credit/*` | credit-engine | 9006 | Verified | Added missing gateway route |
| `/cam/*` | cam-service | 9007 | Verified | Confirmed upstream mapping |
| `/exec/*` | exec-service | 9009 | Verified | Confirmed upstream mapping |

## Root Cause

The shared gateway router did not match the documented backend port inventory. Some prefixes were mapped to the wrong upstream ports, and `/credit/*` was missing entirely. This caused route-level 404s even though the backend services themselves were healthy.

## Files Changed

- [app/main.py](app/main.py)

## Final Verification

- Gateway route resolution check passed for all requested prefixes.
- `pytest tests/test_regression_e2e.py -q` passed.
- `npm --prefix apps/customer-portal run build` passed.

## Final Status

All requested frontend API routes are now mapped to the correct backend services, and no route returns 404 because of incorrect gateway routing.