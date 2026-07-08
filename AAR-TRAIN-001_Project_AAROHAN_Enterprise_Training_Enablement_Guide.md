# AAR-TRAIN-001: Enterprise Training & Enablement Guide

---

## 1. Cover Page

* **Project Name**: Project AAROHAN (Enterprise MSME Underwriting & Embedded Credit Platform)
* **Version**: v1.0.0
* **Document Version**: v1.0.0
* **Classification**: BANK INTERNAL - TRAINING MANUAL
* **Owner**: Enterprise Learning & Development Division
* **Approval Matrix**:
  - Banking Training Manager: APPROVED
  - Learning & Development Lead: APPROVED
  - Google Cloud Customer Success Architect: APPROVED

---

## 2. Executive Summary

This Enterprise Training & Enablement Guide provides learning paths, certification frameworks, and hands-on exercises to prepare all user groups for the rollout of Project AAROHAN v1.0.0.

---

## 3. Training Objectives

* Accelerate user adoption of the AAROHAN portal across branch networks.
* Enable Relationship Managers and Credit Officers to perform paperless MSME onboarding and underwriting.
* Train SRE and Platform Operations teams to support and maintain the platform.

---

## 4. Scope

This guide covers training structures, curriculums, assessment methods, FAQs, and enablement schedules for all technical and business users of Project AAROHAN.

---

## 5. Training Strategy

Training uses a blended learning model:
* **Self-paced E-Learning**: Interactive portal walkthrough modules.
* **Instructor-Led Training (ILT)**: Deep-dive webinars for Credit Officers.
* **Sandbox Simulations**: Guided practical exercises in testing environments.

---

## 6. Target Audience

Learning paths are customized by role:
* **Relationship Managers (RMs)**: Focus on onboarding, document verification, next-best-action, and checklist management.
* **Credit Officers**: Focus on financial analysis, AI decisions override, and editing CAM drafts.
* **Branch Managers & Credit Approvers**: Focus on CAM approval and PDF exporting.
* **Regional Managers & Business Executives**: Focus on performance dashboard trends.
* **Operations & IT Support Teams**: Focus on Active Directory provisioning and ticket resolutions.
* **Platform Administrators, SREs & DevOps**: Focus on secret rotation, database recovery (PITR), and scaling configurations.

---

## 7. Training Curriculum

* **Platform Overview**: System dashboard components and navigation.
* **MSME Onboarding**: Registrations, file uploads, and CKYC checks.
* **DPI Integrations**: Consents tracking, GST analysis, AA bank statements mapping, MCA registers, EPFO payroll, and TReDS discounts.
* **Credit Decisioning**: Understanding FHC scores, explainable AI parameters, manual overrides, and CAM reviews.
* **Workspace & Alerts**: Managing task workflows, calendar dates, and early warning watchlists.
* **OCEN Embedded lending**: Credit eligibility rules, offer discoveries, and digital disbursals.

---

## 8. Role-Based Training Matrix

| Training Module | RMs | Credit Officers | Branch Managers | SRE / DevOps |
| :--- | :---: | :---: | :---: | :---: |
| **Login & Access** | Yes | Yes | Yes | Yes |
| **Borrower Onboarding** | Yes | No | No | No |
| **Override AI Decisions** | No | Yes | No | No |
| **Approve CAM drafts** | No | No | Yes | No |
| **PITR & DR Failover** | No | No | No | Yes |

---

## 9. Learning Paths

Learning paths consist of:
1. **Module 1**: Basics of DPI and Consent Lending (All users - 1 Hour).
2. **Module 2**: Portal Operations & Workspaces (RMs and Credit Officers - 2 Hours).
3. **Module 3**: Credit Approvals & CAM overrides (Approvers - 1.5 Hours).
4. **Module 4**: SRE Operations & DB Management (SRE and DevOps - 4 Hours).

---

## 10. Hands-on Exercises

* **Exercise 1**: Create a new customer profile and run a CKYC check.
* **Exercise 2**: Generate and edit an AI CAM draft for a test borrower.
* **Exercise 3**: Trigger a mock database recovery from a backup snapshot (SREs).

---

## 11. Practical Scenarios

* **Scenario A**: The borrower's AA statement link fails. *Action*: Verify that the customer has accepted the consent request, then resend the AA link notification.

---

## 12. Assessment & Certification

Users must pass a 20-question multiple-choice evaluation and complete a simulated loan workflow in UAT to receive certification.

---

## 13. Knowledge Evaluation

The quiz checks familiarity with RBAC permissions, audit trail logging, and AI explainability parameters.

---

## 14. Frequently Asked Questions

* **Q: How long is a customer consent active?**
  - *A*: Consent duration is defined during creation, typically active for 12 months unless revoked by the user.

---

## 15. Training Schedule

* **Week 1**: Train the Trainer (Core leads).
* **Week 2**: RM and Credit Officer onboarding workshops (Region 1).
* **Week 3**: RM and Credit Officer onboarding workshops (Region 2).
* **Week 4**: DevOps and SRE dry-run drills.

---

## 16. Change Management & User Adoption Strategy

Identify system champions in each branch to assist team members. Provide visible progress trackers on executive portals to encourage adoption.

---

## 17. Post-Go-Live Support

Dedicated MSME-Support Slack channels and daily office hours are available during the first 30 days post-launch.

---

## 18. Success Metrics

* **Adoption Rate**: Target 90% of RMs active in the portal within 30 days.
* **Average Ticket Resolution Time**: Target < 15 minutes for L1 operations.
* **First-Time Match Rate**: Target > 95% success rate on CKYC lookups.

---

## 19. Appendix

* Registration link to the training sandbox.
* Certification exam sample question bank.
