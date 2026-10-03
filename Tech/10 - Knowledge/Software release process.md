---
type: concept
domain: software engineering
created: 2026-09-14
---
## Summary

The software release process controls when and how a software version or feature becomes available to its intended users. A release changes user availability and may happen at the same time as deployment or after the software is already running in production.

## Explanation

A deployment and a release change different states:

| Action | State changed |
| --- | --- |
| [[Software deployment process|Deployment]] | Which artifact and configuration run in an environment |
| **Release** | Which users receive the behavior |

A release process can include:

- Deciding whether a change is ready for users
- Assigning a version and preparing release notes
- Obtaining technical, product, or business approval
- Enabling a feature flag or beginning a gradual rollout
- Monitoring user and system behavior
- Pausing or reversing the rollout when problems appear
- Communicating the change to users or internal teams

The word **release** is sometimes used differently across teams. It may mean publishing a versioned package, deploying a version to production, or exposing functionality to users. Asking whether something is *deployed to production* or *available to users* makes the intended meaning clearer.

Feature flags can separate the two actions. A version can be deployed with its feature disabled, then released to employees, a percentage of customers, and finally everyone without another deployment. Disabling the flag is a **release rollback** because it changes user exposure. Deploying a known-good artifact or restoring configuration is a **technical rollback** because it changes the running environment. Neither action automatically restores database or external-system state.

## Example

Version `app:1.8` is already deployed in production with its new feature disabled. The release begins with employees, expands to 10% of customers while the team monitors results, and finishes when the feature is available to everyone. If the behavior is faulty, the team disables the flag without redeploying.

## Connections

- Part of: [[Software delivery lifecycle]]
- Usually follows: [[Software deployment process]]
- Usually exposes software running in: [[Software deployment environments|a production environment]]
- Uses an artifact created by: [[Software build process]]
- Can be controlled by: [[Feature Flags]]
- Related validation practice: [[Continuous integration]]
