---
type: concept
domain: software engineering
created: 2026-09-13
---
## Summary

Interpretation is an execution strategy in which an interpreter reads a program representation and performs its operations while the program is running. The CPU does not execute the interpreted source or bytecode directly; it executes the interpreter's native machine instructions.

## Explanation

An interpreter is itself a program that has already been compiled for the physical CPU. It repeatedly examines the program being interpreted, determines what an instruction means, and runs the interpreter code that implements that behavior.

The input to an interpreter can have different forms:

- Source text
- An abstract syntax tree (AST)
- Bytecode for a virtual instruction set

This means interpretation and compilation are not opposites that must be chosen exclusively. An implementation can first compile source code into bytecode and then interpret that bytecode. CPython normally follows this combined model.

In simplified pseudocode, a bytecode interpreter behaves like this:

```c
while (running) {
    instruction = read_next_bytecode();

    if (instruction == LOAD_NAME)
        execute_name_lookup();
    else if (instruction == ADD)
        execute_python_addition();
}
```

The loop and functions such as `execute_python_addition()` are native machine code. A bytecode instruction can cause the interpreter to execute many CPU instructions; it is not normally a one-to-one replacement for a machine instruction.

Interpretation therefore answers **how instructions are carried out at runtime**. A [[Bytecode virtual machine]] describes the abstract instruction set and runtime environment those instructions target.

## Definitions and assignments are executable operations

Python definitions and assignments are statements that CPython executes. The compiler converts them into bytecode that tells the interpreter to create or retrieve objects and bind names to them.

### Variable assignment

```python
value = 10
```

Conceptually, this becomes:

```text
LOAD_CONST 10
STORE_NAME value
```

The integer is a Python object. `value` is not a separate “variable object”; the assignment binds the name `value` to that integer object. The exact storage opcode depends on the scope—for example, local variables inside a function commonly use `STORE_FAST`.

### Function definition

```python
def add(a, b):
    return a + b
```

CPython compiles the function body into a code object. When the `def` statement is executed, bytecode conceptually performs:

```text
LOAD_CONST <code object add>
MAKE_FUNCTION
STORE_NAME add
```

This creates a Python function object containing the code object and binds it to the name `add`. The bytecode inside that code object—such as `LOAD_FAST`, `BINARY_OP`, and `RETURN_VALUE`—runs only when the function is called.

This is why `dis.dis(add)` shows the function body's bytecode but not `MAKE_FUNCTION`: it disassembles the code object stored inside the already-created function. Disassembling the outer code that contains the `def` statement shows the function-creation operations.

### Class definition

```python
class Calculator:
    def add(self, a, b):
        return a + b
```

A class statement is executable too. In simplified terms, CPython:

1. Creates a code object for the class body.
2. Executes that body in a new namespace, creating members such as the `add` function.
3. Uses the class-building machinery and metaclass to create the class object.
4. Binds that object to the name `Calculator`.

The outer bytecode therefore contains operations conceptually similar to:

```text
LOAD_BUILD_CLASS
LOAD_CONST <code object Calculator>
MAKE_FUNCTION
CALL
STORE_NAME Calculator
```

### Decorators

A decorator is another example of a definition producing executable operations. This syntax:

```python
@logged
def add(a, b):
    return a + b
```

is approximately equivalent to:

```python
def add(a, b):
    return a + b

add = logged(add)
```

When the definition is executed, CPython creates the function object, calls `logged` with that object, and binds the name `add` to the object returned by `logged`. The decorator may return the original function, a wrapper function, or any other object.

The compiler recognizes the `@decorator` syntax, but the runtime behavior primarily uses ordinary Python operations: create an object, call an object, and bind a name. With multiple decorators, they are applied from the one closest to the function outward.

Exact bytecode instructions vary between Python versions, but the model remains the same:

```text
Python statement
      ↓ compiler
Bytecode describing object and name operations
      ↓ CPython interpreter
Native CPython handlers manipulate Python objects
      ↓
CPU executes the handlers' machine instructions
```

## Example

For a Python expression:

```python
result = a + b
```

CPython's simplified path is:

```text
Read the bytecode instruction requesting addition
                    ↓
Inspect the Python objects and their types
                    ↓
Select CPython's existing addition implementation
                    ↓
CPU executes that implementation's native machine code
```

## Connections

- Broader concept: [[Programming language execution models]]
- Related runtime: [[Bytecode virtual machine]]
- Used by: CPython
- Commonly compared with: [[Ahead-of-time compilation (AOT)]]
- Can be combined with: Just-in-time compilation
- Sources:
