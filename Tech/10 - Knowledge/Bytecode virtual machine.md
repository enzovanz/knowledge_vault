---
type: concept
domain: software engineering
created: 2026-09-13
aliases:
  - Bytecode VM
---
## Summary

A bytecode virtual machine is a software runtime that defines and executes an instruction set designed for a virtual machine rather than a physical CPU. Its bytecode may be interpreted, just-in-time compiled, or processed using both strategies.

## Explanation

Bytecode is a compact intermediate representation between source code and native machine code:

```text
Source code
    ↓ language frontend or bytecode compiler
Bytecode for a virtual instruction set
    ↓ virtual machine
Interpret the instructions or compile them at runtime
    ↓
CPU executes the runtime's native machine instructions
```

The virtual machine defines concepts such as:

- Available instructions or **opcodes**
- How values and program state are represented
- How functions are called
- How control flow and exceptions work
- How bytecode refers to names, constants, or objects

This is a **language virtual machine**, not a system virtual machine such as a virtualized Linux computer. It provides an abstract execution environment for programs, not a complete emulated computer.

### CPython as a bytecode virtual machine

CPython compiles Python source into code objects containing Python bytecode. Its evaluation loop reads one opcode at a time and dispatches to CPython's native implementation of that operation:

```text
Python source
    ↓ CPython parser and compiler
Python code object and bytecode
    ↓ CPython evaluation loop
Opcode selects a native CPython handler
    ↓
CPU executes the handler's machine instructions
```

For example, a Python addition opcode expresses a Python-level operation. It does not tell an ARM or x86 CPU to run one addition instruction. CPython may need to inspect object types, call a special method, allocate a result object, update reference counts, and handle errors. All of those steps are performed by native instructions from the CPython runtime and any native libraries it calls.

CPython bytecode is primarily an internal implementation format and can change between Python versions. Other runtimes use their own bytecode formats and execution strategies; for example, the JVM commonly combines bytecode interpretation with JIT compilation.

## Example

Python's `dis` module shows the bytecode instructions generated for a function:

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
```

The displayed opcodes are instructions for CPython's virtual machine, not the physical CPU.

## Connections

- Broader concept: [[Programming language execution models]]
- Common execution strategy: [[Interpretation]]
- May also use: Just-in-time compilation
- Example implementation: CPython
- Contrasts with native output from: [[Ahead-of-time compilation (AOT)]]
- Sources:
