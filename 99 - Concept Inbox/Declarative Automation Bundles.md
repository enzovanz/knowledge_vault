---
type: concept
domain: data engineering
created: 2026-10-06
---
## Summary

Declarative Automation Bundles, previously named as Databricks Asset Bundles, describe a Databricks project as versioned configuration, source files, and build artifacts. The Databricks CLI resolves that desired state for a target, uploads code, and reconciles managed workspace resources such as jobs and pipelines.

## Explanation

### The problem bundles solve

Editing jobs directly in the Databricks UI makes live workspace state the only record of the change. That weakens code review, reproducibility, environment consistency, and rollback.

A bundle instead keeps the intended project in source control:

```text
bundle configuration + source code + build inputs
                        ↓
              resolve a target
                        ↓
             validate and plan
                        ↓
                      deploy
                        ↓
       workspace files + managed resources + state
```

Deployment is reconciliation. The checked-out bundle describes what should exist; the CLI applies that description to a target Databricks workspace. Deployment does not itself run a job.

### Native bundle components

A bundle has one root `databricks.yml`. It can compose additional configuration files through `include`.

| Component | Purpose |
| --- | --- |
| `bundle` | Defines bundle identity and CLI compatibility. |
| `include` | Adds configuration files to the bundle configuration graph. |
| `resources` | Declares Databricks objects such as jobs, pipelines, dashboards, schemas, and models. |
| `targets` | Defines named deployment overlays such as `dev`, `staging`, or `prod`. |
| `sync` | Selects source files and directories to upload to workspace storage. |
| `artifacts` | Builds and uploads packages such as Python wheels or JARs. |
| `variables` and substitutions | Supply reusable or target-specific values. |
| `workspace` | Selects the remote workspace and bundle root, file, artifact, and state paths. |
| `run_as` | Selects the identity under which supported workflows execute. |
| `permissions` | Declares access for bundle resources. |
| `mode` and `presets` | Apply development or production behavior and reusable resource defaults. |

Three similarly named mechanisms have different roles:

```text
include   = compose configuration
sync      = upload ordinary source files
artifacts = build and upload packages
```

Including a job YAML makes the job part of the desired resource graph. It does not, by itself, package a Python library or guarantee that every notebook path is uploaded.

### Resources and identity

A job is one kind of bundle resource:

```yaml
resources:
  jobs:
    daily_sales_workflow:       # bundle resource key
      name: daily_sales         # workspace display name
      tasks:
        - task_key: transform   # node inside the job
          notebook_task:
            notebook_path: ./src/transform.py
            source: WORKSPACE
```

These identifiers are not interchangeable:

- The **resource key** is the stable logical key used by bundle configuration and deployment state.
- The **display name** is human-facing and can change.
- The **workspace resource ID** is the stable live Databricks identity.
- A **task key** identifies a node inside a job; it is not a separately owned job.

Each bundle target stores deployment state in the workspace. At a high level, state maps bundle resource keys to live resource IDs. Display names are not reliable identity because they are mutable and may not be unique.

Changing a display name while retaining the resource key normally updates the existing resource. Removing a previously deployed resource from the bundle can plan its deletion. Adding a declaration with no state association can plan creation.

`databricks bundle deployment bind` associates a bundle resource key with an existing workspace resource ID. `unbind` removes that state association without deleting or reconfiguring the live resource. Binding is useful when adopting an existing resource or deliberately transferring management while preserving its ID.

The workspace `root_path` is fundamental to bundle identity. By default, it is user-, bundle-, and target-scoped:

```text
/Workspace/Users/<user>/.bundle/<bundle-name>/<target>
```

Derived locations normally separate uploaded files, artifacts, and deployment state below that root.

### Targets and overrides

A target is a named configuration overlay, not merely a label. Target settings take precedence over corresponding top-level settings, while non-conflicting settings combine.

```yaml
resources:
  jobs:
    daily_sales_workflow:
      name: daily_sales
      performance_target: STANDARD

targets:
  prod:
    mode: production
    resources:
      jobs:
        daily_sales_workflow:
          performance_target: PERFORMANCE_OPTIMIZED
```

The resolved production job uses `PERFORMANCE_OPTIMIZED`. For keyed structures such as job tasks, matching keys such as `task_key` allow target settings to join and override the corresponding base task.

Selecting `-t prod` applies the `prod` overlay, but it does not automatically teach arbitrary application code which catalogs, schemas, or tables are production destinations. Those behaviors must be expressed through configuration and code, often with target-specific parameters or variables.

### Lifecycle commands

| Command | Role |
| --- | --- |
| `databricks bundle validate -t <target>` | Resolves the target and checks configuration structure, references, and substitutions. |
| `databricks bundle plan -t <target>` | Previews resource actions without applying them. |
| `databricks bundle deploy -t <target>` | Builds artifacts, uploads files, reconciles resources, and updates state. |
| `databricks bundle summary -t <target>` | Shows resolved or deployed resources, IDs, and links. |
| `databricks bundle run -t <target> <resource-key>` | Starts an already deployed job or pipeline. |
| `databricks bundle destroy -t <target>` | Removes resources and state managed by that bundle target. |

A source-only change can require deployment even if no job API settings changed: the new source still has to replace the workspace copy before later runs can execute it.

### Authentication, execution identity, and permissions

The identity invoking the Databricks CLI authenticates to the target workspace and must be authorized to create or update the managed resources. CI/CD systems can run the CLI, but the CI/CD platform is not part of the bundle specification.

`run_as` is separate from deployment authentication:

```text
deployment identity = who applies the bundle
run_as identity      = who executes the workflow tasks
resource permissions = who may view, run, or manage the resource
```

Declaring permissions makes them managed desired state. Treat the resolved permission list as an access-control contract rather than an additive patch; a partial declaration can remove live grants that were not preserved. A `run_as` identity also does not automatically receive every permission needed to invoke or manage the job through an API.

Development and production modes provide useful defaults and validation, while presets can customize behaviors such as name prefixes, tags, concurrency, or paused triggers. Resource-specific settings override presets. A paused schedule prevents automatic firing but does not necessarily prevent an authorized manual or API-triggered run.

## Example

```yaml
bundle:
  name: sales_pipeline

include:
  - resources/*.yml

sync:
  paths:
    - ./src

artifacts:
  sales_library:
    type: whl
    path: .

targets:
  dev:
    default: true
    mode: development
    workspace:
      host: https://example.cloud.databricks.com

  prod:
    mode: production
    workspace:
      host: https://example.cloud.databricks.com
      root_path: /Workspace/Production/.bundle/${bundle.name}/${bundle.target}
    run_as:
      service_principal_name: <service-principal-id>
```

The included YAML declares resources, `sync.paths` uploads notebook source, and `artifacts` builds the wheel. Deploying `dev` and `prod` resolves two target-specific deployments with separate state. A later `bundle run` starts a deployed resource; `bundle deploy` alone does not execute it.

## Connections

- Related: [[Software deployment process]], [[Software build process]], [[Software build automation]], [[Continuous integration]], [[Continuous deployment]], [[GitHub Actions]]
- Sources:
  - [Databricks: What are Declarative Automation Bundles?](https://docs.databricks.com/aws/en/dev-tools/bundles)
  - [Databricks: Bundle configuration](https://docs.databricks.com/aws/en/dev-tools/bundles/settings)
  - [Databricks: Override with target settings](https://docs.databricks.com/aws/en/dev-tools/bundles/overrides)
  - [Databricks: Bundle CLI commands](https://docs.databricks.com/aws/en/dev-tools/cli/bundle-commands)
  - [Databricks: Deployment modes](https://docs.databricks.com/aws/en/dev-tools/bundles/deployment-modes)
  - [Databricks: Run identity](https://docs.databricks.com/aws/en/dev-tools/bundles/run-as)
  - [Databricks: Resource permissions](https://docs.databricks.com/aws/en/dev-tools/bundles/permissions)
