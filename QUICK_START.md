# Quick Start

This guide is for hackathon judges and reviewers who want the shortest path to a working demo.

## 1. Install

```bash
npm install
npm run build
```

Start the auth service and ESE control plane in separate terminals when running the full demo locally.

## 2. Run

Portal:

```bash
npm --prefix apps/customer-portal run dev
```

Auth service:

```powershell
Set-Location services/auth-service
poetry run python -m uvicorn app.main:app --host 127.0.0.1 --port 9000
```

ESE control plane:

```powershell
Set-Location services/ese-admin-service
$env:PYTHONPATH='D:\SAMUEL\HACK 2 SKILL\IDBI MSME\Project AAROHAN\services\ese-core;D:\SAMUEL\HACK 2 SKILL\IDBI MSME\Project AAROHAN\services\ese-admin-service'
poetry run python -m uvicorn app.main:app --host 127.0.0.1 --port 8090
```

## 3. Demo Login

Use the Relationship Manager account for the main walkthrough:

- Mobile number: 9876543210
- Password: AarohanPass123!

## 4. Select a Persona

Open Demo Studio after login and choose a curated persona such as Priya Textile Works, GreenAgro Cooperative, or QuickLogistics.

## 5. Generate CAM

Walk through the lending journey until the CAM view is available, then open the CAM panel or download the memo.

## 6. View Dashboard

Finish by opening the Executive Dashboard to review KPIs, risk indicators, and portfolio status.

## 7. Screenshot Prompts

If you are preparing a public submission, capture:

- Login screen
- Demo Studio persona selection
- Financial Health Card
- CAM view
- Executive dashboard

## Notes

- The demo is designed to be deterministic.
- If the portal shows a control-plane fetch warning, make sure the ESE admin service is running on port 8090.
