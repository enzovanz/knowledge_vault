---
type: concept
domain: software engineering
created: 2026-09-14
aliases:
  - Deployment environments
  - Software environments
---
## Summary

A software deployment environment is the complete context in which an application version runs: its infrastructure, configuration, secrets, data, permissions, integrations, and traffic. Teams use separate environments to obtain different kinds of feedback while limiting the impact of failures.

## Explanation

Infrastructure is one part of an environment. It includes resources such as compute, networking, storage, databases, queues, and service identities. The environment also includes the artifact version and the runtime state surrounding those resources.

Common environments optimize for different goals:

| Environment | Primary goal | Common limitation |
| --- | --- | --- |
| **Development** | Fast changes and debugging on a local or shared system | Often differs substantially from production |
| **Preview** | Isolated review of one branch or pull request | Temporary and potentially expensive at scale |
| **Test** | Repeatable automated or manual validation | Often uses controlled data and mocked dependencies |
| **Staging** | Final validation with production-like configuration and services | Cannot reproduce production traffic, scale, data, or integrations perfectly |
| **Production** | Reliable service for real users and data | Failures have the largest impact |

A CI runner is usually a temporary execution environment for pipeline jobs, not the development environment. It may run tests directly or deploy an artifact into a separate test environment.

An environment is also not a Git branch. A branch records source history; the [[Software deployment process]] installs an artifact into a runtime environment. A team may map branches to environments, but that mapping is a workflow convention.

### Promotion, parity, and drift

**Promotion** advances a known artifact from one environment to another, either through approval or automation. The same immutable artifact should normally move through test, staging, and production instead of being rebuilt. Configuration and infrastructure capacity may change by environment while the artifact remains identical.

**Environment parity** means keeping behavior-affecting characteristics similar enough that non-production evidence remains useful. Perfect parity is impractical because production has different credentials, traffic, data, scale, and cost constraints.

**Environment drift** is an unintended difference that accumulates over time, such as production receiving a manual database upgrade while staging keeps the old version. Version pinning, shared infrastructure definitions, automated provisioning, and configuration validation reduce drift.

## Example

A pipeline builds Docker image `app:2.0` once. It deploys the image to a resettable test environment, promotes the same digest to staging with production-like services, and then deploys it to production with different secrets and greater capacity. The artifact remains unchanged throughout.

## Connections

- Part of: [[Software delivery lifecycle]]
- Receives artifacts through: [[Software deployment process]]
- May be traversed automatically by: [[Continuous deployment]]
- Runs artifacts produced by: [[Software build process]]
- Production availability is controlled by: [[Software release process]]
