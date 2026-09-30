---
type: concept
domain: software engineering
created: 2026-09-09
aliases:
  - Makefiles and build automation
---
## Summary

`make` is a build automation tool that reads rules from a file usually named `Makefile`. It models a build as a dependency graph and uses file modification times to rebuild only outdated targets.

## Explanation

### Rules, targets, prerequisites, and recipes

A Makefile contains rules that describe targets, their prerequisites, and the recipes used to produce them:

```makefile
app: main.o math.o
	cc main.o math.o -o app

main.o: main.c
	cc -c main.c -o main.o

math.o: math.c
	cc -c math.c -o math.o
```

The general structure is:

```makefile
target: prerequisites
	recipe
```

For example:

```makefile
main.o: main.c
	cc -c main.c -o main.o
```

The whole block is a **rule**. Its parts are:

- `main.o`: target
- `main.c`: prerequisite, also commonly called a dependency
- `cc -c main.c -o main.o`: recipe that produces the target

A recipe can contain multiple commands. Each recipe line normally starts with a tab:

```makefile
main.o: main.c
	echo "Compiling main.c"
	cc -c main.c -o main.o
```

### Modification-time comparison

When considering a file target, `make` runs its recipe when:

- The target does not exist; or
- At least one normal prerequisite is newer than the target.

Otherwise, the target is already up to date and its recipe is skipped.

The comparison propagates through the dependency graph. If `main.c` changes:

1. `main.o` becomes outdated and is recompiled.
2. The new `main.o` becomes newer than `app`.
3. `app` is relinked using both object files.

The same applies to `math.c`:

```text
main.c changed → rebuild main.o → rebuild app
math.c changed → rebuild math.o → rebuild app
```

Only the affected object file is recompiled, but the application must be relinked. This is an incremental build.

### Running targets

```shell
make          # Build the first target in the Makefile
make app      # Build app
make clean    # Run the clean target
```

### Phony targets

Some targets represent actions rather than files:

```makefile
.PHONY: clean test

clean:
	rm -f app *.o

test:
	./run-tests
```

Without `.PHONY`, a real file named `clean` could cause `make clean` to consider the target up to date and skip its recipe.

A phony target:

- Is not treated as a file
- Is always considered out of date
- Runs whenever it is explicitly requested or reached as a prerequisite

A normal dependency on a phony target also causes the dependent target to be considered out of date:

```makefile
.PHONY: prepare

app: prepare main.o math.o
	cc main.o math.o -o app

prepare:
	echo "Preparing build"
```

Here, both `prepare` and the `app` recipe run whenever `app` is evaluated. To run `prepare` first without using it to determine whether `app` is outdated, make it an **order-only prerequisite** with `|`:

```makefile
app: main.o math.o | prepare
	cc main.o math.o -o app
```

## Example

```makefile
.PHONY: all clean

all: app

app: main.o math.o
	cc main.o math.o -o app

main.o: main.c
	cc -c main.c -o main.o

math.o: math.c
	cc -c math.c -o math.o

clean:
	rm -f app main.o math.o
```

In short:

```text
Makefile describes the dependency graph
             ↓
make determines what is outdated
             ↓
recipes rebuild only what is necessary
```

## Make inside a CI/CD pipeline

[[GitHub Actions]] or [[CircleCI]] can invoke Make from a pipeline step. The platform handles the trigger, runner, job coordination, and result reporting; the Makefile supplies the project commands and target dependencies.

```text
Pull request → GitHub Actions job → make test → test recipe
Developer's terminal            → make test → same test recipe
```

Make can run tests, build packages, or invoke deployment scripts, but it does not itself provide hosted runners or listen for GitHub events. It is useful alongside CI/CD platforms. See [[GitHub Actions#Example]] for a workflow and Makefile used together.

## Connections

- Broader concept: [[Software build automation]]
- Related: [[Software build process]], [[Ahead-of-time compilation (AOT)]]
- Can be invoked by: [[Continuous integration]], [[GitHub Actions]], [[CircleCI]]
- Sources:
