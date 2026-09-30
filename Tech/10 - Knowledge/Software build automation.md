---
type: concept
domain: software engineering
created: 2026-09-09
---
## Summary

Build automation is the use of tools to turn source code into a usable product through repeatable commands. The tool coordinates the required steps and runs them in the correct order.

## Explanation

A software build can include:
- Compiling source files
- Linking binaries
- Running tests and linters
- Generating documentation
- Packaging and publishing build artifacts

Automating these steps makes builds repeatable and reduces manual errors. Some build tools also understand dependencies between outputs and inputs, allowing them to run only the steps affected by a change. This is called an **incremental build**.

Build automation tools include Make, Ninja, Gradle, Maven, Cargo, and Bazel. CMake is primarily a build-system generator: it produces build files that another tool, such as Make or Ninja, executes.

Tools such as [[GitHub Actions]] and [[CircleCI]] operate at the pipeline level: they respond to events, select execution environments, coordinate jobs, and report results. A pipeline can invoke a build tool, for example with `make build`. Keeping project commands in a Makefile allows the same commands to run locally and in CI.

## Example

When one C source file changes, a dependency-aware build can recompile only that file and then relink the application instead of recompiling the entire project. [[Make and Makefiles|Make]] is one tool that supports this workflow.

## Connections

- Related: [[Software build process]]
- Implementation: [[Make and Makefiles]]
- Can be invoked by: [[Continuous integration]], [[GitHub Actions]], [[CircleCI]]
- Produces artifacts used by: [[Software deployment process]]
- Sources:
