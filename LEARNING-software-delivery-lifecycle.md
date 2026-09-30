# Learning: Software Delivery Lifecycle and Environments

Started: 2026-09-15

Legend: `[ ]` not started, `[~]` in progress, `[x]` mastered through explanation and quiz.

## 1. The problem the lifecycle solves

- [~] Explain why source code cannot safely move straight from an engineer's machine to users
- [ ] Identify the risks the delivery lifecycle controls and the feedback each stage provides
- [ ] Explain why teams separate transformations, environments, and user exposure

## 2. Build, automation, and continuous integration

- [ ] Distinguish source code, build inputs, and an immutable deployable artifact
- [ ] Distinguish the build process from build automation
- [ ] Explain what continuous integration validates and why frequent integration matters
- [ ] Explain the principle "build once, deploy many" and what can vary by environment

## 3. Deployment environments and promotion

- [ ] Define an environment in terms of infrastructure, configuration, secrets, data, and access
- [ ] Explain the purposes and limitations of development, test, staging, preview, and production environments
- [ ] Distinguish artifact promotion from rebuilding
- [ ] Explain environment parity, why perfect parity is difficult, and the risks of environment drift

## 4. Deployment mechanics

- [ ] Explain what state changes during deployment
- [ ] Trace artifact selection, configuration, migrations, startup, health checks, and rollback
- [ ] Compare rolling, blue-green, and canary deployments and choose between them
- [ ] Reason about failure cases such as bad configuration, failed health checks, and incompatible database migrations

## 5. Delivery, deployment, and release

- [ ] Distinguish continuous integration, continuous delivery, and continuous deployment
- [ ] Distinguish deployment from release using environment state and user availability
- [ ] Explain how feature flags decouple deployment from release
- [ ] Explain technical rollback versus release rollback

## 6. End-to-end mastery

- [ ] Trace one change from source code to a versioned artifact, through environments, into production, and finally to users
- [ ] Diagnose ambiguous team language such as "it is released" or "CD failed"
- [ ] Handle edge cases: deployed but unreleased, released without a new deployment, and different versions across environments
- [ ] Teach the complete model back clearly at both high and low levels

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
