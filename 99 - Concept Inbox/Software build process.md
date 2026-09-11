---
type: concept
domain: software engineering
created: 2026-09-09
---
## Summary

The software build process transforms source code and related inputs into artifacts that can be tested, distributed, or executed. The exact stages depend on the language and project.

## Explanation

A build process can include:

- Resolving dependencies
- Generating source code or assets
- Compiling source files
- Linking object files and libraries
- Running validation such as tests and static analysis
- Packaging the result

Not every project uses every stage. For example, a C application is normally compiled and linked into an executable, while a Python application may primarily need dependency resolution, validation, and packaging.

The **build process** describes what transformations and checks take place. [[Software build automation]] describes how tools execute and coordinate those steps repeatably.

## Example

A small C application can follow this process:

```text
C source files → object files → linked executable → packaged artifact
```

The compilation and linking stages can be performed manually or coordinated by a tool such as [[Make and Makefiles|Make]].

## Connections

- Stage: [[Compilation and linking]]
- Automated by: [[Software build automation]]
- Related: [[Make and Makefiles]], [[Continuous integration]]
- Sources:
