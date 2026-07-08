# Platform Integrations & Configurations (platform/)

This directory houses SQL schemas, database migration files, API gateway proxy bundles, and analytical dashboard configurations.

## Directory Structure

1. **database/**
   * *Purpose:* AlloyDB operational schemas, transactional table rules, row-level security (RLS) policies, and database migration logs.
   * *Owner:* Platform Services Group (PSG).
   * *Integration:* Synchronized with AlloyDB instances.

2. **analytics/**
   * *Purpose:* BigQuery table definitions, ingestion schemas (GSTN, AA CDC streams), Vertex AI Feature Store variables, and Looker dashboard configuration files.
   * *Owner:* Data & AI Squad (DAIS).

3. **apigee/**
   * *Purpose:* Apigee proxy configuration bundles, security policies (JWT checks, signature validation), and rate limiting rules.
   * *Owner:* Integration Squad (IS).
   * *Target:* Deployed directly to Apigee gateway environments.
