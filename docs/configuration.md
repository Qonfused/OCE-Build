# Build Configuration

A build configuration is a [YAML](https://yaml.org/) file that specifies the packages to include in a build. The build configuration is given as a `build.yml` file in the root of the project directory. The build configuration is used to specify the OpenCore version and packages to include in a build.

The term `packages` is used to denote specific plugins, kexts, drivers, and tools. The term `entries` is used to denote a package entry in the build configuration.

Refer to [`example/build.yml`](`/docs/example/build.yml`) for an example build configuration. Additional examples are provided for reference within this document.

## OpenCore configuration

In a `build.yml` file, the OpenCore build and version can optionally be specified using YAML frontmatter with the below properties:

- The `oc-build` property can be either `RELEASE` or `DEBUG` (defaults to `RELEASE`).
- The `oc-version` property is a [version specifier](#version-specifiers) (covered later in this document).

For example, the below configuration specifies the latest debug build of OpenCore:

```yaml
---
oc-version: latest
oc-build: DEBUG
---
```

This build configuration is optional and defaults to the latest release build of OpenCore. It is however recommended to specify this build configuration to ensure that builds are reproducible.

## Package entries

Packages in a `build.yml` file are grouped into the following categories:

- **ACPI**: ACPI SSDTs (e.g. `SSDT-EC.dsl` or `SSDT-PLUG.aml`)
- **Drivers**: UEFI drivers (e.g. `OpenRuntime.efi` or `HfsPlus.efi`)
- **Kexts**: Kernel extensions (e.g. `Lilu.kext` or `VirtualSMC.kext`)
- **Tools**: UEFI tools (e.g. `OpenShell.efi` or `VerifyMsrE2.efi`)

These entry categories correspond to the directories in the `EFI/OC` directory of the OpenCore EFI tree. Package entries are specified under their appropriate category name under a root entry category (`<category>:`). Each package entry can be specified as either a string (in a list) or as an object property.

For example, the below configuration specifies the `Lilu` and `VirtualSMC` kexts as string properties within a `Kexts` object entry:

```yaml
Kexts:
  Lilu: latest
  VirtualSMC: "latest"
```

Additionally, you can specify tools bundled with OpenCore in a list entry for brevity:

```yaml
Tools:
  - OpenShell
  - ControlMsrE2
  - VerifyMsrE2
```

Note that these entries do not include any file extensions. The file extension is automatically inferred based on the package type.

### Specifiers

A specifier is a string that identifies a particular version or location of a package. Specifiers are used to enable reproducible builds by ensuring that the same or acceptable version of a package is used across different builds. Specifiers are also used to identify the location of a package when it is not available in the local registry or filesystem.

By default, specifiers are interpreted as the string value of an entry in a `build.yml` file. They can also be provided with the `specifier` property explicitly when using an object entry.

For example, the below entries are equivalent:

- String value:

  ```yaml
  Kexts:
    Lilu: "^1.5.0"
  ```

- Object entry:

  ```yaml
  Kexts:
    Lilu:
      specifier: "^1.5.0"
  ```

#### Version specifiers

A version specifier is a version number or string that identifies a particular version of a package (e.g. `1.0.2` or `1.0.2-alpha.1`). By default, the latest version of a package that satisfies the version number is used. If a specific version is given, that version is used.

Version numbers support most common formats and are not case-sensitive. For example, `1.0.0`, `1.0.0-alpha.1`, `1.0.0-alpha-1`, and `v1.0.0-Alpha-1` are all valid version numbers. Additionally, version strings can be given (i.e. `latest` or `oldest`) to match the latest or oldest version of a package.

Semantic versioning is used to evaluate version numbers against remote registries (e.g. GitHub or Dortania). Refer to https://semver.org/ for more information about semantic versioning.

- Version numbers can include semver operators like `^` or `~` (e.g. `^1.2.0`, `~1.0.0`) to match up to a specific major/minor/patch version. This follows similar operator semantics to npm. Refer to https://docs.npmjs.com/about-semantic-versioning for more information about semver operators.
- Version numbers can also include comparison operators (e.g. `>`, `>=`, `<`, `<=`, `==`) to specify a range of versions to match.

#### GitHub specifiers

A GitHub specifier is a string that identifies a particular GitHub repository, branch, commit, and/or release tag (e.g. `acidanthera/OpenCorePkg=latest`).

The specifier can be given in the format `<owner>/<repo>` with additional optional parameters:

- To match a specific release tag: `owner/repo=<tag>` or `owner/repo#tag=<tag>`.
  - Tags can be given as a version number (e.g. `1.0.0`) or a version string (e.g. `latest`), following the same rules as version specifiers.
- To match a specific remote or branch: `owner/repo#<branch>` or `owner/repo#branch=<branch>`.
- To match a specific commit: `owner/repo#<commit>` or `owner/repo#commit=<commit>`.
- To match the latest successful run of a specific GitHub Actions workflow: `owner/repo#<workflow>` or `owner/repo#workflow=<workflow>`.

The above formats can also be given when using object entries:

- `tag:<tag>`, `head:<head>`, `workflow:<workflow`, or `commit:<commit>`.

For example:
```yaml
Kexts:
  AsusSMC: Qonfused/AsusSMC=latest
```

Note that a GitHub repository slug **must** be provided to identify non-acidanthera packages (e.g. `OpenIntelWireless/itlwm`). If no repository slug is given, the package is instead searched for in the Dortania registry (assumes `acidanthera/<name>`). Refer to https://dortania.github.io/builds for a list of available builds.

#### File specifiers

A file specifier is a path or file uri that points to a local directory or file (e.g. `../foo/bar.kext` or `file:./foo/bar.efi`). A local path can be absolute or relative to the directory in which the file resides. Additionally, relative filepaths are resolved relative to the location of the `build.yml` file.

File URIs (as given by [RFC 8089](https://datatracker.ietf.org/doc/html/rfc8089)) can start with either `file:` or `file://` and terminate with either a relative or absolute filepath, respectively.

If a filepath does not exist, it is treated as a remote repository slug. Note that filepaths must point to the filepath of a package and not the directory containing it.

#### Wildcard specifiers

A wildcard specifier (`*`) matches any package or binary bundled with OpenCore or in the local registry. This is also the default behavior if no specifier is provided.

### Properties

Packages under the appropriate `ACPI`, `Drivers`, `Kexts`, `Tools`, or `Drivers` entries can be configured with additional properties. Note that these properties are only available when using object entries (i.e. when using the `specifier` property).

#### Bundle properties

Bundles included in packages can be specified using the `bundled` property (list). For example, to whitelist plugins bundled with `VoodooI2C.kext`:

```yaml
Kexts:
  VoodooI2C:
    specifier: VoodooI2C/VoodooI2C=latest
    bundled:
      - VoodooI2CServices
      - VoodooGPIO
      - VoodooInput
```

#### Schema properties

Schema properties correspond to properties under their respective config.plist schema. Refer to the below documentation for more information about these properties for each entry type:

- ACPI: [`ACPI > Add`](https://dortania.github.io/docs/latest/Configuration.html#add-properties)
- Drivers: [`UEFI > Drivers`](https://dortania.github.io/docs/latest/Configuration.html#drivers-properties)
- Kexts: [`Kernel > Add`](https://dortania.github.io/docs/latest/Configuration.html#add-properties1)
- Tools: [`Misc > Tools`](https://dortania.github.io/docs/latest/Configuration.html#entry-properties)

Properties such as the `Path` (including `BundlePath`, `PlistPath`, `ExecutablePath`, etc.) are automatically inferred from the package contents. All properties (such as `Comment` or `Enabled`) can be manually specified to override the default or failsafe values. Note that all entries are enabled by default and must be disabled explicitly.

For example, to add `MinKernel` and `MaxKernel` properties to the `AirportItlwm` kexts:

```yaml
Kexts:
  # Intel Wi-Fi Adapter Kernel Extensions for macOS, based on the OpenBSD Project.
  AirportItlwm-Ventura:
    specifier: OpenIntelWireless/itlwm=^2.2.0
    properties:
      Comment: "Intel Wi-Fi driver for macOS Ventura"
      MaxKernel: "22.99.99"
      MinKernel: "22.0.0"
  AirportItlwm-Monterey:
    specifier: OpenIntelWireless/itlwm=^2.1.0
    properties:
      Comment: "Intel Wi-Fi driver for macOS Monterey"
      MaxKernel: "21.99.99"
      MinKernel: "21.0.0"
  AirportItlwm-BigSur:
    specifier: OpenIntelWireless/itlwm=^2.1.0
    properties:
      Comment: "Intel Wi-Fi driver for macOS Big Sur"
      MaxKernel: "20.99.99"
      MinKernel: "20.0.0"
```

For example, to add the `ResetNvram.efi` driver with the `--preserve-boot` argument (appended):

```yaml
Drivers:
  # OpenCore plugin implementing OC_BOOT_ENTRY_PROTOCOL to add a configurable
  # 'Reset NVRAM entry' to the boot picker menu.
  ResetNvramEntry:
    specifier: "*" # This plugin is bundled with OpenCore
    properties:
      @append(" ") # (Optional) This macro appends to any pre-existing arguments
      Arguments: "--preserve-boot"
```

# Config.plist Configuration

> **TODO**
