---
type: concept
domain: software engineering
created: 2026-09-15
---
## Summary

A feature flag is a runtime decision point that changes which behavior a user receives without requiring a new deployment. It can separate deployment from release, support experiments and gradual rollouts, act as an operational kill switch, or control entitlements.

## Explanation

Code for a new behavior can be deployed while its flag remains disabled. A flagging system evaluates the flag when the application runs, optionally using context such as the user, organization, or rollout percentage, and selects the enabled or disabled path. The team can then expose the behavior to internal users, a beta group, a percentage of customers, or everyone, and quickly disable it if problems appear.

Although the decision appears to be an `if` statement, operating flags at scale requires more infrastructure: configuration storage, contextual evaluation rules, an administrative interface, permissions, an audit trail, and usage telemetry. Building only the initial switch hides this larger “iceberg” of platform complexity.

Flags also create technical debt. A temporary release or experiment flag should normally move through a lifecycle—development, limited rollout, full release, and removal—but it becomes stale when its configuration and conditional code remain after the decision is permanent. Teams can keep this debt under control by recording each flag's owner, purpose, lifecycle stage, and expiration date; detecting flags that are expired, fully released, or no longer evaluated; and reserving time to remove both the configuration and dead code.

A flag should be introduced only when its release-safety or experimentation benefit outweighs its ongoing management and testing cost. Prefer a small number of well-placed decision points over checks scattered through every layer of the system.

## Example

An online store is adding gift wrapping across its catalog, cart, and fulfillment services. It deploys the compatible backend changes first, but places a single flag at the front-end entry point so customers cannot request gift wrapping while the flag is off. The team enables it for employees, then a percentage of customers to measure conversion, and can turn it off if the feature fails. Once the rollout is permanent, it removes the flag and the obsolete path. This placement is the **keystone interface** pattern: one gate provides the benefit without spreading flag checks throughout the system.

## Connections

- Separates deployment from: [[Software release process]]
- Can be used by: [[Continuous deployment]]
- Example feature-flagging platform: [[PostHog]]
- Source: [Feature Flags Suck! - The Problems With Feature Flagging and How To Avoid Them - Pete Hodgson, PH1](https://www.youtube.com/watch?v=MDERgrcaT6w)
