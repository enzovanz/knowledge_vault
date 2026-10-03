---
type: moc
domain: software engineering
---
## Overview

Software engineering covers the principles and practices used to design, build, deploy, and maintain reliable software systems. It includes architecture, code quality, concurrency, collaboration, testing, and the management of change over time.

## Learning path

Work from top to bottom and focus on only the first two or three unchecked topics.

### Code execution concept map

This map separates instructions for language tools from instructions the physical CPU can execute:

```mermaid
flowchart TD
    Models["Programming language execution models"]
    Models --> AOT["Ahead-of-time compilation"]
    Models --> Interpretation["Interpretation"]
    Models --> Bytecode["Bytecode virtual machines"]
    Models --> JIT["Just-in-time compilation"]
    Models --> Transpilation["Transpilation"]

    AOT --> CompileLink["Compilation and linking stages"]
    CompileLink --> Native["Native machine code"]
    Bytecode --> CPython["CPython evaluation loop"]
    JIT --> RuntimeNative["Native code generated at runtime"]

    Native --> CPU["CPU"]
    CPython --> CPU
    RuntimeNative --> CPU
```

See [[Programming language execution models]] for the detailed C and CPython execution paths, then continue into [[Ahead-of-time compilation (AOT)]], [[Interpretation]], and [[Bytecode virtual machine]].

### Product Engineering

#### Product Analytics

- [ ] [[PostHog]]
	- [ ] [[Feature Flags]]

### DevOps

#### Software delivery lifecycle

[[Software delivery lifecycle]] connects the state transitions from source code to user-visible behavior. Build automation and continuous integration describe how parts of that lifecycle are executed and validated repeatedly.

```mermaid
flowchart LR
    Source["Source code"] --> Build["Software build process"]
    Build --> Artifact["Deployable artifact"]
    Artifact --> Deploy["Software deployment process"]
    Deploy --> Environment["Software deployment environment"]
    Environment --> Running["Running software"]
    Running --> Release["Software release process"]
    Release --> Users["Available to users"]

    Automation["Software build automation"] -. coordinates .-> Build
    Make["Make and Makefiles"] --> Automation
    CI["Continuous integration"] -. invokes and validates .-> Automation
    CircleCI["CircleCI"] --> CI
    GitHubActions["GitHub Actions"] --> CI
```

##### Build and continuous integration

- [[Software build process]]
- [[Software build automation]]
- [[Make and Makefiles]]
- [[Continuous integration]]
- [[GitHub Actions]] — workflows, `.github` structure, automation examples, and how Actions works with Make
- [[CircleCI]]

##### Deployment and release

- [[Software deployment environments]]
- [[Software deployment process]]
- [[Continuous deployment]]
- [[Software release process]]

### SRE / Production Engineering

#### Observability

- [ ] Datadog

### Foundations

- [ ] Abstraction and modularity
- [ ] Cohesion and coupling
- [ ] Interfaces and contracts
- [[Programming language execution models]]
	- [[Ahead-of-time compilation (AOT)]]
	- [[Interpretation]]
	- [[Bytecode virtual machine]]
- [ ] Testing fundamentals
- [ ] [[Unit tests vs integration tests]]
- [ ] [[Code comments as context for humans and AI]]
- [ ] Refactoring

### Core topics

- [ ] [[DRY principle and knowledge duplication]]
- [ ] [[Orthogonality in software design]]
- [ ] [[Law of Demeter]]
- [ ] [[Application architecture models]]
- [ ] Dependency management
- [ ] Design patterns

### Advanced topics

- [ ] [[Blackboard architectural pattern]]
- [ ] [[Concurrency and parallelism]]
- [ ] [[Temporal coupling]]

When a topic becomes a developed note, keep its link in the appropriate topical section, remove the checkbox, and move the note from `99 - Concept Inbox` or `98 - Concept Backlog/Tech` to `Tech/10 - Knowledge`.
