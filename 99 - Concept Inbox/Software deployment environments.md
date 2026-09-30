---
type: concept
domain: software engineering
created: 2026-09-14
aliases:
  - Deployment environments
  - Software environments
---
## Summary

A software deployment environment is an isolated context in which a version of an application runs with its own infrastructure, configuration, data, and access rules. Teams use multiple environments to validate changes with increasing realism before or while making them available to users.

## Explanation

Common environments include:

- **Development:** used by engineers for rapid local or shared experimentation
- **Test:** used for automated or manual validation in controlled conditions
- **Staging:** resembles production and is used for final integration and release checks
- **Production:** serves real users and requires the strongest reliability and security controls

Some teams also create temporary preview environments for individual pull requests. Environment names and boundaries vary: a small system may have only development and production, while a larger system may use several testing, pre-production, regional, or customer-specific environments.

An environment is not a stage of the [[Software build process|build process]]. The build produces an artifact; the [[Software deployment process|deployment process]] installs and runs that artifact in an environment. Ideally, the same immutable artifact is promoted through environments instead of being rebuilt for each one. Configuration, secrets, infrastructure capacity, external services, and data can differ by environment.

Environments support the software delivery lifecycle by limiting risk:

```text
Source change
    ↓ build and validate
Versioned artifact
    ↓ deploy
Test or staging environment
    ↓ promote the same artifact
Production environment
    ↓ release
Available to intended users
```

**Promotion** means approving or automatically advancing a known artifact from one environment to the next. It is a lifecycle decision; it does not necessarily mean rebuilding the software.

Environment parity reduces surprises by keeping non-production environments similar to production. Perfect parity is rarely practical, so teams must understand differences such as data volume, permissions, integrations, and infrastructure scale.

## Example

A pipeline builds Docker image `app:2.0` once. It deploys that image to a test environment for automated checks, promotes the same image to staging for final validation, and then deploys it to production. Production uses different secrets and more infrastructure, but the application artifact remains unchanged. The feature is released later through a feature flag.

## Connections

- Receives artifacts through: [[Software deployment process]]
- May be traversed automatically by: [[Continuous deployment]]
- Runs artifacts produced by: [[Software build process]]
- Production availability is controlled by: [[Software release process]]
- Sources:
