---
type: concept
domain: software engineering
created: 2026-10-03
---
## Summary

The software delivery lifecycle moves a change from source code to user-visible behavior while reducing a different kind of uncertainty at each boundary. Build changes source into an artifact, deployment changes an environment's running version, and release changes which users receive the behavior.

## Explanation

The lifecycle can be understood as a sequence of state changes:

```text
Source code
    ↓ build and validate
Immutable artifact
    ↓ deploy
Running software in an environment
    ↓ release
Behavior available to intended users
```

Each boundary answers a different question:

| Boundary                        | State that changes | Evidence it provides                                            |                                                                      |
| ------------------------------- | ------------------ | --------------------------------------------------------------- | -------------------------------------------------------------------- |
| [[Software build process]]      | Build              | Source and build inputs become a versioned artifact             | The change can be packaged and passes automated validation           |
| [[Software deployment process]] | Deploy             | A target environment runs a selected artifact and configuration | The version can start, become ready, and operate in that environment |
| [[Software release process]]    | Release            | User exposure changes                                           | The behavior can be introduced to the intended audience and observed |

[[Continuous integration]] validates small changes against the shared codebase. Continuous delivery keeps validated changes ready for production but may retain a manual production gate. [[Continuous deployment]] removes that gate and automatically deploys every passing change to production. These practices automate movement through the lifecycle; they do not collapse its state boundaries.

A Git branch is a source-control history, not a runtime environment. Teams may connect branches to environments as a workflow choice, but an artifact is deployed to an environment rather than to a branch.

The same immutable artifact should normally be promoted through [[Software deployment environments|environments]]. Rebuilding for each environment weakens the evidence gathered earlier because the artifact itself may change. Environment-specific configuration, secrets, permissions, data, and infrastructure can vary without changing the artifact.

Deployment and release can also remain independent. A new version may run in production with a [[Feature Flags|feature flag]] disabled, then be released gradually without another deployment. Disabling the flag reverses user exposure; deploying a known-good artifact changes the running application version. Neither action automatically reverses database or external-system state.

## Example

A checkout change is integrated into the main branch. CI validates it and build automation produces Docker image `checkout:2.0`. The same image is deployed to test and staging, then promoted to production after its readiness checks pass. Its feature remains disabled until the team releases it to employees, then 10% of customers, and finally everyone.

## Connections

- Transforms source through: [[Software build process]], [[Software build automation]]
- Validates integrated changes through: [[Continuous integration]]
- Runs artifacts in: [[Software deployment environments]]
- Changes runtime state through: [[Software deployment process]]
- Can automate production deployment through: [[Continuous deployment]]
- Changes user exposure through: [[Software release process]], [[Feature Flags]]
