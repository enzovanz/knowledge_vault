# Learning: Software Delivery Lifecycle and Environments

Started: 2026-09-15

Legend: `[ ]` not started, `[~]` in progress, `[x]` mastered through explanation and quiz.

## 1. The problem the lifecycle solves

- [x] Explain why source code cannot safely move straight from an engineer's machine to users
- [x] Identify the risks the delivery lifecycle controls and the feedback each stage provides
- [x] Explain why teams separate transformations, environments, and user exposure

## 2. Build, automation, and continuous integration

- [x] Distinguish source code, build inputs, and an immutable deployable artifact
- [x] Distinguish the build process from build automation
- [x] Explain what continuous integration validates and why frequent integration matters
- [x] Explain the principle "build once, deploy many" and what can vary by environment

## 3. Deployment environments and promotion

- [x] Define an environment in terms of infrastructure, configuration, secrets, data, and access
- [x] Explain the purposes and limitations of development, test, staging, preview, and production environments
- [x] Distinguish artifact promotion from rebuilding
- [x] Explain environment parity, why perfect parity is difficult, and the risks of environment drift

## 4. Deployment mechanics

- [x] Explain what state changes during deployment
- [x] Trace artifact selection, configuration, migrations, startup, health checks, and rollback
- [x] Compare rolling, blue-green, and canary deployments and choose between them
- [x] Reason about failure cases such as bad configuration, failed health checks, and incompatible database migrations

## 5. Delivery, deployment, and release

- [x] Distinguish continuous integration, continuous delivery, and continuous deployment
- [x] Distinguish deployment from release using environment state and user availability
- [x] Explain how feature flags decouple deployment from release
- [x] Explain technical rollback versus release rollback

## 6. End-to-end mastery

- [x] Trace one change from source code to a versioned artifact, through environments, into production, and finally to users
- [x] Diagnose ambiguous team language such as "it is released" or "CD failed"
- [x] Handle edge cases: deployed but unreleased, released without a new deployment, and different versions across environments
- [x] Teach the complete model back clearly at both high and low levels

## Working example

We will follow one application change through this sequence:

```text
Source change
  -> validation and build
  -> immutable versioned artifact
  -> deployment into an environment
  -> running production software
  -> controlled user release
```

## Session notes

- Mastery is recorded only after teach-back and an edge-case question.
- Initial diagnostic: correctly identified uncertainty after coding, progressive validation through environments, and staging as a production-like proving ground. Still to sharpen: build/CI before deployment, the purpose of development versus test environments, and deployment versus user release.
- Stage 1 quiz: correctly diagnosed production-only configuration/secret drift and proposed deployment-time validation; correctly identified software that is deployed to production but not released behind a disabled feature flag.
- Stage 1 teach-back: explained that deployment can support production testing and limited-user rollout before broad release, reducing the blast radius of a faulty feature.
- Stage 2 diagnostic: correctly identified Docker image `app:2.0` as the artifact. Currently conflates build automation with CI and treats the merge as the build process; did not yet explain why the same artifact should be promoted.
- Stage 2 check: correctly explained that a manual `make package` run contains a build process and build automation but is not CI. Recognized that rebuilding changes the artifact; still needs to explain why builds differ and why validation evidence belongs to the artifact rather than only the source commit.
- Artifact promotion check: explained how a mutable Node base image can make the same source commit produce a different artifact, and correctly identified secrets and replica counts as environment-specific rather than artifact contents.
- CI check: correctly recognized that automated validation can be CI without deployment and identified fast feedback as a benefit. Still needs to distinguish frequent pushes to an isolated branch from frequent integration into shared code, and CI feedback from deployment feedback.
- CI re-check: explained that private-branch pushes still test code in isolation, while frequent shared-branch integration validates it together with other engineers' changes. Stage 2 mastered.
- Stage 3 diagnostic: identified databases, secrets, compute, infrastructure, and user traffic as environment concerns; correctly described development as fast-feedback, staging as production-like, and production as user-facing. Needs to define test and preview, separate CI runners from development environments, and distinguish infrastructure from the complete environment. Artifact promotion was already mastered in Stage 2.
- Environment check: explained that identical artifacts still run in different environments when data, integrations, and infrastructure differ; correctly identified a disposable CI VM as an ephemeral test runner rather than the development environment.
- Environment roles and parity check: correctly matched preview, test, and staging to their intended workloads; diagnosed database-version divergence as environment drift and proposed version pinning with automated provisioning. Stage 3 mastered.
- Stage 4 diagnostic: identified integration tests as a pre-deployment gate, production infrastructure and running instances as rollout concerns, and health-check failure as a reason to stop or retry. Needs to trace configuration, migrations, readiness, traffic shifting, observation, and rollback; rollout strategies are new.
- Deployment sequence check: ordered artifact selection, configuration validation, instance startup, readiness, traffic shifting, and monitoring correctly; explained retry for transient readiness failures and rollback for a persistent faulty version.
- Rollout strategy check in progress: selected rolling correctly for a backward-compatible stateless service with limited spare capacity; tradeoff reasoning and the blue-green/canary cases remain to verify.
- Rollout strategy completion: explained rolling version coexistence and slower rollback, and correctly selected blue-green for instant switching and canary for limited real-traffic exposure.
- Migration failure teach-back: explained expand-and-contract compatibility, migration of reads and writes, verification that the old state is unused, and later removal. Stage 4 mastered.
- Stage 5 carry-forward: deployment versus release was already demonstrated through production deployment with controlled or disabled user exposure; CI is mastered, while continuous delivery versus deployment and rollback types remain to verify.
- Stage 5 diagnostic: correctly distinguished feature-flag rollback (user exposure) from application-version rollback (deployed runtime). Initially described continuous deployment as general environment automation and continuous delivery as automated delivery to users; needs the production automation/manual-gate distinction.
- CI/CD completion: correctly identified a pipeline with a manual production gate as continuous delivery, automatic production deployment as continuous deployment, and a disabled feature flag as deployed but unreleased behavior. Stage 5 mastered.
- Final teach-back attempt: accurately covered CI runners, an immutable image, staging, production health checks, rolling/blue-green/canary rollout, feature-flag separation, and application/configuration/database rollback differences. Still conflates Git branches with deployment environments, treats continuous delivery and deployment as sequential phases, places mocks too broadly in staging, and needs to make the risk-reduction purpose of each boundary explicit.
- Final correction check: distinguished Git history branches from runtime environments, corrected artifact deployment to staging/production environments, and correctly mapped manual versus automatic production gates to continuous delivery versus continuous deployment.
- Ambiguity/edge-case check: proposed useful health, retry, feature, environment, and failure questions, but did not first disambiguate what "CD" means or locate the failed pipeline boundary. Edge-case labels were too compressed and treated staging-v3/production-v2 as generically "waiting for delivery" rather than distinguishing intentional promotion lag from drift or a stuck pipeline.
- Ambiguity re-check: correctly asked whether CD meant continuous delivery or deployment and localized the failure across build, staging deployment, production approval/rollout, or release. Correctly labeled deployed-with-flag-off and later flag enablement; still needs to describe the production state transition caused by artifact promotion.
- Final promotion check: identified that promoting the same digest changes the production environment's running version without rebuilding the artifact; after correction, explained that a disabled feature flag leaves user exposure unchanged, so deployment occurred without release. All objectives mastered.
