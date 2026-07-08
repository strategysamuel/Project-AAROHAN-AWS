# Testing & Quality Assurance (tests/)

This directory houses global integration, performance, security, and End-to-End (E2E) testing configurations.

## Directory Structure

1. **integration/**: Integration tests validating database and internal API calls.
2. **contract/**: Schema checks validating API formats across gateways.
3. **security/**: Penetration testing scripts, vulnerability checks, and container image scans.
4. **performance/**: Load test scripts (e.g., K6, Locust templates) verifying endpoint latency.
5. **e2e/**: End-to-end user journey tests (e.g., Cypress, Playwright configurations).

---

## Test Execution Guidelines
* Run local integration tests:
  ```bash
  npm run test:integration
  ```
* Run local API contract checks:
  ```bash
  npm run test:contract
  ```
