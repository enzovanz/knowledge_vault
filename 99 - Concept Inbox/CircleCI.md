---
type: concept
domain: software engineering
created: 2026-09-10
---
## Summary

CircleCI is a platform for defining and running [[Continuous integration|CI]] pipelines. A repository commonly stores its CircleCI configuration in `.circleci/config.yml`.

## Explanation

Important CircleCI concepts include:

- **Pipeline:** the complete run triggered by an event such as a push
- **Workflow:** coordinates jobs and their order
- **Job:** a collection of steps executed in the same environment
- **Step:** an individual action, such as checking out code or running a command
- **Executor:** the environment in which a job runs, such as a Docker container or virtual machine

CircleCI is the orchestrator. It prepares the environment and decides which jobs and steps to run. Project tools still perform the underlying work. For example, a CircleCI step may call a Make target, whose recipe then invokes Black or pytest.

## Example

```yaml
version: 2.1

jobs:
  checks:
    docker:
      - image: cimg/python:3.12
    steps:
      - checkout
      - run: make format-check

workflows:
  validation:
    jobs:
      - checks
```

The execution chain is:

```text
CircleCI job → run step → make format-check → Make recipe → formatting tool
```

The Makefile determines what `format-check` means; CircleCI determines when and where it runs.

## Connections

- Implements: [[Continuous integration]]
- Can invoke: [[Make and Makefiles]], [[Software build automation]]
- Sources:
