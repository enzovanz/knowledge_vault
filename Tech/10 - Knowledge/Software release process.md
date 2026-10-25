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

### Rolling release versus fixed release

These models describe how users receive software updates over time:

| Model | How updates reach users | Linux distribution example |
| --- | --- | --- |
| **Rolling release** | The installed system evolves through ongoing package updates, without a separate upgrade between named distribution releases. Individual packages still have versions. | [Arch Linux](https://archlinux.org/about/) uses a rolling release model: users maintain their existing installation through system updates. |
| **Fixed release** | Changes are grouped into discrete, versioned releases. Each supported release receives maintenance updates; moving to a newer release requires an explicit release upgrade or a fresh installation. | [Ubuntu](https://ubuntu.com/about/release-cycle) publishes scheduled releases with defined support periods. |

The distinction is the release model, not whether updates can modify an existing installation: fixed-release systems can also be upgraded in place. Rolling release does not mean updates install themselves automatically.

These models are separate from **continuous delivery**, which keeps validated changes ready for production, and [[Continuous deployment]], which deploys passing changes automatically. A team can use continuous delivery while publishing fixed releases. Rolling release also differs from a **rolling deployment**, which replaces running instances gradually during one deployment.

### Long-term support (LTS)

**Long-term support (LTS)** is a maintenance policy that keeps a designated version supported for an extended period. It generally prioritizes security patches and selected bug fixes while limiting disruptive changes, so users can keep a stable baseline without frequently upgrading to a new release. It does not promise all the newest features; the duration and scope of support depend on the project.

Rolling versus fixed release describes how updates are organized; LTS describes how long a version is maintained. For example, [Ubuntu's release cycle](https://ubuntu.com/about/release-cycle) includes both fixed LTS releases and shorter-supported interim releases. An organization can choose an LTS release, apply maintenance updates, and plan its next release upgrade before support ends.

## Example

Version `app:1.8` is already deployed in production with its new feature disabled. The release begins with employees, expands to 10% of customers while the team monitors results, and finishes when the feature is available to everyone. If the behavior is faulty, the team disables the flag without redeploying.

## Connections

- Part of: [[Software delivery lifecycle]]
- Usually follows: [[Software deployment process]]
- Usually exposes software running in: [[Software deployment environments|a production environment]]
- Uses an artifact created by: [[Software build process]]
- Can be controlled by: [[Feature Flags]]
- Related validation practice: [[Continuous integration]]
