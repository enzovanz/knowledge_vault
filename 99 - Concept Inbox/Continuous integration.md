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

- Platform example: [[CircleCI]]
- Can invoke: [[Software build automation]], [[Make and Makefiles]]
- Validates: [[Software build process]]
- Sources:
