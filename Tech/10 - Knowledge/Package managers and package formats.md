---
type: concept
domain: software engineering
created: 2026-10-26
---
## Summary

Software packages combine files with information that tells tools what they provide and how to install them. Package managers use that information to install compatible software and dependencies, track changes, and manage updates and removal.

## 1. Core concepts

| Concept | Meaning | Example |
| --- | --- | --- |
| **Software package** | A unit of distribution containing files and metadata such as name, version, and requirements | A curl `.deb`, a Python wheel |
| **Package format** | Rules for organizing those files and metadata | `.deb`, `.rpm`, `.whl` |
| **Package manager** | A tool that finds, installs, updates, and removes packages and resolves their requirements | Homebrew, APT, pip, npm |
| **Package repository** | An indexed collection of packages or installation recipes | A Debian repository; a Homebrew tap |
| **Package registry** | A service that catalogs package names, versions, metadata, and download locations | PyPI, the npm registry |

Repository and registry overlap in usage. Both distribute packages; a Git source repository primarily tracks development history and may live at a different URL.

### Archive, executable, and package

These describe different things:

- An **archive** groups files into one container. A ZIP of holiday photos is an archive, but has no software installation rules.
- An **executable** is a file that can be launched as a program, either as native machine code or through an interpreter. It does not necessarily describe its dependencies or installation procedure.
- A **package** gives software a form an installation tool understands: its files plus metadata describing what they are and what they require. A curl package might contain the executable, documentation, and a declaration that a compatible TLS library must be installed.

An archive can therefore be a package when it follows a packaging specification: a wheel is a ZIP with defined metadata and layout. Packages can also contain only fonts, documentation, or data. A **metapackage** mainly lists other packages to install together, without supplying an application itself.

### Libraries and dependencies

A **library** provides reusable code that other programs call—for example, encryption or image-decoding functions. It is usually used by a program rather than launched directly. Libraries can be distributed as source modules, compiled code, or both; they are not always precompiled.

A **dependency** is something software requires to build or work. If an application calls a library's functions, that library is a dependency. Its package metadata declares the required package and compatible versions; the manager checks what is installed and obtains anything missing. Dependencies can also be runtimes, tools, or data, not just libraries.

For native compiled code, the library's linking model affects distribution:

| Library type | How the program uses it | Installation and updates |
| --- | --- | --- |
| **Static**—commonly `.a` on Unix-like systems, `.lib` on Windows | The linker copies needed library code into the executable during the build. | That library file is not needed at runtime for the embedded code. Updating the library requires relinking and redistributing the program. |
| **Dynamic/shared**—`.so` on Linux, `.dylib` on macOS, `.dll` on Windows | The library stays separate and is loaded into the process at launch or when requested. | A compatible library must be available at runtime, installed separately or bundled with the application. A compatible update can serve existing programs without rebuilding them. |

Dynamic libraries can serve several programs, but incompatible replacements can break them. Static linking embeds a particular library's code; it does not imply that every other dependency is also embedded. See [[Ahead-of-time compilation (AOT)]] for compilation and linking, and [Apple's library overview](https://developer.apple.com/library/archive/documentation/DeveloperTools/Conceptual/DynamicLibraries/100-Articles/OverviewOfDynamicLibraries.html).

Installation places executables, libraries, and supporting files into the filesystem. The shell searches `PATH` for commands; native loaders locate shared libraries; language runtimes locate modules through their own search rules. These are separate mechanisms. The OS, CPU architecture, and runtime must also support the installed code.

## 2. Package formats

| Format | Contents and metadata | Installation |
| --- | --- | --- |
| **`.deb`** | An `ar` archive with `debian-binary`, `control.tar.*` metadata, and `data.tar.*` files. Metadata declares identity, architecture, dependencies, and optional maintainer scripts. | `dpkg` unpacks files, runs scripts, and records state; APT selects and fetches dependencies. |
| **`.rpm`** | Headers describe identity, dependencies, file lists, signatures/digests, and optional scripts; a compressed payload holds files, conventionally in CPIO format. | RPM installs and tracks files; tools such as DNF resolve repository dependencies. |
| **`.whl`** | A ZIP containing Python modules, optional native extensions, and `.dist-info`: `METADATA` describes requirements, `WHEEL` compatibility, and `RECORD` files/hashes. | An installer maps files into the Python environment and creates declared command wrappers. Wheels have no arbitrary installation hooks. |
| **`.tar.gz`** | A gzip-compressed tar archive; the suffix alone specifies no software metadata. Python source distributions add build configuration and package metadata; npm tarballs contain `package.json`. | Ecosystem-specific build/install rules are needed. A generic tarball has no universal installation procedure. |
| **`.dmg`** | A macOS disk image containing a filesystem, often holding an `.app` or `.pkg`. | Mounting exposes files. Installation usually means copying the app or running its installer; DMG itself has no dependency solver. |
| **macOS `.pkg`** | Modern flat packages use XAR containers with component metadata, file inventories, payloads, and optional scripts or installation checks. | Apple's Installer places files, runs scripts, and records receipts; it does not resolve repository dependencies like APT. |

**Source packages** require a build before installation; that may need compilers and development libraries. **Binary packages** contain ready-to-install output. “Binary” does not always mean machine code: a pure-Python wheel can contain Python source, while a native-extension wheel must match its interpreter and platform. See [[Software build process]].

Format references: [Debian](https://www.debian.org/doc/manuals/debian-handbook/sect.package-meta-information.en.html), [RPM](https://rpm.org/docs/6.0.x/manual/format_v4.html), [wheels](https://packaging.python.org/en/latest/specifications/binary-distribution-format/), [Python source distributions](https://packaging.python.org/en/latest/specifications/source-distribution-format/), [Apple disk images](https://support.apple.com/en-gb/guide/mac-help/mchlp1700/mac).

## 3. Package managers

### Why use a package manager?

A package manager automates work that would otherwise fall to the user or individual installers: finding downloads, checking requirements, placing files, recording ownership, and maintaining versions. Its main benefits are:

- **Convenience:** one interface coordinates installation, dependencies, updates, and removal. Manual installation may require downloading, extracting, building, configuring paths, and tracking updates yourself; vendor installers automate some of these steps too.
- **Security and maintenance:** trusted repositories, integrity/authenticity checks, and centralized security updates help administrators maintain systems. An upgrade command can update eligible packages within the manager's scope, rather than updating each application separately. It does not cover software installed outside that scope or guarantee safe code.
- **Compatibility:** dependency constraints, architecture checks, and declared conflicts help select packages that can work together. Distribution maintainers also integrate and test packages. These checks reduce breakage; they cannot detect every runtime bug or undeclared incompatibility.
- **Efficiency and space:** when two programs require the same compatible shared library package, APT can reuse one installed copy. The programs load the library from the filesystem; APT manages its installation and version. This avoids some duplicated files and downloads, although bundled libraries, incompatible versions, and isolated environments may still require separate copies.
- **Consistent administration:** the same workflow can manage many machines. APT works across Debian and Debian-derived systems using repositories appropriate to each distribution and release. This does not make arbitrary packages interchangeable across operating systems.
- **License visibility:** package metadata and included license notices help distributions document redistribution terms and organize their repositories. Maintainers make licensing decisions; the manager does not automatically establish legal compliance. Debian, for example, requires package license information in `/usr/share/doc/PACKAGE/copyright`.

References: [Ubuntu package administration](https://ubuntu.com/server/docs/how-to/software/package-management/), [Debian package management](https://www.debian.org/doc/manuals/debian-reference/ch02.html), [Debian license documentation policy](https://www.debian.org/doc/debian-policy/ch-docs.html#copyright-information).

### Manager scope and layout

| Tool | What it manages | Installation layout |
| --- | --- | --- |
| **Homebrew** | A **formula** defines URLs, checksums, dependencies, and build steps. A **bottle** is a prebuilt formula installation; a **cask** describes vendor-distributed software such as a macOS app. | Formula versions live in `Cellar/<name>/<version>`, with selected files linked into the prefix: usually `/opt/homebrew` on Apple Silicon or `/usr/local` on Intel macOS. Casks use `Caskroom` and destinations such as `/Applications`. |
| **APT / dpkg** | APT chooses and downloads Debian packages and dependencies. `dpkg` installs `.deb` files and tracks state; it does not fetch missing dependencies itself. | Shared OS directories such as `/usr/bin`, `/usr/lib`, and `/etc`; records under `/var/lib/dpkg`. |
| **pip** | Python distributions: installs compatible wheels or builds wheels from source distributions. | The selected Python environment's `site-packages`, with command wrappers in its scripts directory (`bin` on macOS/Linux). |
| **npm** | JavaScript ecosystem packages and their dependency tree, described by `package.json`. | Usually project-local `node_modules`, with commands in `node_modules/.bin`; global installs use a configured prefix. |

**System-level managers** coordinate software across an OS or shared prefix. **Language-specific managers** coordinate packages for a language runtime, often per project. The boundary is their scope, not whether they use administrator privileges: npm's global mode remains language-specific. pip generally cannot supply missing OS libraries required by a native extension.

References: [Homebrew](https://docs.brew.sh/Manpage), [pip](https://pip.pypa.io/en/stable/cli/pip_install/), [npm](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/).

## 4. Installation lifecycle

The common sequence is **discover → resolve dependencies → download and verify → build if needed → install files → record state**. Resolution and downloading can interleave.

| Command | What happens internally | Result |
| --- | --- | --- |
| `brew install wget` | Reads formula metadata, checks installed dependencies, selects a compatible bottle or builds from source, and verifies declared checksums. Installs a versioned keg and records a receipt. | Links exposed files into Homebrew's prefix. The shell finds `wget` when that prefix's `bin` is on `PATH`. Keg-only formulae are not linked there. |
| `sudo apt install curl` | Uses cached repository indexes to select compatible versions, downloads `.deb` files, and verifies hashes through signed repository metadata. `dpkg` unpacks/configures packages and runs scripts. `apt update` refreshes indexes separately. | Records package/file ownership and normally installs `/usr/bin/curl`, already on typical `PATH` settings. Root privileges allow writes to OS directories. |
| `pip install requests` | Queries the configured index, normally PyPI, resolves Python requirements, and downloads wheels or builds them from source, normally with isolated build dependencies. Uses HTTPS and supplied artifact hashes. | Installs modules and `.dist-info` records in the chosen Python environment. Requests is an importable library, so no `requests` command appears. Packages declaring command entry points get wrappers. |

Use `python -m pip` to select the interpreter explicitly. Installing a command makes it available through `PATH`; installing a library makes it available through the relevant loader or import mechanism.

Verification differs by ecosystem: APT authenticates repository metadata rather than requiring a signature on every `.deb`; pip's `--require-hashes` checks explicitly supplied hashes. Verification establishes integrity within that trust model, not harmlessness. Builds and installation scripts can execute code. [Homebrew bottles](https://docs.brew.sh/Bottles), [APT authentication](https://manpages.debian.org/testing/apt/apt-secure.8.en.html), [pip hash checking](https://pip.pypa.io/en/stable/topics/secure-installs/).

## 5. Dependencies and version management

### Dependency graphs and conflicts

Suppose an application uses an HTTP library, which uses a certificate-data package:

```text
Application → HTTP library → certificate data
```

The HTTP library is a **direct dependency** of the application; certificate data is a **transitive dependency**, needed through the library. The manager follows these declarations recursively and chooses versions satisfying the whole graph.

Software has two sets of requirements: **build dependencies**, used by developers or build systems to produce it, and **runtime dependencies**, needed to actually run it. These sets can overlap, but they are not necessarily the same: a compiler is usually needed only during the build, while a shared library must be available at runtime. A statically linked library contributes code during the build without requiring its library file at runtime.

A constraint such as `>=2,<3` allows versions from 2 up to, but excluding, 3. If two packages require `C<2` and `C>=2`, one C version cannot satisfy both. pip generally allows one installed version per distribution in an environment; npm can often place different versions in separate branches of `node_modules`, although peer dependencies add constraints. OS managers must coordinate versions sharing system paths.

### Reproducibility and isolation

A manifest declares acceptable dependencies; a **lockfile** records the versions and artifacts selected for a resolved graph. npm's `package-lock.json` supports `npm ci`, which installs the locked tree and rejects disagreement with `package.json`. Reproducing an installation also requires compatible runtimes/platforms and available artifacts. `pip freeze` records installed versions but lacks artifact hashes and a complete description of build inputs. [npm lockfiles](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/), [npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci/).

**Isolated environments**, such as Python virtual environments and project-local npm trees, let projects use different dependency versions. A venv separates Python installations; it does not isolate the OS or sandbox code.

### Updates and removal

Managers track installed state using databases, receipts, file lists, or dependency trees. dpkg records package ownership; Homebrew keeps versioned kegs and receipts; pip uses `.dist-info/RECORD`; npm uses its installed tree and project records.

An update selects newer allowed versions and replaces files or switches links. Uninstall removes tracked files, but generated data and some configuration may remain. Removing a package does not always remove dependencies: pip leaves them installed, while other managers offer separate cleanup operations. macOS Installer receipts describe installations but do not provide a universal uninstaller.

## Connections

- [[Software build process]] — produces artifacts for distribution.
- [[Ahead-of-time compilation (AOT)]] — explains linking executables and libraries.
- [[Software deployment process]] — installation can prepare a system for execution.
- [[Linux-based operating systems]] — distributions coordinate packages into a usable OS.
- [[Terminals, shells, and command-line interfaces]] — explains command discovery and execution.
