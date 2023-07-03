## Overview

The goal of this project is to enable a minimal framework for fast, secure, and reliable dependency & build management for OpenCore EFIs. OCE-Build is designed to help enable projects to be highly composable and easily maintainable, prioritizing a small and git-friendly footprint.

While this project is primarily intended to be used for unsupported Macs using [OpenCore Legacy Patcher (OCLP)](https://github.com/dortania/OpenCore-Legacy-Patcher) or for PC Hackintosh projects using [OpenCore](https://github.com/acidanthera/OpenCorePkg), other projects (including Virtual Machines) that use OpenCore are supported.

### Key Features
- **Declarative Configuration**
  - [x] Minimal project configuration
  - [x] Flexible support for any project structure
  - [ ] Shared/Template configurations
    - [ ] Support for overriding build pipeline inclusions/exclusions
    - [ ] Inheritance resolution for extending config.plist configurations.
  - [ ] Automated config.plist schema conflict resolution
    - [ ] Diff file creation between two PLIST files
    - [x] Support for reading declarative config.{yml|yaml} files.
- **Version Management**
  - [ ] Versioning for OpenCore binaries and resources
    - [ ] Versioning for bundled driver and tool binaries
    - [x] Versioning for supplemental OCBinaryData binaries
  - [x] Versioning for local & external Kext sources
    - [x] Fetch external Kext sources by release version or commit
    - [x] Kext dependency sorting for proper prelink injection
  - [ ] Versioning for local & external SSDT binaries
    - [ ] Versioning for pre-built SSDT files
    - [x] SSDT dependency sorting for proper ACPI table loading
  - [ ] Lockfile creation for intelligent registry management
- **Build Support**
  - [ ] Incremental builds and cache management from lockfile.
    - [ ] Support for remote cache artifacts
  - [ ] Advanced ACPI language support
    - [x] Support for building DSL source into compiled AML
    - [ ] Compiler options with external refs and patchfiles
  - [ ] CI support for managing and building Kexts with XCode

## Development

#### Installing Poetry

Install the poetry package manager:
```shell
bash scripts/install-poetry.sh
```

Setup the poetry environment and project dependencies:
```shell
bash scripts/setup-poetry.sh
```

## License
[BSD 3-Clause License](https://github.com/Qonfused/OCE-Build/blob/main/LICENSE).
