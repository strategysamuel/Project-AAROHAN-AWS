# Operational & Automation Scripts (scripts/)

This directory houses helper scripts used to automate development tasks and deployment operations.

## Script Catalog

* **bootstrap.sh / bootstrap.ps1**: Environment initialization scripts for developer machines.
* **deploy-check.sh**: Pre-deployment validation scripts verifying security configurations and access keys.
* **db-seed.js / db-seed.py**: Scripts to seed development databases with mock persona records.

## Usage Conventions
* All scripts must be documented with clear parameter descriptions.
* Do not hardcode access tokens or credentials inside script files.
