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
  <a href="https://github.com/Qonfused/OCE-Build/actions/workflows/ci-python.yml">![Python CI](https://github.com/Qonfused/OCE-Build/actions/workflows/ci-python.yml/badge.svg?branch=main)</a>

</div>

OCE-Build is designed to help enable projects to be highly composable and easily
maintainable, prioritizing a small git-friendly footprint. It is designed to be
flexible and extensible for existing projects, while also providing a simple
configuration and interface for new projects to get started quickly.

## Feature Overview

> **Note**: This project is still in early development and is not yet ready for general use.
The following is a list of features that are planned for the initial release.

- **Declarative Configuration**
  - Minimal project configuration.
  - Flexible support for any project structure.
  - Shared/Template config.plist configurations.
  - Automated config.plist schema conflict resolution.
- **Version Management**
  - Versioning for OpenCore binaries and resources (Kexts, SSDTs, etc).
  - Automatic version resolution for dependencies.
  - Lockfile creation for intelligent registry management.
- **Build Support**
  - Incremental builds and cache management from lockfile.
  - Advanced ACPI language support, including compiler and patchfile options.
  - Dependency sorting for proper prelink injection (i.e. SSDTs, Kexts).
  - CI support for managing and building Kexts with XCode.

## User Documentation

*This section is for users looking to integrate this tool with their own project.
For information on contributing to this project, refer to the
[Developer Docs](#developer-documentation)*

### Installation

This project is distributed as both a standalone CLI and a Python library on
PyPI. The CLI is intended to be used for simple projects or for CI/CD, while the
library is intended to be used for supporting Python library development or
complex build pipelines. The library also comes bundled with the CLI and it's
source code is available under the `ocebuild.cli` module.

The recommended way to install the CLI is from [GitHub releases](https://github.com/Qonfused/OCE-Build/releases). This will provide you with a standalone executable that can be used without installing Python or any other dependencies. The CLI is available for Windows, macOS, and Linux.

To install the CLI / library from PyPI, you will need to have Python 3.8 or
later installed. You can install Python from [python.org](https://www.python.org/downloads/)
or from your package manager. For more information on installing Python, refer
to the [Python documentation](https://docs.python.org/3/using/index.html).

To install the library directly from PyPI using `pip`, simply run the following
command in your terminal:
```sh
pip install ocebuild
```

Or when using the `poetry` package manager, run:
```sh
poetry add ocebuild
```

Depending on your system, you may need to use `pip3` instead of `pip` when
installing the library. You may also need to use `sudo` or `pip install --user`
to install the library globally or locally, respectively.

After installing the library, the CLI will also be available in your PATH, which
you can invoke by simply running `ocebuild` in your terminal (or `poetry run ocebuild`).

### Getting Started

To get started, you will need to create a `build.yml` file in the root of your
project. This file will contain all of the information needed to build your EFI.
You can follow along with the below example or reference one of the [example projects](https://github.com/Qonfused/OCE-Build/tree/main/examples) included in this repository.

The following is a minimal example of a `build.yml` file located under a `src/`
directory:

```yaml
# src/build.yml
---
build: DEBUG
version: latest
---
ACPI:
Drivers:
  - AudioDxe
  - HfsPlus
  - OpenRuntime
  - ResetNvramEntry
Kexts:
  Lilu: latest
  VirtualSMC: latest
Resources:
Tools:
  - OpenShell
```

Once you have created your `build.yml` file, you can run the build command to
build your EFI:

```sh
ocebuild build --cwd src/build.yml
```

This will create a new `dist/` directory in your project containing your EFI.
You can also specify a custom output directory by using the `-o` / `--output`
option. To view all available commands and options, run `ocebuild --help` or run
`ocebuild <command> --help` for more information on a specific command.

Refer to [docs/configuration.md](https://github.com/Qonfused/OCE-Build/blob/main/docs/configuration.md#build-configuration) for more information on how to setup your build
configuration.

Note that this does not output a config.plist file. To generate a config.plist
file, you will need to create a `config.yml` file in the same directory as your
`build.yml` file. The `config.yml` file contains only the changes you wish to
make to the default Sample.plist file (located under `dist/Docs/Sample.plist`).
Refer to [docs/configuration.md](https://github.com/Qonfused/OCE-Build/blob/main/docs/configuration.md#configplist-configuration) for more information.

## Developer Documentation

*This section is for developers looking to contribute to this project. This is
only meant to be a brief overview of the project structure and development
guidelines. For more information, refer to the [contributing](/CONTRIBUTING.md)
documentation.*

### Guidelines and Philosophy

The general philosophy for this project is to keep things as simple as possible.
This means that the project should be easy to understand, easy to maintain, and
easy to contribute to.

A summary of the contributing guidelines for this project are as follows:

- Create an [issue](https://github.com/Qonfused/OCE-Build/issues) for any major
  changes and enhancements that you wish to make.
  - If you find a security vulnerability, do NOT open an issue. Please refer to our [Security Policy](https://github.com/Qonfused/OCE-Build/security/policy) for reporting security vulnerabilities.
  - For questions or discussions related to this project, please open a new GitHub
  [discussion](https://github.com/Qonfused/OCE-Build/discussions) instead of
  opening an issue.
- Create a [pull request](https://github.com/Qonfused/OCE-Build/pulls) for your
  changes and coordinate with the project maintainers to get it merged to main.
  - Include unit tests when you contribute new features or fix a bug. This:
    - Proves that your code works correctly and prevents regressions from going
      unnoticed.
    - Guards against breaking changes to the public API and ensures that the
      project can remain backwards compatible.
    - Lowers the maintenance cost of the project by making it easier to
      troubleshoot and debug issues.
  - Keep compatibility and cohesiveness mind when contributing a change that
    will impact the public API. This helps limit the scope of changes to only
    what is required to implement the new feature or fix the bug.

## License

[BSD 3-Clause License](/LICENSE).
