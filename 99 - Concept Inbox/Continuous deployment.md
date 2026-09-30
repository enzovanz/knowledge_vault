---
type: concept
domain: software engineering
created: 2026-09-14
aliases:
  - CD
---
## Summary

Continuous deployment is the practice of automatically deploying every software change that passes the required automated validation to production. It uses a repeatable [[Software deployment process|deployment process]] without requiring a manual approval step for each production deployment.

## Explanation

A continuous deployment pipeline commonly:

- Receives a code change
- Runs continuous integration checks
- Builds and stores an immutable artifact
- Deploys that artifact to production automatically
- Runs health checks and monitors the rollout
- Stops or rolls back when automated safety checks fail

Continuous deployment describes **when and under what conditions deployment happens automatically**. The deployment process describes **how the artifact is installed, configured, started, verified, and rolled back**.

Continuous deployment is different from **continuous delivery**. In continuous delivery, every validated change is kept ready for production, but releasing or deploying it may still require a person to approve the action. Because both terms are abbreviated as **CD**, their intended meaning must be established from context.

Automatic deployment also does not require automatic release. A change can be continuously deployed to production while remaining unavailable to users behind a feature flag until the [[Software release process|release process]] exposes it.

### Tools that run the pipeline

[[GitHub Actions]], [[CircleCI]], GitLab CI/CD, Jenkins, and Azure Pipelines can coordinate testing, building, and deployment. These are automation platforms; using one does not by itself mean a team practices continuous deployment.

For example, a GitHub Actions workflow can run after a merge to `main`, validate the change, and deploy the resulting artifact. If every validated change proceeds to production automatically, this implements continuous deployment. If production requires a human approval, the workflow can support continuous delivery instead. Deployment jobs still need the commands, permissions, and credentials required by the target environment.

## Example

A developer merges a change into the main branch. The pipeline runs tests, builds Docker image `app:1.9`, deploys it to production, and verifies its health without waiting for manual approval. The new functionality remains disabled until the team enables its feature flag.

## Connections

- Receives validated changes from: [[Continuous integration]]
- Can be implemented with: [[GitHub Actions]], [[CircleCI]]
- Automates: [[Software deployment process]]
- Promotes artifacts through: [[Software deployment environments]]
- Can remain separate from: [[Software release process]]
- Sources:
