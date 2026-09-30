---
type: concept
domain: software engineering
created: 2026-09-14
---
## Summary

The software deployment process places a specific software artifact into a target environment and makes it run there. Deployment changes the technical state of an environment, but it does not necessarily make the software or feature available to users.

## Explanation

A deployment process can include:

- Selecting a previously built and tested artifact
- Providing environment-specific configuration and secrets
- Applying infrastructure or database changes
- Starting or updating the application
- Running health checks
- Rolling back when the deployment is unhealthy

Common deployment strategies include rolling deployments, blue-green deployments, and canary deployments. A useful principle is **build once, deploy many**: the same immutable artifact is promoted through testing, staging, and production while environment-specific configuration remains separate.

The process may be started manually or automatically. [[Continuous deployment]] is the practice of automatically running the production deployment process for every change that passes the required validation.

Deployment is different from [[Software release process|release]]. A version may be running in production while its new behavior remains hidden behind a feature flag.

## Example

A CI pipeline builds and tests the Docker image `app:1.8`. The deployment process configures production to run that exact image, waits for its health checks to pass, and keeps the new feature disabled.

## Connections

- Receives artifacts from: [[Software build process]], [[Software build automation]]
- Targets: [[Software deployment environments]]
- Can follow validation by: [[Continuous integration]]
- Can be automated through: [[Continuous deployment]]
- Makes software available for: [[Software release process]]
- Sources:
