# Infrastructure as Code & Deployment Automation (infrastructure/)

This directory houses infrastructure configuration files and automated build templates for Project AAROHAN.

## Directory Structure

1. **terraform/**
   * *Purpose:* Declarative configuration files managing landing zones, IAM roles, databases, pub/sub queues, and networking.
   * *Owner:* DevSecOps & Platform Engineers.
   * *Conventions:* Uses remote state storage on GCS buckets. Resources are structured into reusable modules (`modules/`) and environment configurations (`environments/dev/`, `environments/prod/`).

2. **cloudbuild/**
   * *Purpose:* Cloud Build YAML files defining triggers, security scans, unit testing steps, container builds, and Cloud Deploy actions.
   * *Owner:* DevSecOps.
   * *Conventions:* Secrets must be loaded from Secret Manager; credentials are never hardcoded in triggers.
