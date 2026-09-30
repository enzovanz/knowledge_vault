---
type: concept
domain: software engineering
created: 2026-09-30
---
## Summary

GitHub Actions is GitHub's platform for running automation in response to repository events, schedules, or manual requests. It can implement [[Continuous integration|CI]] and [[Continuous deployment|CD]], and also automate repository maintenance, documentation, and issue management.

Actions workflows can call [[Make and Makefiles|Make]]: GitHub Actions coordinates when and where jobs run, while Make defines project commands and dependencies between build targets.

## Explanation

### How the pieces fit together

- **Workflow:** an automated process defined in a YAML file, such as `ci.yml`.
- **Event:** what starts a workflow run, such as a push, pull request, or schedule.
- **Job:** a group of steps executed on a runner. Jobs can run in parallel; `needs` declares dependencies between them.
- **Runner:** the machine that executes a job. GitHub provides hosted runners, or you can manage your own.
- **Step:** a command or reusable action within a job. Steps normally execute in order and share the job's workspace.
- **Action:** a reusable component invoked with `uses`, such as checking out a repository or setting up Python. An action is a building block within a workflow, not a synonym for the entire workflow.

```text
Pull request opened or updated
    → workflow run starts
    → job gets a runner
    → checkout, setup, and test steps execute
    → GitHub reports the check result on the pull request
```

Separate jobs should not assume they share a filesystem. If one job builds a package and another deploys it, transfer the artifact explicitly, for example with artifact upload/download actions or a package registry.

### The `.github` directory

`.github` is a **directory at the repository root**, not a single file. GitHub recognizes particular files and subdirectories inside it. A possible layout is:

```text
my-project/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── deploy.yml
│   │   └── check-links.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CODEOWNERS
│   └── dependabot.yml
├── Makefile
├── pyproject.toml
├── requirements-dev.txt
├── src/
└── tests/
```

| Location | Purpose |
| --- | --- |
| `.github/workflows/*.yml` or `*.yaml` | GitHub Actions workflow definitions. Names such as `ci.yml` and `deploy.yml` are choices, not reserved names. |
| `.github/ISSUE_TEMPLATE/` | Issue templates in Markdown or issue forms in YAML. |
| `.github/PULL_REQUEST_TEMPLATE.md` | Starting text for pull request descriptions. |
| `.github/CODEOWNERS` | Maps files and directories to people or teams for review requests. Requiring their approval also involves repository protection settings. |
| `.github/dependabot.yml` | Configures Dependabot version updates, such as opening pull requests for outdated packages or action versions. |

Only the files in `workflows/` in this example define Actions workflows. Templates, code ownership, and Dependabot are separate GitHub features. Their configuration does not become a workflow just because it lives under `.github`.

The directory is also different from `.git/`, which contains Git's local repository metadata. `.github/` configuration is normally committed and reviewed with the project. Settings such as required status checks and deployment credentials are configured separately in GitHub; this directory does not contain every repository setting.

### Anatomy of a workflow file

YAML uses indentation to express nesting. Use spaces for YAML indentation.

| Key | What it controls |
| --- | --- |
| `name` | The workflow's display name. |
| `on` | Trigger events and filters, such as pushes to `main`. |
| `permissions` | Access granted to the workflow's `GITHUB_TOKEN`. |
| `jobs` | The jobs in this workflow, indexed by identifiers you choose. |
| `runs-on` | The runner selection for a job, such as `ubuntu-latest`. |
| `needs` | Jobs that must complete successfully before this job normally runs. |
| `steps` | The steps within a job. |
| `uses` | Invokes a reusable action in a step, such as `actions/checkout@v6`. |
| `with` | Inputs passed to that action. |
| `run` | Shell commands to execute in a step. |
| `env` | Environment variables available at the workflow, job, or step scope. |

A `run` step can invoke Python, a shell script, a compiler, a deployment CLI, or Make. Actions does not require a Makefile.

### Things you can automate

| Trigger | Example automation |
| --- | --- |
| Pull request | Check formatting, lint code, run tests, and build the project. |
| Pull request or push | Test across several language versions or operating systems with a job matrix. |
| Push to `main` | Build an artifact, deploy to staging, and run smoke tests. |
| Version tag or release | Publish a package or container image, or deploy a selected version. |
| Scheduled run | Check documentation links, run a longer test suite, or generate a maintenance report. |
| Issue or pull request event | Apply labels or validate contribution metadata. |
| Manual request (`workflow_dispatch`) | Run an on-demand diagnostic or deploy a chosen version. |

These are possibilities you configure, not behaviors enabled automatically by adding `.github/`. Publishing, labeling, and deployment jobs also need appropriate permissions and credentials. A manual trigger requires the workflow definition to exist on the default branch.

For this knowledge base, useful examples would be checking Markdown formatting, detecting broken Obsidian links, checking external links on a schedule, or building and publishing a documentation site. Checking `[[Obsidian links]]` requires a checker that understands that syntax.

A workflow that deploys every validated change to production without human approval implements continuous deployment. If production deployment waits for approval, it can support continuous delivery. GitHub Actions is the tool; the workflow's behavior determines which practice it implements.

### How this differs from Make

| Question | GitHub Actions | Make |
| --- | --- | --- |
| What is its main role? | Coordinate event-driven workflows and their execution environments. | Execute target recipes according to a dependency graph. |
| What describes the work? | YAML workflows containing jobs and steps. | Makefile rules containing targets, prerequisites, and recipes. |
| What starts it? | Repository events, schedules, manual requests, or API calls. | A process invokes `make`, locally or inside automation. |
| How does it decide what to run? | Triggers, conditions, job dependencies, and matrices. | Requested targets and prerequisites; file timestamps determine which file targets need rebuilding. |
| Where does it run? | Jobs execute on selected hosted or self-hosted runners. | Wherever Make is installed and invoked, including an Actions runner. |

There is overlap: both can coordinate commands, and a Make target can run tests or deployment scripts. Make itself does not supply GitHub event handling, hosted runners, pull request check reporting, or deployment approvals. Actions does not automatically infer which object files need recompilation from a Makefile dependency graph.

Using them together lets developers and CI call the same project commands. Make's incremental builds still depend on the relevant files being present: a fresh checkout on a fresh runner will not automatically retain outputs from a previous workflow run.

## Example

Suppose a Python project has a `pyproject.toml`, tests, and a `requirements-dev.txt` containing `pytest`, `build`, and any other test dependencies. These are illustrative project files, not requirements for this knowledge base.

The project's `Makefile` defines the commands:

```makefile
.PHONY: install test build

install:
	python -m pip install -r requirements-dev.txt
	python -m pip install -e .

test:
	python -m pytest

build:
	python -m build
```

Recipe lines begin with a **tab**. These targets are phony, so the selected recipe runs each time; this example uses Make as a command interface rather than demonstrating incremental compilation.

The file `.github/workflows/ci.yml` defines when and where those commands run:

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - name: Check out the repository
        uses: actions/checkout@v6

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: make install

      - name: Run tests
        run: make test

      - name: Build the package
        run: make build
```

`checks` is a job identifier chosen by the author. `@v6` and `@v5` select versions of the reusable actions; `python-version: "3.12"` selects the Python runtime. The Ubuntu hosted runner supplies Make, while `setup-python` selects Python for subsequent steps.

Here, `on` starts the workflow for pull requests, pushes to `main`, or a manual request. The job downloads the source, prepares Python, and executes the Make targets. If tests fail, the job fails and the build step is normally skipped. There is no deployment step in this example.

```text
GitHub Actions → run: make test → Makefile recipe → python -m pytest
Developer     →      make test → Makefile recipe → python -m pytest
```

To make a successful CI check a condition for merging, configure the repository's ruleset or branch protection to require that check. Defining a workflow alone does not enforce that policy.

## Connections

- Implements: [[Continuous integration]], [[Continuous deployment]]
- Can invoke: [[Software build automation]], [[Make and Makefiles]]
- Can automate: [[Software deployment process]], [[Software release process]]
- Comparable platform: [[CircleCI]]; see [[Continuous integration#Examples of CI/CD platforms]] for GitLab CI/CD, Jenkins, and Azure Pipelines.
- Sources:
  - [GitHub: Understanding GitHub Actions](https://docs.github.com/en/actions/get-started/understand-github-actions)
  - [GitHub: Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
  - [GitHub: Building and testing Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
  - [GitHub: About issue and pull request templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates)
  - [GitHub: About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
  - [GitHub: Dependabot options reference](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference)
  - [GNU Make: Overview](https://www.gnu.org/software/make/manual/html_node/Overview.html)
