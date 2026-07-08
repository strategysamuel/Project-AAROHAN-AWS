# AAR-V11-SPRINT-001: Project AAROHAN Sprint 1 Planning

---

## 1. Executive Summary

This document specifies the Sprint 1 Planning targets for Project AAROHAN Version 1.1. It sets capacity plans, selected user stories, and task breakdowns for the first two-week iteration.

---

## 2. Sprint Goal

Deliver the highest-priority business capabilities from Version 1.1 while maintaining production stability.

---

## 3. Sprint Scope

Sprint 1 targets the platform security automation and base technical debt features:
* **US-11-201**: Trigger Secret Manager Cron Rotation.
* **US-11-701**: Migrate auxiliary services to Pydantic v2.

---

## 4. Sprint Capacity Planning

* **Product Owner**: 1 (100% capacity).
* **Scrum Master**: 1 (100% capacity).
* **Backend Developers**: 2 (Total: 80 Hours).
* **Frontend Developers**: 1 (Total: 40 Hours).
* **AI Engineers**: 1 (Total: 40 Hours).
* **QA Engineers**: 1 (Total: 40 Hours).
* **DevOps Engineers**: 1 (Total: 40 Hours).
* **Target Velocity**: 6 Story Points.

---

## 5. Selected User Stories

### Story ID: US-11-201
* **Title**: Trigger Secret Manager Cron Rotation
* **Story Points**: 3
* **Priority**: Critical (Must Have)
* **Acceptance Criteria**:
  - *Given*: The Scheduler cron fires at midnight.
  - *When*: The script executes in Secret Manager.
  - *Then*: A new secret version is created, and services reload settings without downtime.
* **Dependencies**: Secret Manager configuration.

### Story ID: US-11-701
* **Title**: Migrate auxiliary services to Pydantic v2
* **Story Points**: 3
* **Priority**: High (Must Have)
* **Acceptance Criteria**:
  - *Given*: Auxiliary services (CKYC, MCA, EPFO) schemas configuration.
  - *When*: Python runtime environment executes builds.
  - *Then*: Code compiles cleanly without Pydantic deprecation warnings.
* **Dependencies**: None.

---

## 6. Sprint Backlog

Total selected points: **6 Story Points** (aligned with capacity).

---

## 7. Task Breakdown

### Tasks for US-11-201
* **Task 1.1**: Draft rotation script in python. (2h)
* **Task 1.2**: Deploy Cloud Scheduler test trigger. (2h)
* **Task 1.3**: Configure Cloud Run to hot-reload environment values. (4h)

### Tasks for US-11-701
* **Task 2.1**: Update `schemas.py` in `ckyc-service` to use Pydantic V2. (3h)
* **Task 2.2**: Update `schemas.py` in `mca-service` and `epfo-service`. (5h)
* **Task 2.3**: Execute validation regression tests. (4h)

---

## 8. Definition of Ready (DoR)

Stories must be estimated in Fibonacci points, have clear acceptance criteria, and resolve external blockers.

---

## 9. Definition of Done (DoD)

All tasks completed, code committed, unit tests passed, code reviewed by another developer, and successfully deployed to staging.

---

## 10. Sprint Risks

* **Risk**: Service disruption during rolling container restarts post secret rotation.
* **Mitigation**: Perform test rotations in staging environments before running scheduled production crons.

---

## 11. Sprint Assumptions

* Staging and UAT environments remain available throughout the sprint.
* The team has access to Google Cloud Secret Manager APIs.

---

## 12. Sprint KPIs

* **Velocity**: Target 6 points.
* **Story Completion**: 100% completion of selected stories.
* **Defect Leakage**: Zero high/critical defects leak to UAT.
* **Code Coverage**: Maintain >= 80% coverage on new code.
* **Build Success Rate**: 100% success on main branch CI pipelines.

---

## 13. Sprint Review Plan

Demonstrate automatic secret rotation logs and warning-free service compilation results on the final day of the sprint.

---

## 14. Sprint Retrospective Plan

Examine SRE performance metrics and developer workflows on the final day of the sprint to identify process improvements.

---

## 15. Deliverables

* Updated `Secret Manager` rotation cron triggers.
* Pydantic V2 compliant services in staging.

---

## 16. Approval Matrix

* **CPO**: APPROVED
* **Scrum Master**: APPROVED
* **Technical Lead**: APPROVED

---

## 17. Appendix

* Sprint Board Link.
* Daily Standup schedule (09:45 IST).
