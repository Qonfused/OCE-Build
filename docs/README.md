## Overview

The goal of this project is to enable a minimal framework for fast, secure, and reliable dependency & build management for OpenCore EFIs. OCE-Build is designed to make projects highly composable and easily mainainable, prioritizing a small footprint in a git-friendly manner.

While this project is primarily intended to be used for unsupported Macs using [OpenCore Legacy Patcher (OCLP)](https://github.com/dortania/OpenCore-Legacy-Patcher) or for PC Hackintosh projects using [OpenCore](https://github.com/acidanthera/OpenCorePkg), other projects (including Virtual Machines) that use OpenCore are supported.

### Key Features
- **Declarative Configuration**
  - [x] Minimal project configuration
  - [x] Flexible support for any project structure
  - [ ] Shared/Template configurations
    - [ ] Inheritance resolution for overriding inclusions/exclusions
  - [ ] CI support for managing and building Kexts with XCode
- **Version Management**
  - [x] Versioning for local & external Kext sources
    - [x] Fetch external Kext sources by release version or commit
  - [ ] Automated config.plist schema conflict resolution
  - [x] Lockfile creation for intelligent registry management
- **Incremental Builds**
  - [ ] Advanced ACPI language support
    - [x] Support for building DSL source into compiled AML
    - [ ] Compile options with external refs and patches

## Development

#### Installing Poetry

Windows users:
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

macOS, Linux (including WSL2):
```shell
curl -sSL https://install.python-poetry.org | python3 -
```

Setup the poetry environment and dependencies:
```shell
bash scripts/poetry.sh
```

## License
[BSD 3-Clause License](https://github.com/Qonfused/OCE-Build/blob/main/LICENSE).