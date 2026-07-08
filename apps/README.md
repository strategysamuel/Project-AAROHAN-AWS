# Applications (apps/)

This directory houses user-facing frontend applications for Project AAROHAN.

## Application Inventory

1. **customer-portal/**
   * *Purpose:* Self-service portal for MSME owners to register, upload financials, check limits, and execute drawdowns.
   * *Owner:* Digital Experience Squad (DXS).
   * *Coding Standards:* TypeScript, React, TailwindCSS, Material Design 3.
   * *Deployment Target:* Firebase Hosting / Cloud Run.

2. **employee-workspace/**
   * *Purpose:* Workspaces for Relationship Managers (sales funnel management), Credit Analysts (balance sheet spreading & rules checklist), Credit Committee members (consensus voting), and Risk Management (EWS console).
   * *Owner:* DXS & CET.
   * *Coding Standards:* TypeScript, React, Material Design 3.
   * *Deployment Target:* Cloud Run.

3. **admin-console/**
   * *Purpose:* Administrative interface to adjust policy parameters, fee calculations, interest margins, and manage user roles.
   * *Owner:* Platform Services Group (PSG).
   * *Coding Standards:* TypeScript, React, Material Design 3.
   * *Deployment Target:* Cloud Run.

---

## Build and Run Guidelines

*   **Development Server:**
    ```bash
    npm run dev --filter <app-name>
    ```
*   **Production Build Compilation:**
    ```bash
    npm run build --filter <app-name>
    ```
