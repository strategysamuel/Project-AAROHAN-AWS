# GitHub Actions Workflows (.github/workflows/)

This directory houses automated CI/CD pipeline triggers and configurations.

## Workflow Definitions

* **pr-verification.yml**: Triggered on pull request creations. Runs code checkers, security scans, and unit tests.
* **deploy-dev.yml**: Triggered on merges to the main branch. Builds container images and deploys them to the Dev environment.
* **release-uat.yml**: Deploys release candidates to the UAT environment on tag creation events.
