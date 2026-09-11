---
type: concept
domain: software engineering
created: 2026-09-10
---
## Summary

Compilation translates source code into a lower-level form that a computer can execute. Linking combines compiled object files and libraries into a final executable or library.

## Explanation

In a simplified C build:

1. Each source file is compiled separately into an **object file** containing machine code and unresolved references.
2. The linker combines the object files with required libraries.
3. The linker resolves references between them and produces the final executable.

Separate compilation means that when one source file changes, only its object file normally needs to be recompiled. The object files must then be linked again to create an updated executable.

Some languages use different models, such as interpretation, bytecode, just-in-time compilation, or a combination of these approaches.

## Example

```shell
cc -c main.c -o main.o
cc -c math.c -o math.o
cc main.o math.o -o app
```

The first two commands compile the source files. The last command links their object files into `app`.

## Connections

- Part of: [[Software build process]]
- Automated by: [[Software build automation]], [[Make and Makefiles]]
- Sources:
