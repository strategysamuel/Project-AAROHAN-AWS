# AAR-BUILD-003: Authentication, RBAC & Demo User Management Report

**Date:** July 8, 2026  
**Status:** **🟢 AUTHENTICATION & RBAC IMPLEMENTED – READY FOR CORE BANKING MODULES**

---

### Components Added
1.  **Demo Login Screen**: Fully styled login component with single-click Quick Login buttons for:
    - Administrator
    - Executive
    - Relationship Manager
    - Trainer
    - Demo User
2.  **Navigation Sidebar Adaptation**: Dynamic sidebar listing filtered on-the-fly depending on user RBAC permissions list.
3.  **Profile View**: Interactive screen showing details (User Name, Role, Department, Branch, Location) and specific permissions assigned to the profile.

---

### Backend APIs Added/Enhanced
- **`/auth/login`**: Accepts mobile number + password, verifies hashed credentials, and returns access and refresh tokens.
- **`/auth/me`**: Returns the logged-in user profile, department, branch, status, and permissions.
- **`/auth/logout`**: Revokes active JWT refresh sessions.
- **`/auth/token/refresh`**: Generates a new access token from valid refresh credentials.

---

### Database Changes
- Modified `User` entity structure in [services/auth-service/app/models.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/auth-service/app/models.py) to incorporate new columns:
  - `username` (unique identifier)
  - `department`
  - `branch`
  - `avatar`
  - `status`
- Redesigned `seed_database()` in [services/auth-service/app/database.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/auth-service/app/database.py) to seed all 8 target roles:
  - Administrator
  - Relationship Manager
  - Credit Manager
  - Operations Officer
  - Executive
  - Auditor
  - Trainer
  - Demo User
- Encrypted password values using bcrypt before storing them.

---

### Roles & Permissions Matrix
The RBAC permission matrix maps out modules allowed per role:
- **ADMINISTRATOR**: Full access to all 16 modules.
- **RELATIONSHIP_MANAGER**: Access to Dashboard, Customer Management, CKYC, GST, Account Aggregator, EPFO, MCA, Financial Health Card, Reports.
- **CREDIT_MANAGER**: Access to Dashboard, Customer Management, Financial Health Card, Credit Engine, CAM, Reports.
- **OPERATIONS_OFFICER**: Access to Dashboard, Customer Management, OCEN, Reports.
- **EXECUTIVE**: Access to Dashboard, Reports.
- **AUDITOR**: Access to Dashboard, Reports.
- **TRAINER**: Access to Dashboard, Customer Management, Simulation Engine, Reports.
- **DEMO_USER**: Access to Dashboard, Customer Management, Reports.

---

### Security Features
- Password hashing with bcrypt.
- JWT Access token and SQLite stateful session validation.
- Adapted routing that handles route authorization strictly client-side and endpoint protection server-side.
