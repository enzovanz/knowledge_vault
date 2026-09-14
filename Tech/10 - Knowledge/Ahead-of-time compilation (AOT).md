---
type: concept
domain: software engineering
created: 2026-09-10
aliases:
  - Compilation and linking
  - AOT compilation
---
## Summary

Ahead-of-time compilation (AOT) translates a program before it runs, commonly producing native machine code for a specific operating system and CPU architecture. Compilation, assembly, and linking are stages commonly used by native AOT toolchains.

## Explanation

In a simplified C build:

```text
C source files
      ↓ compiler toolchain
Object files containing machine code and metadata
      ↓ linker
Native executable or library
      ↓ operating-system loader
Machine instructions executed by the CPU
```

Each source file can be compiled separately into an **object file** containing machine code, symbols, and information the linker still needs. The linker combines object files and libraries, resolves references between them, and produces the final executable or library.

The operating system's loader later maps the executable and any required shared libraries into memory and starts the program. Loading happens at runtime, but the program's machine code was compiled ahead of time.

Separate compilation also enables incremental builds. When one source file changes, only its object file normally needs to be recompiled, after which the affected executable or library is linked again.

AOT describes **when compilation happens**: before execution. It contrasts with just-in-time compilation (JIT), which generates native code while a program is running. AOT output is often native code, although a tool may also compile ahead of time to an intermediate representation used by another runtime.

## Example

```shell
cc -c main.c -o main.o
cc -c math.c -o math.o
cc main.o math.o -o app
```

The first two commands compile the source files into object files. The last command links those object files into the native executable `app`.

## Connections

- Broader concept: [[Programming language execution models]]
- Common runtime alternative: [[Interpretation]]
- Contrasts with: Just-in-time compilation
- Part of: [[Software build process]]
- Automated by: [[Software build automation]], [[Make and Makefiles]]
- Sources:
