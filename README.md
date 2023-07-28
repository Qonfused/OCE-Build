## Overview

The goal of this project is to enable a minimal framework for fast, secure, and reliable dependency & build management for OpenCore EFIs. OCE-Build is designed to help enable projects to be highly composable and easily maintainable, prioritizing a small and git-friendly footprint.

This project is distributed as both a standalone executable and a Python library on PyPI. The standalone executable is intended to be used for CI/CD or project build pipelines, while the Python library is intended to be used for supporting library development.

While this project is primarily intended to be used for PC Hackintosh projects using [OpenCore](https://github.com/acidanthera/OpenCorePkg) or unsupported Macs using [OpenCore Legacy Patcher (OCLP)](https://github.com/dortania/OpenCore-Legacy-Patcher), other projects (including Virtual Machines) that use OpenCore are supported.

### Key Features
- **Declarative Configuration**
  - [x] Minimal project configuration
  - [x] Flexible support for any project structure
  - [ ] Shared/Template configurations
    - [x] Support for overriding build pipeline inclusions/exclusions
    - [ ] Inheritance resolution for extending config.plist configurations.
  - [x] Automated config.plist schema conflict resolution
    - [ ] Diff file creation between two PLIST files
    - [x] Support for reading declarative config.{yml|yaml} files.
- **Version Management**
  - [x] Versioning for OpenCore binaries and resources
    - [x] Versioning for bundled driver and tool binaries
    - [x] Versioning for supplemental OCBinaryData binaries
  - [x] Versioning for local & external Kext sources
    - [x] Fetch external Kext sources by release version or commit
    - [x] Kext dependency sorting for proper prelink injection
  - [x] Versioning for local & external SSDT binaries
    - [x] Versioning for pre-built SSDT files
    - [x] SSDT dependency sorting for proper ACPI table loading
  - [ ] Lockfile creation for intelligent registry management
- **Build Support**
  - [ ] Incremental builds and cache management from lockfile.
    - [x] Support for remote cache artifacts
  - [ ] Advanced ACPI language support
    - [x] Support for building DSL source into compiled AML
    - [ ] Compiler options with external refs and patchfiles
  - [ ] CI support for managing and building Kexts with XCode

## Installation

See the [install](/docs/install.md) documentation for more information on how to
install OCE Build as an executable or as a Python library.

## Getting Started

>TODO

## Contributing

See the [contributing](/docs/contributing.md) documentation for more information on how to contribute to this project.

## Development

Development of this project is done using [Poetry](https://python-poetry.org/). Poetry is a Python package manager that provides a virtual environment for managing dependencies and project configuration. Poetry is required to be installed on your system to develop and build this project.

### Poetry

It's recommended to use at least version `1.5.0` of Poetry to ensure compatibility with this project.

To install Poetry, you can either use the [official installation instructions](https://python-poetry.org/docs/#installation) or use the provided script to install Poetry in your home directory:
```shell
bash scripts/install-poetry.sh
```

To upgrade Poetry from a previous version, you can run `poetry self update` to fetch the latest version, or run `poetry self update 1.5.0` to update to the project's recommended version.

To setup the poetry environment and install project dependencies, run the below command:
```shell
bash scripts/setup-poetry.sh
```

### Project Scripts

This project uses a custom set of scripts to help manage the development and build process. These scripts are located in the **ci/scripts** directory. These scripts are intended to be run through the [**poethepoet**](https://github.com/nat-n/poethepoet) plugin, which is installed as part of the `setup-poetry.sh` script.

To list all available scripts, run `poetry run poe`. Run a script using `poetry <script>` or `poetry run poe <script>`.

Note that scripts listed in the **ci/scripts** directory must be prefixed with `poetry run poe <command>`, while scripts listed in the [**pyproject.toml**](/pyproject.toml) file can also be run through `poetry <command>`.

For example, to run the **test** script, simply run `poetry test` or `poetry run poe test`. Only the latter option is available for CI scripts to avoid namespace pollution of Poetry commands.

It's recommended to run the **resolve-modules** and **sort-imports** CI scripts before commiting; these scripts will ensure that all module namespaces can properly be resolved and that all imports are sorted correctly. These scripts will run automatically on the pre-commit git hook, but can be run manually by running `poetry run poe resolve-modules` and `poetry run poe sort-imports`.

## License
[BSD 3-Clause License](https://github.com/Qonfused/OCE-Build/blob/main/LICENSE).
