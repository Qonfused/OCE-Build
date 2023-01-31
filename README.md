## Overview

The goal of this project is to enable a minimal framework for fast, secure, and reliable dependency & build management for OpenCore EFIs. OC-Build is designed to make projects highly composable and easily mainainable in a git-friendly manner.

While this project is primarily intended to be used for unsupported Macs using [OpenCore Legacy Patcher (OCLP)](https://github.com/dortania/OpenCore-Legacy-Patcher) or for PC Hackintosh projects using [OpenCore](https://github.com/acidanthera/OpenCorePkg), other projects (including Virtual Machines) are supported.

### Key Features
- **Declarative Configuration**
  - [x] Minimal project configuration
  - [x] Flexible support for any project structure
  - [ ] Inheritance resolution for template configurations
- **Version Management**
  - [x] Versioning for local & external Kext sources
  - [ ] Automated config.plist schema conflict resolution
  - [ ] Lockfile creation for intelligent registry management
- **Incremental Builds**
  - [x] Support for building ACPI DSL source into compiled AML
  - [ ] Advanced ACPI feature support for external refs and patches
  - [ ] CI support for managing and building Kexts with XCode

## License
[BSD 3-Clause License](https://github.com/Qonfused/OC-Build/blob/main/LICENSE).