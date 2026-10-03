---
type: concept
domain: software engineering
created: 2026-09-14
---
## Summary

The software deployment process places a specific software artifact into a target environment and makes it run there. Deployment changes the technical state of an environment, but it does not necessarily make the software or feature available to users.

## Explanation

A deployment starts with a known artifact and changes the target environment's desired and running state. A typical process:

1. Selects the exact tested artifact, preferably by an immutable digest.
2. Validates configuration, secret access, permissions, and capacity.
3. Applies compatible infrastructure or database changes when required.
4. Starts or updates application instances.
5. Waits for startup and readiness checks before routing traffic.
6. Shifts traffic according to the rollout strategy.
7. Monitors errors, latency, and relevant business signals.
8. Completes the rollout or restores a known-good state.

Health checks answer different questions: a startup check determines whether initialization finished, readiness determines whether an instance can receive traffic, and liveness determines whether it must be restarted. A running process is not necessarily ready.

Common rollout strategies make different tradeoffs:

| Strategy | Mechanism | Main tradeoff |
| --- | --- | --- |
| **Rolling** | Replaces old instances gradually | Uses little spare capacity, but old and new versions coexist and rollback is incremental |
| **Blue-green** | Prepares a complete parallel version and switches traffic | Enables a fast traffic switch and application rollback, but requires duplicate capacity |
| **Canary** | Sends a small share of traffic to the new version before expanding | Limits blast radius, but requires traffic control and reliable metrics |

On failure, the system should keep traffic away from unready instances, retry only when the problem may be transient, stop after a defined threshold, and roll back the artifact or configuration when safe. Application rollback does not restore destructive database changes. Schema changes should preserve compatibility across mixed versions, often by expanding the schema, migrating reads and writes, and removing old structures only after they are unused.

The process may be started manually or automatically. [[Continuous deployment]] automatically runs the production deployment process for every validated change.

Deployment is different from [[Software release process|release]]. A version may be running in production while its new behavior remains hidden behind a feature flag.

## Example

A pipeline selects image digest `app:1.8@sha256:abc`, validates its production configuration, starts a small canary, and routes traffic only after readiness succeeds. If error rates remain acceptable, it expands the rollout; the new feature remains disabled until release.

## Connections

- Part of: [[Software delivery lifecycle]]
- Receives artifacts from: [[Software build process]], [[Software build automation]]
- Targets: [[Software deployment environments]]
- Can follow validation by: [[Continuous integration]]
- Can be automated through: [[Continuous deployment]]
- Makes software available for: [[Software release process]]
