---
type: concept
domain: software engineering
created: 2026-09-10
aliases:
  - CI
---
## Summary

Continuous integration (CI) is the practice of integrating code changes frequently and automatically validating each change. It gives the team fast feedback when a change breaks expected behavior or quality checks.

## Explanation

A push or pull request commonly triggers a CI pipeline. The CI system creates a controlled environment, checks out the code, installs dependencies, and runs a sequence of automated checks such as:

- Formatting verification
- Linting and static analysis
- Unit and integration tests
- Building and packaging

The individual commands return exit codes. A nonzero exit code normally fails the step and therefore the job or pipeline. CI orchestrates these commands but often delegates the actual work to existing project tools such as `make`, Black, pytest, or a compiler.

Continuous integration is distinct from continuous delivery and continuous deployment, which concern making validated changes available to users or deploying them automatically.

### Examples of CI/CD platforms

CI is a practice; the platform runs the automation used to support it. Several tools fill a similar role:

| Platform | How it expresses or runs automation |
| --- | --- |
| [[GitHub Actions]] | YAML workflows in `.github/workflows/`, triggered by repository events, schedules, or manual requests. |
| [[CircleCI]] | Jobs and workflows in `.circleci/config.yml`; see [CircleCI's configuration guide](https://circleci.com/docs/introduction-to-yaml-configurations/). |
| GitLab CI/CD | Pipelines with jobs and stages, usually defined in `.gitlab-ci.yml`; see [GitLab's getting-started guide](https://docs.gitlab.com/ci/). |
| Jenkins | An extensible automation server whose pipelines can be stored in a `Jenkinsfile`; see [Jenkins Pipeline](https://www.jenkins.io/doc/book/pipeline/). |
| Azure Pipelines | Azure DevOps pipelines that coordinate build, test, and deployment tasks; see [Microsoft's overview](https://learn.microsoft.com/en-us/azure/devops/pipelines/get-started/what-is-azure-pipelines?view=azure-devops). |

These platforms can also support delivery and deployment. Their syntax, hosting, and integrations differ, but each can invoke project tools such as `make`, test runners, compilers, or deployment scripts.

### CI orchestration versus build automation

The CI platform decides when checks run, prepares an execution environment, coordinates jobs, and reports their results. [[Software build automation]] tools define and execute the project's build work. For example, [[GitHub Actions]] can run `make test`, and [[Make and Makefiles|Make]] then invokes the test command defined in its recipe. The same Make target can also run on a developer's machine.

Passing CI can be required before merging, but that requirement must be configured in the repository's ruleset or branch protection. Merely defining a workflow does not enforce a merge requirement.

## Example

```text
Git push
   ↓
CI pipeline starts
   ↓
Environment and dependencies are prepared
   ↓
Formatting, tests, and build commands run
   ↓
Results are reported to the team
```

## Connections

- Platform examples: [[GitHub Actions]], [[CircleCI]]
- Can invoke: [[Software build automation]], [[Make and Makefiles]]
- Validates: [[Software build process]]
- Can provide validated changes for: [[Continuous deployment]]
- Sources:
