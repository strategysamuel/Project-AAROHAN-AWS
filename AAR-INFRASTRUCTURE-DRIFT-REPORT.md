# AAR-INFRASTRUCTURE-DRIFT-REPORT

This report identifies every difference between the updated repository configuration and the live AWS deployment.

## ECS Services
**Live Services:** 3
- `arn:aws:ecs:ap-south-1:905417996641:service/aarohan-hackathon-cluster/aarohan-platform-IdentityService-nT8rlUCM4Eff`
- `arn:aws:ecs:ap-south-1:905417996641:service/aarohan-hackathon-cluster/aarohan-platform-LendingService-U9S3O9hdumuS`
- `arn:aws:ecs:ap-south-1:905417996641:service/aarohan-hackathon-cluster/aarohan-platform-ExecutiveService-QHDeXHct5oCZ`

## Task Definitions
### Service: `aarohan-platform-IdentityService-nT8rlUCM4Eff`
**Live Family:** `identity-task-definition`
**Live Revision:** `1`
**Live Exposed Ports:** [9000]
### Service: `aarohan-platform-LendingService-U9S3O9hdumuS`
**Live Family:** `lending-task-definition`
**Live Revision:** `1`
**Live Exposed Ports:** [9001, 9003, 9004, 9005, 9006, 9007, 9011, 9012, 9013]
### Service: `aarohan-platform-ExecutiveService-QHDeXHct5oCZ`
**Live Family:** `executive-task-definition`
**Live Revision:** `1`
**Live Exposed Ports:** [9009]

## Target Groups
**Live Target Groups:** 3
- `aarohan-executive-tg`
- `aarohan-identity-tg`
- `aarohan-lending-tg`
**DRIFT IDENTIFIED:** `aarohan-rbi-tg` is missing in live environment.

## Listener Rules
**Live Path Rules:**
- `/auth/*`
- `/api/*`
- `/exec/*`
**DRIFT IDENTIFIED:** Listener rule for `/rbi/*` is missing in live environment.

## Conclusion & Deployment Action
Drift exists between the updated repository and the live environment for the `lending-intelligence` ECS service, missing port mappings for 9002, 9008, and 9014. Additionally, the CloudFormation stack is missing the `aarohan-rbi-tg` target group and corresponding listener rule. We will deploy these missing infrastructure changes immediately.
