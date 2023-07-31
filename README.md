<h1 align="center">OCE Build</h1>
<p align="center">
  <!-- <img
    src=""
    alt=""
    class="center"
    width=500px
  ><br> -->
  A minimal framework for fast, secure, and reliable build and dependency management for <a href="https://github.com/acidanthera/OpenCorePkg">OpenCore</a> EFIs.
</p>

<div align="center">

  <!-- TODO: Add PyPI badges for supported Python versions, etc -->
  <a href="/LICENSE">![License](https://img.shields.io/badge/⚖_License-BSD_3_Clause-lightblue?labelColor=3f4551)</a>
  <a href="/CHANGELOG.md">![SemVer](https://img.shields.io/badge/dynamic/yaml?label=SemVer&logo=SemVer&labelColor=3f4551&color=f48042&prefix=v&query=$.version&url=https://raw.githubusercontent.com/Qonfused/OCE-Build/main/ci/registry/project.json)</a>
  <a href="https://github.com/acidanthera/OpenCorePkg/releases">![OpenCore](https://img.shields.io/badge/dynamic/yaml?label=OpenCore&logo=Osano&logoColor=0298e1&labelColor=3f4451&prefix=v&query=$.version&url=https://raw.githubusercontent.com/Qonfused/OCE-Build/main/ci/registry/schema.json)</a>
  <a href="https://github.com/Qonfused/OCE-Build/actions/workflows/ci:python.yml">![CI:Python](https://github.com/Qonfused/OCE-Build/actions/workflows/ci:python.yml/badge.svg?branch=main)</a>

</div>

OCE-Build is designed to help enable projects to be highly composable and easily maintainable, prioritizing a small and git-friendly footprint.

### Key Features

- **Declarative Configuration**
  - [x] Minimal project configuration
  - [x] Flexible support for any project structure
  - [ ] Shared/Template configurations
    - [x] Support for overriding build pipeline inclusions/exclusions
    - [ ] Inheritance resolution for extending config.plist configurations.
  - [ ] Automated config.plist schema conflict resolution
    - [ ] Diff file creation between two PLIST files
    - [x] Support for reading declarative config.{yml|yaml} files.
    - [x] Support for reading and converting existing config.plist files.
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
  - [x] Lockfile creation for intelligent registry management
- **Build Support**
  - [x] Incremental builds and cache management from lockfile.
    - [ ] Support for remote cache artifacts
  - [x] Advanced ACPI language support
    - [x] Support for building DSL source into compiled AML
    - [ ] Compiler options with external refs and patchfiles
  - [ ] CI support for managing and building Kexts with XCode

## Installation

This project is distributed as both a standalone executable and a Python library on PyPI. The standalone executable is intended to be used for simple projects or for CI/CD, while the Python library is intended to be used for supporting library development or complex build pipelines.

See the [install](/docs/install.md) documentation for more information on how to
install OCE Build as an executable or as a Python library.

## Getting Started

>TODO

## Contributing

See the [contributing](/CONTRIBUTING.md) documentation for more information on how to contribute to this project.

## Issues

>TODO

## License

[BSD 3-Clause License](/LICENSE).
