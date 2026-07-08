# Shared Packages (packages/)

This directory houses libraries, utility packages, and components shared across applications and microservices.

## Package Inventory

1. **common-types/**
   * *Purpose:* Unified TypeScript interfaces, API request/response schemas, and canonical entity definitions.
   * *Owner:* Platform Services Group (PSG).
   * *Usage:* Linked during compilation by frontend applications and backend Node.js microservices.

2. **ui-components/**
   * *Purpose:* Shared component library (buttons, card layout grids, filters, navigation bars) conforming to Google Material Design 3 and WCAG 2.1 accessibility targets.
   * *Owner:* Digital Experience Squad (DXS).
   * *Usage:* Imported directly by apps under `/apps`.

3. **mcp-core/**
   * *Purpose:* Shared Python/TypeScript library implementing the Model Context Protocol (MCP) to connect AI agents with database structures.
   * *Owner:* Data & AI Squad (DAIS).
   * *Usage:* Imported by AI services (e.g., `agent-coach-service`).

4. **prompt-registry/**
   * *Purpose:* Versioned prompt templates (YAML configurations) for Gemini operations (e.g., CAM compiler, client outreach emails).
   * *Owner:* DAIS.
   * *Usage:* Loaded as configuration assets at runtime by AI service instances.
