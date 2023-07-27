<h1 id=schema>OpenCore Config.plist Schema - v0.9.3</h1>

#### Last Updated: `2023-07-27 18:41:04.900010+00:00`

#### Revision: `{ SHA1: d52fc46ba650ce1afe00c354331a0657a533ef18 }`

<h2 id=table-of-contents>Table of Contents</h2>

<details><summary>Click to Expand</summary>

- [ACPI -> Add](#acpi-add)
  - [ACPI -> Add[] -> Comment](#acpi-add-comment)
  - [ACPI -> Add[] -> Enabled](#acpi-add-enabled)
  - [ACPI -> Add[] -> Path](#acpi-add-path)
- [ACPI -> Delete](#acpi-delete)
  - [ACPI -> Delete[] -> All](#acpi-delete-all)
  - [ACPI -> Delete[] -> Comment](#acpi-delete-comment)
  - [ACPI -> Delete[] -> Enabled](#acpi-delete-enabled)
  - [ACPI -> Delete[] -> OemTableId](#acpi-delete-oemtableid)
  - [ACPI -> Delete[] -> TableLength](#acpi-delete-tablelength)
  - [ACPI -> Delete[] -> TableSignature](#acpi-delete-tablesignature)
- [ACPI -> Patch](#acpi-patch)
  - [ACPI -> Patch[] -> Base](#acpi-patch-base)
  - [ACPI -> Patch[] -> BaseSkip](#acpi-patch-baseskip)
  - [ACPI -> Patch[] -> Comment](#acpi-patch-comment)
  - [ACPI -> Patch[] -> Count](#acpi-patch-count)
  - [ACPI -> Patch[] -> Enabled](#acpi-patch-enabled)
  - [ACPI -> Patch[] -> Find](#acpi-patch-find)
  - [ACPI -> Patch[] -> Limit](#acpi-patch-limit)
  - [ACPI -> Patch[] -> Mask](#acpi-patch-mask)
  - [ACPI -> Patch[] -> OemTableId](#acpi-patch-oemtableid)
  - [ACPI -> Patch[] -> Replace](#acpi-patch-replace)
  - [ACPI -> Patch[] -> ReplaceMask](#acpi-patch-replacemask)
  - [ACPI -> Patch[] -> Skip](#acpi-patch-skip)
  - [ACPI -> Patch[] -> TableLength](#acpi-patch-tablelength)
  - [ACPI -> Patch[] -> TableSignature](#acpi-patch-tablesignature)
- [ACPI -> Quirks](#acpi-quirks)
  - [ACPI -> Quirks -> FadtEnableReset](#acpi-quirks-fadtenablereset)
  - [ACPI -> Quirks -> NormalizeHeaders](#acpi-quirks-normalizeheaders)
  - [ACPI -> Quirks -> RebaseRegions](#acpi-quirks-rebaseregions)
  - [ACPI -> Quirks -> ResetHwSig](#acpi-quirks-resethwsig)
  - [ACPI -> Quirks -> ResetLogoStatus](#acpi-quirks-resetlogostatus)
  - [ACPI -> Quirks -> SyncTableIds](#acpi-quirks-synctableids)
- [Booter -> MmioWhitelist](#booter-mmiowhitelist)
  - [Booter -> MmioWhitelist[] -> Address](#booter-mmiowhitelist-address)
  - [Booter -> MmioWhitelist[] -> Comment](#booter-mmiowhitelist-comment)
  - [Booter -> MmioWhitelist[] -> Enabled](#booter-mmiowhitelist-enabled)
- [Booter -> Patch](#booter-patch)
  - [Booter -> Patch[] -> Arch](#booter-patch-arch)
  - [Booter -> Patch[] -> Comment](#booter-patch-comment)
  - [Booter -> Patch[] -> Count](#booter-patch-count)
  - [Booter -> Patch[] -> Enabled](#booter-patch-enabled)
  - [Booter -> Patch[] -> Find](#booter-patch-find)
  - [Booter -> Patch[] -> Identifier](#booter-patch-identifier)
  - [Booter -> Patch[] -> Limit](#booter-patch-limit)
  - [Booter -> Patch[] -> Mask](#booter-patch-mask)
  - [Booter -> Patch[] -> Replace](#booter-patch-replace)
  - [Booter -> Patch[] -> ReplaceMask](#booter-patch-replacemask)
  - [Booter -> Patch[] -> Skip](#booter-patch-skip)
- [Booter -> Quirks](#booter-quirks)
  - [Booter -> Quirks -> AllowRelocationBlock](#booter-quirks-allowrelocationblock)
  - [Booter -> Quirks -> AvoidRuntimeDefrag](#booter-quirks-avoidruntimedefrag)
  - [Booter -> Quirks -> DevirtualiseMmio](#booter-quirks-devirtualisemmio)
  - [Booter -> Quirks -> DisableSingleUser](#booter-quirks-disablesingleuser)
  - [Booter -> Quirks -> DisableVariableWrite](#booter-quirks-disablevariablewrite)
  - [Booter -> Quirks -> DiscardHibernateMap](#booter-quirks-discardhibernatemap)
  - [Booter -> Quirks -> EnableSafeModeSlide](#booter-quirks-enablesafemodeslide)
  - [Booter -> Quirks -> EnableWriteUnprotector](#booter-quirks-enablewriteunprotector)
  - [Booter -> Quirks -> ForceBooterSignature](#booter-quirks-forcebootersignature)
  - [Booter -> Quirks -> ForceExitBootServices](#booter-quirks-forceexitbootservices)
  - [Booter -> Quirks -> ProtectMemoryRegions](#booter-quirks-protectmemoryregions)
  - [Booter -> Quirks -> ProtectSecureBoot](#booter-quirks-protectsecureboot)
  - [Booter -> Quirks -> ProtectUefiServices](#booter-quirks-protectuefiservices)
  - [Booter -> Quirks -> ProvideCustomSlide](#booter-quirks-providecustomslide)
  - [Booter -> Quirks -> ProvideMaxSlide](#booter-quirks-providemaxslide)
  - [Booter -> Quirks -> RebuildAppleMemoryMap](#booter-quirks-rebuildapplememorymap)
  - [Booter -> Quirks -> ResizeAppleGpuBars](#booter-quirks-resizeapplegpubars)
  - [Booter -> Quirks -> SetupVirtualMap](#booter-quirks-setupvirtualmap)
  - [Booter -> Quirks -> SignalAppleOS](#booter-quirks-signalappleos)
  - [Booter -> Quirks -> SyncRuntimePermissions](#booter-quirks-syncruntimepermissions)
- [DeviceProperties -> Add](#deviceproperties-add)
- [DeviceProperties -> Delete](#deviceproperties-delete)
- [Kernel -> Add](#kernel-add)
  - [Kernel -> Add[] -> Arch](#kernel-add-arch)
  - [Kernel -> Add[] -> BundlePath](#kernel-add-bundlepath)
  - [Kernel -> Add[] -> Comment](#kernel-add-comment)
  - [Kernel -> Add[] -> Enabled](#kernel-add-enabled)
  - [Kernel -> Add[] -> ExecutablePath](#kernel-add-executablepath)
  - [Kernel -> Add[] -> MaxKernel](#kernel-add-maxkernel)
  - [Kernel -> Add[] -> MinKernel](#kernel-add-minkernel)
  - [Kernel -> Add[] -> PlistPath](#kernel-add-plistpath)
- [Kernel -> Block](#kernel-block)
  - [Kernel -> Block[] -> Arch](#kernel-block-arch)
  - [Kernel -> Block[] -> Comment](#kernel-block-comment)
  - [Kernel -> Block[] -> Enabled](#kernel-block-enabled)
  - [Kernel -> Block[] -> Identifier](#kernel-block-identifier)
  - [Kernel -> Block[] -> MaxKernel](#kernel-block-maxkernel)
  - [Kernel -> Block[] -> MinKernel](#kernel-block-minkernel)
  - [Kernel -> Block[] -> Strategy](#kernel-block-strategy)
- [Kernel -> Emulate](#kernel-emulate)
  - [Kernel -> Emulate -> Cpuid1Data](#kernel-emulate-cpuid1data)
  - [Kernel -> Emulate -> Cpuid1Mask](#kernel-emulate-cpuid1mask)
  - [Kernel -> Emulate -> DummyPowerManagement](#kernel-emulate-dummypowermanagement)
  - [Kernel -> Emulate -> MaxKernel](#kernel-emulate-maxkernel)
  - [Kernel -> Emulate -> MinKernel](#kernel-emulate-minkernel)
- [Kernel -> Force](#kernel-force)
  - [Kernel -> Force[] -> Arch](#kernel-force-arch)
  - [Kernel -> Force[] -> BundlePath](#kernel-force-bundlepath)
  - [Kernel -> Force[] -> Comment](#kernel-force-comment)
  - [Kernel -> Force[] -> Enabled](#kernel-force-enabled)
  - [Kernel -> Force[] -> ExecutablePath](#kernel-force-executablepath)
  - [Kernel -> Force[] -> Identifier](#kernel-force-identifier)
  - [Kernel -> Force[] -> MaxKernel](#kernel-force-maxkernel)
  - [Kernel -> Force[] -> MinKernel](#kernel-force-minkernel)
  - [Kernel -> Force[] -> PlistPath](#kernel-force-plistpath)
- [Kernel -> Patch](#kernel-patch)
  - [Kernel -> Patch[] -> Arch](#kernel-patch-arch)
  - [Kernel -> Patch[] -> Base](#kernel-patch-base)
  - [Kernel -> Patch[] -> Comment](#kernel-patch-comment)
  - [Kernel -> Patch[] -> Count](#kernel-patch-count)
  - [Kernel -> Patch[] -> Enabled](#kernel-patch-enabled)
  - [Kernel -> Patch[] -> Find](#kernel-patch-find)
  - [Kernel -> Patch[] -> Identifier](#kernel-patch-identifier)
  - [Kernel -> Patch[] -> Limit](#kernel-patch-limit)
  - [Kernel -> Patch[] -> Mask](#kernel-patch-mask)
  - [Kernel -> Patch[] -> MaxKernel](#kernel-patch-maxkernel)
  - [Kernel -> Patch[] -> MinKernel](#kernel-patch-minkernel)
  - [Kernel -> Patch[] -> Replace](#kernel-patch-replace)
  - [Kernel -> Patch[] -> ReplaceMask](#kernel-patch-replacemask)
  - [Kernel -> Patch[] -> Skip](#kernel-patch-skip)
- [Kernel -> Quirks](#kernel-quirks)
  - [Kernel -> Quirks -> AppleCpuPmCfgLock](#kernel-quirks-applecpupmcfglock)
  - [Kernel -> Quirks -> AppleXcpmCfgLock](#kernel-quirks-applexcpmcfglock)
  - [Kernel -> Quirks -> AppleXcpmExtraMsrs](#kernel-quirks-applexcpmextramsrs)
  - [Kernel -> Quirks -> AppleXcpmForceBoost](#kernel-quirks-applexcpmforceboost)
  - [Kernel -> Quirks -> CustomPciSerialDevice](#kernel-quirks-custompciserialdevice)
  - [Kernel -> Quirks -> CustomSMBIOSGuid](#kernel-quirks-customsmbiosguid)
  - [Kernel -> Quirks -> DisableIoMapper](#kernel-quirks-disableiomapper)
  - [Kernel -> Quirks -> DisableIoMapperMapping](#kernel-quirks-disableiomappermapping)
  - [Kernel -> Quirks -> DisableLinkeditJettison](#kernel-quirks-disablelinkeditjettison)
  - [Kernel -> Quirks -> DisableRtcChecksum](#kernel-quirks-disablertcchecksum)
  - [Kernel -> Quirks -> ExtendBTFeatureFlags](#kernel-quirks-extendbtfeatureflags)
  - [Kernel -> Quirks -> ExternalDiskIcons](#kernel-quirks-externaldiskicons)
  - [Kernel -> Quirks -> ForceAquantiaEthernet](#kernel-quirks-forceaquantiaethernet)
  - [Kernel -> Quirks -> ForceSecureBootScheme](#kernel-quirks-forcesecurebootscheme)
  - [Kernel -> Quirks -> IncreasePciBarSize](#kernel-quirks-increasepcibarsize)
  - [Kernel -> Quirks -> LapicKernelPanic](#kernel-quirks-lapickernelpanic)
  - [Kernel -> Quirks -> LegacyCommpage](#kernel-quirks-legacycommpage)
  - [Kernel -> Quirks -> PanicNoKextDump](#kernel-quirks-panicnokextdump)
  - [Kernel -> Quirks -> PowerTimeoutKernelPanic](#kernel-quirks-powertimeoutkernelpanic)
  - [Kernel -> Quirks -> ProvideCurrentCpuInfo](#kernel-quirks-providecurrentcpuinfo)
  - [Kernel -> Quirks -> SetApfsTrimTimeout](#kernel-quirks-setapfstrimtimeout)
  - [Kernel -> Quirks -> ThirdPartyDrives](#kernel-quirks-thirdpartydrives)
  - [Kernel -> Quirks -> XhciPortLimit](#kernel-quirks-xhciportlimit)
- [Kernel -> Scheme](#kernel-scheme)
  - [Kernel -> Scheme -> CustomKernel](#kernel-scheme-customkernel)
  - [Kernel -> Scheme -> FuzzyMatch](#kernel-scheme-fuzzymatch)
  - [Kernel -> Scheme -> KernelArch](#kernel-scheme-kernelarch)
  - [Kernel -> Scheme -> KernelCache](#kernel-scheme-kernelcache)
- [Misc -> BlessOverride](#misc-blessoverride)
- [Misc -> Boot](#misc-boot)
  - [Misc -> Boot -> ConsoleAttributes](#misc-boot-consoleattributes)
  - [Misc -> Boot -> HibernateMode](#misc-boot-hibernatemode)
  - [Misc -> Boot -> HibernateSkipsPicker](#misc-boot-hibernateskipspicker)
  - [Misc -> Boot -> HideAuxiliary](#misc-boot-hideauxiliary)
  - [Misc -> Boot -> LauncherOption](#misc-boot-launcheroption)
  - [Misc -> Boot -> LauncherPath](#misc-boot-launcherpath)
  - [Misc -> Boot -> PickerAttributes](#misc-boot-pickerattributes)
  - [Misc -> Boot -> PickerAudioAssist](#misc-boot-pickeraudioassist)
  - [Misc -> Boot -> PickerMode](#misc-boot-pickermode)
  - [Misc -> Boot -> PickerVariant](#misc-boot-pickervariant)
  - [Misc -> Boot -> PollAppleHotKeys](#misc-boot-pollapplehotkeys)
  - [Misc -> Boot -> ShowPicker](#misc-boot-showpicker)
  - [Misc -> Boot -> TakeoffDelay](#misc-boot-takeoffdelay)
  - [Misc -> Boot -> Timeout](#misc-boot-timeout)
- [Misc -> Debug](#misc-debug)
  - [Misc -> Debug -> AppleDebug](#misc-debug-appledebug)
  - [Misc -> Debug -> ApplePanic](#misc-debug-applepanic)
  - [Misc -> Debug -> DisableWatchDog](#misc-debug-disablewatchdog)
  - [Misc -> Debug -> DisplayDelay](#misc-debug-displaydelay)
  - [Misc -> Debug -> DisplayLevel](#misc-debug-displaylevel)
  - [Misc -> Debug -> LogModules](#misc-debug-logmodules)
  - [Misc -> Debug -> SysReport](#misc-debug-sysreport)
  - [Misc -> Debug -> Target](#misc-debug-target)
- [Misc -> Entries](#misc-entries)
  - [Misc -> Entries[] -> Arguments](#misc-entries-arguments)
  - [Misc -> Entries[] -> Auxiliary](#misc-entries-auxiliary)
  - [Misc -> Entries[] -> Comment](#misc-entries-comment)
  - [Misc -> Entries[] -> Enabled](#misc-entries-enabled)
  - [Misc -> Entries[] -> Flavour](#misc-entries-flavour)
  - [Misc -> Entries[] -> Name](#misc-entries-name)
  - [Misc -> Entries[] -> Path](#misc-entries-path)
  - [Misc -> Entries[] -> TextMode](#misc-entries-textmode)
- [Misc -> Security](#misc-security)
  - [Misc -> Security -> AllowSetDefault](#misc-security-allowsetdefault)
  - [Misc -> Security -> ApECID](#misc-security-apecid)
  - [Misc -> Security -> AuthRestart](#misc-security-authrestart)
  - [Misc -> Security -> BlacklistAppleUpdate](#misc-security-blacklistappleupdate)
  - [Misc -> Security -> DmgLoading](#misc-security-dmgloading)
  - [Misc -> Security -> EnablePassword](#misc-security-enablepassword)
  - [Misc -> Security -> ExposeSensitiveData](#misc-security-exposesensitivedata)
  - [Misc -> Security -> HaltLevel](#misc-security-haltlevel)
  - [Misc -> Security -> PasswordHash](#misc-security-passwordhash)
  - [Misc -> Security -> PasswordSalt](#misc-security-passwordsalt)
  - [Misc -> Security -> ScanPolicy](#misc-security-scanpolicy)
  - [Misc -> Security -> SecureBootModel](#misc-security-securebootmodel)
  - [Misc -> Security -> Vault](#misc-security-vault)
- [Misc -> Serial](#misc-serial)
  - [Misc -> Serial -> Custom](#misc-serial-custom)
    - [Misc -> Serial -> Custom -> BaudRate](#misc-serial-custom-baudrate)
    - [Misc -> Serial -> Custom -> ClockRate](#misc-serial-custom-clockrate)
    - [Misc -> Serial -> Custom -> DetectCable](#misc-serial-custom-detectcable)
    - [Misc -> Serial -> Custom -> ExtendedTxFifoSize](#misc-serial-custom-extendedtxfifosize)
    - [Misc -> Serial -> Custom -> FifoControl](#misc-serial-custom-fifocontrol)
    - [Misc -> Serial -> Custom -> LineControl](#misc-serial-custom-linecontrol)
    - [Misc -> Serial -> Custom -> PciDeviceInfo](#misc-serial-custom-pcideviceinfo)
    - [Misc -> Serial -> Custom -> RegisterAccessWidth](#misc-serial-custom-registeraccesswidth)
    - [Misc -> Serial -> Custom -> RegisterBase](#misc-serial-custom-registerbase)
    - [Misc -> Serial -> Custom -> RegisterStride](#misc-serial-custom-registerstride)
    - [Misc -> Serial -> Custom -> UseHardwareFlowControl](#misc-serial-custom-usehardwareflowcontrol)
    - [Misc -> Serial -> Custom -> UseMmio](#misc-serial-custom-usemmio)
  - [Misc -> Serial -> Init](#misc-serial-init)
  - [Misc -> Serial -> Override](#misc-serial-override)
- [Misc -> Tools](#misc-tools)
  - [Misc -> Tools[] -> Arguments](#misc-tools-arguments)
  - [Misc -> Tools[] -> Auxiliary](#misc-tools-auxiliary)
  - [Misc -> Tools[] -> Comment](#misc-tools-comment)
  - [Misc -> Tools[] -> Enabled](#misc-tools-enabled)
  - [Misc -> Tools[] -> Flavour](#misc-tools-flavour)
  - [Misc -> Tools[] -> FullNvramAccess](#misc-tools-fullnvramaccess)
  - [Misc -> Tools[] -> Name](#misc-tools-name)
  - [Misc -> Tools[] -> Path](#misc-tools-path)
  - [Misc -> Tools[] -> RealPath](#misc-tools-realpath)
  - [Misc -> Tools[] -> TextMode](#misc-tools-textmode)
- [NVRAM -> Add](#nvram-add)
- [NVRAM -> Delete](#nvram-delete)
- [NVRAM -> LegacyOverwrite](#nvram-legacyoverwrite)
- [NVRAM -> LegacySchema](#nvram-legacyschema)
- [NVRAM -> WriteFlash](#nvram-writeflash)
- [PlatformInfo -> Automatic](#platforminfo-automatic)
- [PlatformInfo -> CustomMemory](#platforminfo-custommemory)
- [PlatformInfo -> DataHub](#platforminfo-datahub)
  - [PlatformInfo -> DataHub -> ARTFrequency](#platforminfo-datahub-artfrequency)
  - [PlatformInfo -> DataHub -> BoardProduct](#platforminfo-datahub-boardproduct)
  - [PlatformInfo -> DataHub -> BoardRevision](#platforminfo-datahub-boardrevision)
  - [PlatformInfo -> DataHub -> DevicePathsSupported](#platforminfo-datahub-devicepathssupported)
  - [PlatformInfo -> DataHub -> FSBFrequency](#platforminfo-datahub-fsbfrequency)
  - [PlatformInfo -> DataHub -> InitialTSC](#platforminfo-datahub-initialtsc)
  - [PlatformInfo -> DataHub -> PlatformName](#platforminfo-datahub-platformname)
  - [PlatformInfo -> DataHub -> SmcBranch](#platforminfo-datahub-smcbranch)
  - [PlatformInfo -> DataHub -> SmcPlatform](#platforminfo-datahub-smcplatform)
  - [PlatformInfo -> DataHub -> SmcRevision](#platforminfo-datahub-smcrevision)
  - [PlatformInfo -> DataHub -> StartupPowerEvents](#platforminfo-datahub-startuppowerevents)
  - [PlatformInfo -> DataHub -> SystemProductName](#platforminfo-datahub-systemproductname)
  - [PlatformInfo -> DataHub -> SystemSerialNumber](#platforminfo-datahub-systemserialnumber)
  - [PlatformInfo -> DataHub -> SystemUUID](#platforminfo-datahub-systemuuid)
- [PlatformInfo -> Generic](#platforminfo-generic)
  - [PlatformInfo -> Generic -> AdviseFeatures](#platforminfo-generic-advisefeatures)
  - [PlatformInfo -> Generic -> MLB](#platforminfo-generic-mlb)
  - [PlatformInfo -> Generic -> MaxBIOSVersion](#platforminfo-generic-maxbiosversion)
  - [PlatformInfo -> Generic -> ProcessorType](#platforminfo-generic-processortype)
  - [PlatformInfo -> Generic -> ROM](#platforminfo-generic-rom)
  - [PlatformInfo -> Generic -> SpoofVendor](#platforminfo-generic-spoofvendor)
  - [PlatformInfo -> Generic -> SystemMemoryStatus](#platforminfo-generic-systemmemorystatus)
  - [PlatformInfo -> Generic -> SystemProductName](#platforminfo-generic-systemproductname)
  - [PlatformInfo -> Generic -> SystemSerialNumber](#platforminfo-generic-systemserialnumber)
  - [PlatformInfo -> Generic -> SystemUUID](#platforminfo-generic-systemuuid)
- [PlatformInfo -> Memory](#platforminfo-memory)
  - [PlatformInfo -> Memory -> DataWidth](#platforminfo-memory-datawidth)
  - [PlatformInfo -> Memory -> Devices](#platforminfo-memory-devices)
    - [PlatformInfo -> Memory -> Devices[] -> AssetTag](#platforminfo-memory-devices-assettag)
    - [PlatformInfo -> Memory -> Devices[] -> BankLocator](#platforminfo-memory-devices-banklocator)
    - [PlatformInfo -> Memory -> Devices[] -> DeviceLocator](#platforminfo-memory-devices-devicelocator)
    - [PlatformInfo -> Memory -> Devices[] -> Manufacturer](#platforminfo-memory-devices-manufacturer)
    - [PlatformInfo -> Memory -> Devices[] -> PartNumber](#platforminfo-memory-devices-partnumber)
    - [PlatformInfo -> Memory -> Devices[] -> SerialNumber](#platforminfo-memory-devices-serialnumber)
    - [PlatformInfo -> Memory -> Devices[] -> Size](#platforminfo-memory-devices-size)
    - [PlatformInfo -> Memory -> Devices[] -> Speed](#platforminfo-memory-devices-speed)
  - [PlatformInfo -> Memory -> ErrorCorrection](#platforminfo-memory-errorcorrection)
  - [PlatformInfo -> Memory -> FormFactor](#platforminfo-memory-formfactor)
  - [PlatformInfo -> Memory -> MaxCapacity](#platforminfo-memory-maxcapacity)
  - [PlatformInfo -> Memory -> TotalWidth](#platforminfo-memory-totalwidth)
  - [PlatformInfo -> Memory -> Type](#platforminfo-memory-type)
  - [PlatformInfo -> Memory -> TypeDetail](#platforminfo-memory-typedetail)
- [PlatformInfo -> PlatformNVRAM](#platforminfo-platformnvram)
  - [PlatformInfo -> PlatformNVRAM -> BID](#platforminfo-platformnvram-bid)
  - [PlatformInfo -> PlatformNVRAM -> FirmwareFeatures](#platforminfo-platformnvram-firmwarefeatures)
  - [PlatformInfo -> PlatformNVRAM -> FirmwareFeaturesMask](#platforminfo-platformnvram-firmwarefeaturesmask)
  - [PlatformInfo -> PlatformNVRAM -> MLB](#platforminfo-platformnvram-mlb)
  - [PlatformInfo -> PlatformNVRAM -> ROM](#platforminfo-platformnvram-rom)
  - [PlatformInfo -> PlatformNVRAM -> SystemSerialNumber](#platforminfo-platformnvram-systemserialnumber)
  - [PlatformInfo -> PlatformNVRAM -> SystemUUID](#platforminfo-platformnvram-systemuuid)
- [PlatformInfo -> SMBIOS](#platforminfo-smbios)
  - [PlatformInfo -> SMBIOS -> BIOSReleaseDate](#platforminfo-smbios-biosreleasedate)
  - [PlatformInfo -> SMBIOS -> BIOSVendor](#platforminfo-smbios-biosvendor)
  - [PlatformInfo -> SMBIOS -> BIOSVersion](#platforminfo-smbios-biosversion)
  - [PlatformInfo -> SMBIOS -> BoardAssetTag](#platforminfo-smbios-boardassettag)
  - [PlatformInfo -> SMBIOS -> BoardLocationInChassis](#platforminfo-smbios-boardlocationinchassis)
  - [PlatformInfo -> SMBIOS -> BoardManufacturer](#platforminfo-smbios-boardmanufacturer)
  - [PlatformInfo -> SMBIOS -> BoardProduct](#platforminfo-smbios-boardproduct)
  - [PlatformInfo -> SMBIOS -> BoardSerialNumber](#platforminfo-smbios-boardserialnumber)
  - [PlatformInfo -> SMBIOS -> BoardType](#platforminfo-smbios-boardtype)
  - [PlatformInfo -> SMBIOS -> BoardVersion](#platforminfo-smbios-boardversion)
  - [PlatformInfo -> SMBIOS -> ChassisAssetTag](#platforminfo-smbios-chassisassettag)
  - [PlatformInfo -> SMBIOS -> ChassisManufacturer](#platforminfo-smbios-chassismanufacturer)
  - [PlatformInfo -> SMBIOS -> ChassisSerialNumber](#platforminfo-smbios-chassisserialnumber)
  - [PlatformInfo -> SMBIOS -> ChassisType](#platforminfo-smbios-chassistype)
  - [PlatformInfo -> SMBIOS -> ChassisVersion](#platforminfo-smbios-chassisversion)
  - [PlatformInfo -> SMBIOS -> FirmwareFeatures](#platforminfo-smbios-firmwarefeatures)
  - [PlatformInfo -> SMBIOS -> FirmwareFeaturesMask](#platforminfo-smbios-firmwarefeaturesmask)
  - [PlatformInfo -> SMBIOS -> PlatformFeature](#platforminfo-smbios-platformfeature)
  - [PlatformInfo -> SMBIOS -> ProcessorType](#platforminfo-smbios-processortype)
  - [PlatformInfo -> SMBIOS -> SmcVersion](#platforminfo-smbios-smcversion)
  - [PlatformInfo -> SMBIOS -> SystemFamily](#platforminfo-smbios-systemfamily)
  - [PlatformInfo -> SMBIOS -> SystemManufacturer](#platforminfo-smbios-systemmanufacturer)
  - [PlatformInfo -> SMBIOS -> SystemProductName](#platforminfo-smbios-systemproductname)
  - [PlatformInfo -> SMBIOS -> SystemSKUNumber](#platforminfo-smbios-systemskunumber)
  - [PlatformInfo -> SMBIOS -> SystemSerialNumber](#platforminfo-smbios-systemserialnumber)
  - [PlatformInfo -> SMBIOS -> SystemUUID](#platforminfo-smbios-systemuuid)
  - [PlatformInfo -> SMBIOS -> SystemVersion](#platforminfo-smbios-systemversion)
- [PlatformInfo -> UpdateDataHub](#platforminfo-updatedatahub)
- [PlatformInfo -> UpdateNVRAM](#platforminfo-updatenvram)
- [PlatformInfo -> UpdateSMBIOS](#platforminfo-updatesmbios)
- [PlatformInfo -> UpdateSMBIOSMode](#platforminfo-updatesmbiosmode)
- [PlatformInfo -> UseRawUuidEncoding](#platforminfo-userawuuidencoding)
- [UEFI -> APFS](#uefi-apfs)
  - [UEFI -> APFS -> EnableJumpstart](#uefi-apfs-enablejumpstart)
  - [UEFI -> APFS -> GlobalConnect](#uefi-apfs-globalconnect)
  - [UEFI -> APFS -> HideVerbose](#uefi-apfs-hideverbose)
  - [UEFI -> APFS -> JumpstartHotPlug](#uefi-apfs-jumpstarthotplug)
  - [UEFI -> APFS -> MinDate](#uefi-apfs-mindate)
  - [UEFI -> APFS -> MinVersion](#uefi-apfs-minversion)
- [UEFI -> AppleInput](#uefi-appleinput)
  - [UEFI -> AppleInput -> AppleEvent](#uefi-appleinput-appleevent)
  - [UEFI -> AppleInput -> CustomDelays](#uefi-appleinput-customdelays)
  - [UEFI -> AppleInput -> GraphicsInputMirroring](#uefi-appleinput-graphicsinputmirroring)
  - [UEFI -> AppleInput -> KeyInitialDelay](#uefi-appleinput-keyinitialdelay)
  - [UEFI -> AppleInput -> KeySubsequentDelay](#uefi-appleinput-keysubsequentdelay)
  - [UEFI -> AppleInput -> PointerDwellClickTimeout](#uefi-appleinput-pointerdwellclicktimeout)
  - [UEFI -> AppleInput -> PointerDwellDoubleClickTimeout](#uefi-appleinput-pointerdwelldoubleclicktimeout)
  - [UEFI -> AppleInput -> PointerDwellRadius](#uefi-appleinput-pointerdwellradius)
  - [UEFI -> AppleInput -> PointerPollMask](#uefi-appleinput-pointerpollmask)
  - [UEFI -> AppleInput -> PointerPollMax](#uefi-appleinput-pointerpollmax)
  - [UEFI -> AppleInput -> PointerPollMin](#uefi-appleinput-pointerpollmin)
  - [UEFI -> AppleInput -> PointerSpeedDiv](#uefi-appleinput-pointerspeeddiv)
  - [UEFI -> AppleInput -> PointerSpeedMul](#uefi-appleinput-pointerspeedmul)
- [UEFI -> Audio](#uefi-audio)
  - [UEFI -> Audio -> AudioCodec](#uefi-audio-audiocodec)
  - [UEFI -> Audio -> AudioDevice](#uefi-audio-audiodevice)
  - [UEFI -> Audio -> AudioOutMask](#uefi-audio-audiooutmask)
  - [UEFI -> Audio -> AudioSupport](#uefi-audio-audiosupport)
  - [UEFI -> Audio -> DisconnectHda](#uefi-audio-disconnecthda)
  - [UEFI -> Audio -> MaximumGain](#uefi-audio-maximumgain)
  - [UEFI -> Audio -> MinimumAssistGain](#uefi-audio-minimumassistgain)
  - [UEFI -> Audio -> MinimumAudibleGain](#uefi-audio-minimumaudiblegain)
  - [UEFI -> Audio -> PlayChime](#uefi-audio-playchime)
  - [UEFI -> Audio -> ResetTrafficClass](#uefi-audio-resettrafficclass)
  - [UEFI -> Audio -> SetupDelay](#uefi-audio-setupdelay)
- [UEFI -> ConnectDrivers](#uefi-connectdrivers)
- [UEFI -> Drivers](#uefi-drivers)
  - [UEFI -> Drivers[] -> Arguments](#uefi-drivers-arguments)
  - [UEFI -> Drivers[] -> Comment](#uefi-drivers-comment)
  - [UEFI -> Drivers[] -> Enabled](#uefi-drivers-enabled)
  - [UEFI -> Drivers[] -> LoadEarly](#uefi-drivers-loadearly)
  - [UEFI -> Drivers[] -> Path](#uefi-drivers-path)
- [UEFI -> Input](#uefi-input)
  - [UEFI -> Input -> KeyFiltering](#uefi-input-keyfiltering)
  - [UEFI -> Input -> KeyForgetThreshold](#uefi-input-keyforgetthreshold)
  - [UEFI -> Input -> KeySupport](#uefi-input-keysupport)
  - [UEFI -> Input -> KeySupportMode](#uefi-input-keysupportmode)
  - [UEFI -> Input -> KeySwap](#uefi-input-keyswap)
  - [UEFI -> Input -> PointerSupport](#uefi-input-pointersupport)
  - [UEFI -> Input -> PointerSupportMode](#uefi-input-pointersupportmode)
  - [UEFI -> Input -> TimerResolution](#uefi-input-timerresolution)
- [UEFI -> Output](#uefi-output)
  - [UEFI -> Output -> ClearScreenOnModeSwitch](#uefi-output-clearscreenonmodeswitch)
  - [UEFI -> Output -> ConsoleFont](#uefi-output-consolefont)
  - [UEFI -> Output -> ConsoleMode](#uefi-output-consolemode)
  - [UEFI -> Output -> DirectGopRendering](#uefi-output-directgoprendering)
  - [UEFI -> Output -> ForceResolution](#uefi-output-forceresolution)
  - [UEFI -> Output -> GopBurstMode](#uefi-output-gopburstmode)
  - [UEFI -> Output -> GopPassThrough](#uefi-output-goppassthrough)
  - [UEFI -> Output -> IgnoreTextInGraphics](#uefi-output-ignoretextingraphics)
  - [UEFI -> Output -> InitialMode](#uefi-output-initialmode)
  - [UEFI -> Output -> ProvideConsoleGop](#uefi-output-provideconsolegop)
  - [UEFI -> Output -> ReconnectGraphicsOnConnect](#uefi-output-reconnectgraphicsonconnect)
  - [UEFI -> Output -> ReconnectOnResChange](#uefi-output-reconnectonreschange)
  - [UEFI -> Output -> ReplaceTabWithSpace](#uefi-output-replacetabwithspace)
  - [UEFI -> Output -> Resolution](#uefi-output-resolution)
  - [UEFI -> Output -> SanitiseClearScreen](#uefi-output-sanitiseclearscreen)
  - [UEFI -> Output -> TextRenderer](#uefi-output-textrenderer)
  - [UEFI -> Output -> UIScale](#uefi-output-uiscale)
  - [UEFI -> Output -> UgaPassThrough](#uefi-output-ugapassthrough)
- [UEFI -> ProtocolOverrides](#uefi-protocoloverrides)
  - [UEFI -> ProtocolOverrides -> AppleAudio](#uefi-protocoloverrides-appleaudio)
  - [UEFI -> ProtocolOverrides -> AppleBootPolicy](#uefi-protocoloverrides-applebootpolicy)
  - [UEFI -> ProtocolOverrides -> AppleDebugLog](#uefi-protocoloverrides-appledebuglog)
  - [UEFI -> ProtocolOverrides -> AppleEg2Info](#uefi-protocoloverrides-appleeg2info)
  - [UEFI -> ProtocolOverrides -> AppleFramebufferInfo](#uefi-protocoloverrides-appleframebufferinfo)
  - [UEFI -> ProtocolOverrides -> AppleImageConversion](#uefi-protocoloverrides-appleimageconversion)
  - [UEFI -> ProtocolOverrides -> AppleImg4Verification](#uefi-protocoloverrides-appleimg4verification)
  - [UEFI -> ProtocolOverrides -> AppleKeyMap](#uefi-protocoloverrides-applekeymap)
  - [UEFI -> ProtocolOverrides -> AppleRtcRam](#uefi-protocoloverrides-applertcram)
  - [UEFI -> ProtocolOverrides -> AppleSecureBoot](#uefi-protocoloverrides-applesecureboot)
  - [UEFI -> ProtocolOverrides -> AppleSmcIo](#uefi-protocoloverrides-applesmcio)
  - [UEFI -> ProtocolOverrides -> AppleUserInterfaceTheme](#uefi-protocoloverrides-appleuserinterfacetheme)
  - [UEFI -> ProtocolOverrides -> DataHub](#uefi-protocoloverrides-datahub)
  - [UEFI -> ProtocolOverrides -> DeviceProperties](#uefi-protocoloverrides-deviceproperties)
  - [UEFI -> ProtocolOverrides -> FirmwareVolume](#uefi-protocoloverrides-firmwarevolume)
  - [UEFI -> ProtocolOverrides -> HashServices](#uefi-protocoloverrides-hashservices)
  - [UEFI -> ProtocolOverrides -> OSInfo](#uefi-protocoloverrides-osinfo)
  - [UEFI -> ProtocolOverrides -> PciIo](#uefi-protocoloverrides-pciio)
  - [UEFI -> ProtocolOverrides -> UnicodeCollation](#uefi-protocoloverrides-unicodecollation)
- [UEFI -> Quirks](#uefi-quirks)
  - [UEFI -> Quirks -> ActivateHpetSupport](#uefi-quirks-activatehpetsupport)
  - [UEFI -> Quirks -> DisableSecurityPolicy](#uefi-quirks-disablesecuritypolicy)
  - [UEFI -> Quirks -> EnableVectorAcceleration](#uefi-quirks-enablevectoracceleration)
  - [UEFI -> Quirks -> EnableVmx](#uefi-quirks-enablevmx)
  - [UEFI -> Quirks -> ExitBootServicesDelay](#uefi-quirks-exitbootservicesdelay)
  - [UEFI -> Quirks -> ForceOcWriteFlash](#uefi-quirks-forceocwriteflash)
  - [UEFI -> Quirks -> ForgeUefiSupport](#uefi-quirks-forgeuefisupport)
  - [UEFI -> Quirks -> IgnoreInvalidFlexRatio](#uefi-quirks-ignoreinvalidflexratio)
  - [UEFI -> Quirks -> ReleaseUsbOwnership](#uefi-quirks-releaseusbownership)
  - [UEFI -> Quirks -> ReloadOptionRoms](#uefi-quirks-reloadoptionroms)
  - [UEFI -> Quirks -> RequestBootVarRouting](#uefi-quirks-requestbootvarrouting)
  - [UEFI -> Quirks -> ResizeGpuBars](#uefi-quirks-resizegpubars)
  - [UEFI -> Quirks -> ResizeUsePciRbIo](#uefi-quirks-resizeusepcirbio)
  - [UEFI -> Quirks -> TscSyncTimeout](#uefi-quirks-tscsynctimeout)
  - [UEFI -> Quirks -> UnblockFsConnect](#uefi-quirks-unblockfsconnect)
- [UEFI -> ReservedMemory](#uefi-reservedmemory)
  - [UEFI -> ReservedMemory[] -> Address](#uefi-reservedmemory-address)
  - [UEFI -> ReservedMemory[] -> Comment](#uefi-reservedmemory-comment)
  - [UEFI -> ReservedMemory[] -> Enabled](#uefi-reservedmemory-enabled)
  - [UEFI -> ReservedMemory[] -> Size](#uefi-reservedmemory-size)
  - [UEFI -> ReservedMemory[] -> Type](#uefi-reservedmemory-type)

</details>

<h2 id=acpi-add>ACPI -> Add</h2>

**Type**: `plist array`

**Failsafe**: Empty

**Description**: Load selected tables from the `OC/ACPI` directory.

To be filled with `plist dict` values, describing each add entry. Refer to the **Add Properties** section below for details.

<h3 id=acpi-add-comment>ACPI -> Add[] -> Comment</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Arbitrary ASCII string used to provide human readable reference for the entry. Whether this value is used is implementation defined.

<h3 id=acpi-add-enabled>ACPI -> Add[] -> Enabled</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Set to `true` to add this ACPI table.

<h3 id=acpi-add-path>ACPI -> Add[] -> Path</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: File paths meant to be loaded as ACPI tables. Example values include `DSDT.aml`, `SubDir/SSDT-8.aml`, `SSDT-USBX.aml`, etc.

The ACPI table load order follows the item order in the array. ACPI tables are loaded from the `OC/ACPI` directory.

**Note**: All tables apart from tables with a `DSDT` table identifier (determined by parsing data, not by filename) insert new tables into the ACPI stack. `DSDT` tables perform a replacement of DSDT tables instead.

<h2 id=acpi-delete>ACPI -> Delete</h2>

**Type**: `plist array`

**Failsafe**: Empty

**Description**: Remove selected tables from the ACPI stack.

To be filled with `plist dict` values, describing each delete entry. Refer to the **Delete Properties** section below for details.

<h3 id=acpi-delete-all>ACPI -> Delete[] -> All</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false` (Only delete the first matched table)

**Description**: Set to `true` to delete all ACPI tables matching the condition.

<h3 id=acpi-delete-comment>ACPI -> Delete[] -> Comment</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Arbitrary ASCII string used to provide human readable reference for the entry. Whether this value is used is implementation defined.

<h3 id=acpi-delete-enabled>ACPI -> Delete[] -> Enabled</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Set to `true` to remove this ACPI table.

<h3 id=acpi-delete-oemtableid>ACPI -> Delete[] -> OemTableId</h3>

**Type**: `plist data`, 8 bytes

**Default**: `0x0000000000000000`

**Failsafe**: All zero (Match any table OEM ID)

**Description**: Match table OEM ID equal to this value.

<h3 id=acpi-delete-tablelength>ACPI -> Delete[] -> TableLength</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0` (Match any table size)

**Description**: Match table size equal to this value.

<h3 id=acpi-delete-tablesignature>ACPI -> Delete[] -> TableSignature</h3>

**Type**: `plist data`, 4 bytes

**Default**: `0x00000000`

**Failsafe**: All zero (Match any table signature)

**Description**: Match table signature equal to this value.

*Note*: Do not use table signatures when the sequence must be replaced in multiple places. This is particularly relevant when performing different types of renames.

<h2 id=acpi-patch>ACPI -> Patch</h2>

**Type**: `plist array`

**Failsafe**: Empty

**Description**: Perform binary patches in ACPI tables before table addition or removal.

To be filled with `plist dictionary` values describing each patch entry. Refer to the **Patch Properties** section below for details.

<h3 id=acpi-patch-base>ACPI -> Patch[] -> Base</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty (Ignored)

**Description**: Selects ACPI path base for patch lookup (or immediate replacement) by obtaining the offset to the provided path.

Only fully-qualified absolute paths are supported (e.g. `\_SB.PCI0.LPCB.HPET`). Currently supported object types are: `Device`, `Field`, `Method`.

*Note*: Use with care, not all OEM tables can be parsed. Use `ACPIe` utility to debug. `ACPIe` compiledwith `DEBUG=1 make` command produces helpful ACPI lookup tracing.

<h3 id=acpi-patch-baseskip>ACPI -> Patch[] -> BaseSkip</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0` (Do not skip any occurrences)

**Description**: Number of found `Base` occurrences to skip before finds and replacements are applied.

<h3 id=acpi-patch-comment>ACPI -> Patch[] -> Comment</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Arbitrary ASCII string used to provide human readable reference for the entry. Whether this value is used is implementation defined.

<h3 id=acpi-patch-count>ACPI -> Patch[] -> Count</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0` (Apply patch to all occurrences found)

**Description**: Number of occurrences to patch.

<h3 id=acpi-patch-enabled>ACPI -> Patch[] -> Enabled</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Set to `true` to apply this ACPI patch.

<h3 id=acpi-patch-find>ACPI -> Patch[] -> Find</h3>

**Type**: `plist data`

**Default**: Empty

**Failsafe**: Empty

**Description**: Data to find. Must be equal to `Replace` in size if set.

*Note*: Can be empty, when `Base` is specified, immediate replacement after `Base` lookup happens in this case.

<h3 id=acpi-patch-limit>ACPI -> Patch[] -> Limit</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0` (Search entire ACPI table)

**Description**: Maximum number of bytes to search for.

<h3 id=acpi-patch-mask>ACPI -> Patch[] -> Mask</h3>

**Type**: `plist data`

**Default**: Empty

**Failsafe**: Empty (Ignored)

**Description**: Data bitwise mask used during find comparison. Allows fuzzy search by ignoring not masked (set to zero) bits. Must be equal to `Replace` in size if set.

<h3 id=acpi-patch-oemtableid>ACPI -> Patch[] -> OemTableId</h3>

**Type**: `plist data`, 8 bytes

**Default**: `0x0000000000000000`

**Failsafe**: All zero (Match any table OEM ID)

**Description**: Match table OEM ID equal to this value.

<h3 id=acpi-patch-replace>ACPI -> Patch[] -> Replace</h3>

**Type**: `plist data`

**Default**: Empty

**Failsafe**: Empty

**Description**: Replacement data of one or more bytes.

<h3 id=acpi-patch-replacemask>ACPI -> Patch[] -> ReplaceMask</h3>

**Type**: `plist data`

**Default**: Empty

**Failsafe**: Empty (Ignored)

**Description**: Data bitwise mask used during replacement. Allows fuzzy replacement by updating masked (set to non-zero) bits. Must be equal to `Replace` in size if set.

<h3 id=acpi-patch-skip>ACPI -> Patch[] -> Skip</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0` (Do not skip any occurrences)

**Description**: Number of found occurrences to skip before replacements are applied.

<h3 id=acpi-patch-tablelength>ACPI -> Patch[] -> TableLength</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0` (Match any table size)

**Description**: Match table size equal to this value.

<h3 id=acpi-patch-tablesignature>ACPI -> Patch[] -> TableSignature</h3>

**Type**: `plist data`, 4 bytes

**Default**: `0x00000000`

**Failsafe**: All zero (Match any table signature)

**Description**: Match table signature equal to this value.

<h2 id=acpi-quirks>ACPI -> Quirks</h2>

**Type**: `plist dict`

**Description**: Apply individual ACPI quirks described in the **Quirks Properties** section below.

<h3 id=acpi-quirks-fadtenablereset>ACPI -> Quirks -> FadtEnableReset</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Provide reset register and flag in FADT table to enable reboot and shutdown.

Mainly required on legacy hardware and a few newer laptops. Can also fix power-button shortcuts. Not recommended unless required.

<h3 id=acpi-quirks-normalizeheaders>ACPI -> Quirks -> NormalizeHeaders</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Cleanup ACPI header fields to workaround macOS ACPI implementation flaws that result in boot crashes. Reference: [Debugging AppleACPIPlatform on 10.13](https://alextjam.es/debugging-appleacpiplatform/) by Alex James (also known as theracermaster). The issue was fixed in macOS Mojave (10.14).

<h3 id=acpi-quirks-rebaseregions>ACPI -> Quirks -> RebaseRegions</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Attempt to heuristically relocate ACPI memory regions. Not recommended.

ACPI tables are often generated dynamically by the underlying firmware implementation. Among the position-independent code, ACPI tables may contain the physical addresses of MMIO areas used for device configuration, typically grouped by region (e.g. `OperationRegion`). Changing firmware settings or hardware configuration, upgrading or patching the firmware inevitably leads to changes in dynamically generated ACPI code, which sometimes results in the shift of the addresses in the aforementioned `OperationRegion` constructions.

For this reason, the application of modifications to ACPI tables is extremely risky. The best approach is to make as few changes as possible to ACPI tables and to avoid replacing any tables, particularly DSDT tables. When this cannot be avoided, ensure that any custom DSDT tables are based on the most recent DSDT tables or attempt to remove reads and writes for the affected areas.

When nothing else helps, this option could be tried to avoid stalls at `PCI Configuration Begin` phase of macOS booting by attempting to fix the ACPI addresses. It is not a magic bullet however, and only works with the most typical cases. Do not use unless absolutely required as it can have the opposite effect on certain platforms and result in boot failures.

<h3 id=acpi-quirks-resethwsig>ACPI -> Quirks -> ResetHwSig</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Reset `FACS` table `HardwareSignature` value to `0`.

This works around firmware that fail to maintain hardware signature across the reboots and cause issues with waking from hibernation.

<h3 id=acpi-quirks-resetlogostatus>ACPI -> Quirks -> ResetLogoStatus</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Reset `BGRT` table `Displayed` status field to `false`.

This works around firmware that provide a `BGRT` table but fail to handle screen updates afterwards.

<h3 id=acpi-quirks-synctableids>ACPI -> Quirks -> SyncTableIds</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Sync table identifiers with the `SLIC` table.

This works around patched tables becoming incompatible with the `SLIC` table causing licensing issues in older Windows operating systems.

<h2 id=booter-mmiowhitelist>Booter -> MmioWhitelist</h2>

**Type**: `plist array`

**Failsafe**: Empty

**Description**: To be filled with `plist dict` values, describing addresses critical for particular firmware functioning when `DevirtualiseMmio` quirk is in use. Refer to the **MmioWhitelist Properties** section below for details.

<h3 id=booter-mmiowhitelist-address>Booter -> MmioWhitelist[] -> Address</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0`

**Description**: Exceptional MMIO address, which memory descriptor should be left virtualised (unchanged) by `DevirtualiseMmio`. This means that the firmware will be able to directly communicate with this memory region during operating system functioning, because the region this value is in will be assigned a virtual address.

The addresses written here must be part of the memory map, have `EfiMemoryMappedIO` type and `EFI_MEMORY_RUNTIME` attribute (highest bit) set. The debug log can be used to find the list of the candidates.

<h3 id=booter-mmiowhitelist-comment>Booter -> MmioWhitelist[] -> Comment</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Arbitrary ASCII string used to provide human readable reference for the entry. Whether this value is used is implementation defined.

<h3 id=booter-mmiowhitelist-enabled>Booter -> MmioWhitelist[] -> Enabled</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Exclude MMIO address from the devirtualisation procedure.

<h2 id=booter-patch>Booter -> Patch</h2>

**Type**: `plist array`

**Failsafe**: Empty

**Description**: Perform binary patches in booter.

To be filled with `plist dictionary` values, describing each patch. Refer to the **Patch Properties** section below for details.

<h3 id=booter-patch-arch>Booter -> Patch[] -> Arch</h3>

**Type**: `plist string`

**Default**: `Any`

**Failsafe**: `Any` (Apply to any supported architecture)

**Description**: Booter patch architecture (`i386`, `x86_64`).

<h3 id=booter-patch-comment>Booter -> Patch[] -> Comment</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Arbitrary ASCII string used to provide human readable reference for the entry. Whether this value is used is implementation defined.

<h3 id=booter-patch-count>Booter -> Patch[] -> Count</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0` (Apply to all occurrences found)

**Description**: Number of patch occurrences to apply.

<h3 id=booter-patch-enabled>Booter -> Patch[] -> Enabled</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Set to `true` to activate this booter patch.

<h3 id=booter-patch-find>Booter -> Patch[] -> Find</h3>

**Type**: `plist data`

**Default**: Empty

**Failsafe**: Empty

**Description**: Data to find. Must be equal to `Replace` in size if set.

<h3 id=booter-patch-identifier>Booter -> Patch[] -> Identifier</h3>

**Type**: `plist string`

**Default**: `Any`

**Failsafe**:`Any` (Match any booter)

**Description**: `Apple` for macOS booter (typically `boot.efi`); or a name with a suffix, such as `bootmgfw.efi`, for a specific booter.

<h3 id=booter-patch-limit>Booter -> Patch[] -> Limit</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0` (Search the entire booter)

**Description**: Maximum number of bytes to search for.

<h3 id=booter-patch-mask>Booter -> Patch[] -> Mask</h3>

**Type**: `plist data`

**Default**: Empty

**Failsafe**: Empty (Ignored)

**Description**: Data bitwise mask used during find comparison. Allows fuzzy search by ignoring not masked (set to zero) bits. Must be equal to `Find` in size if set.

<h3 id=booter-patch-replace>Booter -> Patch[] -> Replace</h3>

**Type**: `plist data`

**Default**: Empty

**Failsafe**: Empty

**Description**: Replacement data of one or more bytes.

<h3 id=booter-patch-replacemask>Booter -> Patch[] -> ReplaceMask</h3>

**Type**: `plist data`

**Default**: Empty

**Failsafe**: Empty (Ignored)

**Description**: Data bitwise mask used during replacement. Allows fuzzy replacement by updating masked (set to non-zero) bits. Must be equal to `Replace` in size if set.

<h3 id=booter-patch-skip>Booter -> Patch[] -> Skip</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0` (Do not skip any occurrences)

**Description**: Number of found occurrences to skip before replacements are applied.

<h2 id=booter-quirks>Booter -> Quirks</h2>

**Type**: `plist dict`

**Description**: Apply individual booter quirks described in the **Quirks Properties** section below.

<h3 id=booter-quirks-allowrelocationblock>Booter -> Quirks -> AllowRelocationBlock</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Allows booting macOS through a relocation block.

The relocation block is a scratch buffer allocated in the lower 4 GB used for loading the kernel and related structures by EfiBoot on firmware where the lower memory region is otherwise occupied by (assumed) non-runtime data. Right before kernel startup, the relocation block is copied back to lower addresses. Similarly, all the other addresses pointing to the relocation block are also carefully adjusted. The relocation block can be used when:
* No better slide exists (all the memory is used)
* `slide=0` is forced (by an argument or safe mode)
* KASLR (slide) is unsupported (this is macOS 10.7 or older) 

This quirk requires `ProvideCustomSlide` to be enabled and typically also requires enabling `AvoidRuntimeDefrag` to function correctly. Hibernation is not supported when booting with a relocation block, which will only be used if required when the quirk is enabled.

*Note*: While this quirk is required to run older macOS versions on platforms with used lower memory, it is not compatible with some hardware and macOS 11. In such cases, consider using `EnableSafeModeSlide` instead.

<h3 id=booter-quirks-avoidruntimedefrag>Booter -> Quirks -> AvoidRuntimeDefrag</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Protect from boot.efi runtime memory defragmentation.

This option fixes UEFI runtime services (date, time, NVRAM, power control, etc.) support on firmware that uses SMM backing for certain services such as variable storage. SMM may try to access memory by physical addresses in non-SMM areas but this may sometimes have been moved by boot.efi. This option prevents boot.efi from moving such data.

*Note*: Most types of firmware, apart from Apple and VMware, need this quirk.

<h3 id=booter-quirks-devirtualisemmio>Booter -> Quirks -> DevirtualiseMmio</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Remove runtime attribute from certain MMIO regions.

This quirk reduces the stolen memory footprint in the memory map by removing the runtime bit for known memory regions. This quirk may result in an increase of KASLR slides available but without additional measures, it is not necessarily compatible with the target board. This quirk typically frees between 64 and 256 megabytes of memory, present in the debug log, and on some platforms, is the only way to boot macOS, which otherwise fails with allocation errors at the bootloader stage.

This option is useful on all types of firmware, except for some very old ones such as Sandy Bridge. On certain firmware, a list of addresses that need virtual addresses for proper NVRAM and hibernation functionality may be required. Use the `MmioWhitelist` section for this.

<h3 id=booter-quirks-disablesingleuser>Booter -> Quirks -> DisableSingleUser</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Disable single user mode.

This is a security option that restricts the activation of single user mode by ignoring the `CMD+S` hotkey and the `-s` boot argument. The behaviour with this quirk enabled is supposed to match T2-based model behaviour. Refer to this [archived article](https://web.archive.org/web/20200517125051/https://support.apple.com/en-us/HT201573) to understand how to use single user mode with this quirk enabled.

*Note*: When Apple Secure Boot is enabled single user mode is always disabled.

<h3 id=booter-quirks-disablevariablewrite>Booter -> Quirks -> DisableVariableWrite</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Protect from macOS NVRAM write access.

This is a security option that restricts NVRAM access in macOS. This quirk requires `OC_FIRMWARE_RUNTIME` protocol implemented in `OpenRuntime.efi`.

*Note*: This quirk can also be used as an ad hoc workaround for defective UEFI runtime services implementations that are unable to write variables to NVRAM and results in operating system failures.

<h3 id=booter-quirks-discardhibernatemap>Booter -> Quirks -> DiscardHibernateMap</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Reuse original hibernate memory map.

This option forces the XNU kernel to ignore a newly supplied memory map and assume that it did not change after waking from hibernation. This behaviour is required byWindows to work. Windows mandates [preserving](https://docs.microsoft.com/en-us/windows-hardware/design/device-experiences/oem-uefi#hibernation-state-s4-transition-requirements) runtime memory size and location after S4 wake.

*Note*: This may be used to workaround defective memory map implementations on older, rare legacy hardware. Examples of such hardware are Ivy Bridge laptops with Insyde firmware such as the Acer V3-571G. Do not use this option without a full understanding of the implications.

<h3 id=booter-quirks-enablesafemodeslide>Booter -> Quirks -> EnableSafeModeSlide</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Patch bootloader to have KASLR enabled in safe mode.

This option is relevant to users with issues booting to safe mode (e.g. by holding `shift` or with using the `-x` boot argument). By default, safe mode forces `0` slide as if the system was launched with the `slide=0` boot argument.
* This quirk attempts to patch the `boot.efi` file to remove this limitation and to allow using other values (from `1` to `255` inclusive).
* This quirk requires enabling `ProvideCustomSlide`. 

*Note*: The need for this option is dependent on the availability of safe mode. It can be enabled when booting to safe mode fails.

<h3 id=booter-quirks-enablewriteunprotector>Booter -> Quirks -> EnableWriteUnprotector</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Permit write access to UEFI runtime services code.

This option bypasses `W^{`X} permissions in code pages of UEFI runtime services by removing write protection (`WP`) bit from `CR0` register during their execution. This quirk requires `OC_FIRMWARE_RUNTIME` protocol implemented in `OpenRuntime.efi`.

*Note*: This quirk may potentially weaken firmware security. Please use `RebuildAppleMemoryMap` if the firmware supports memory attributes table (MAT). Refer to the `OCABC: MAT support is 1/0` log entry to determine whether MAT is supported.

<h3 id=booter-quirks-forcebootersignature>Booter -> Quirks -> ForceBooterSignature</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Set macOS `boot-signature` to OpenCore launcher.

Booter signature, essentially a SHA-1 hash of the loaded image, is used by Mac EFI to verify the authenticity of the bootloader when waking from hibernation. This option forces macOS to use OpenCore launcher SHA-1 hash as a booter signature to let OpenCore shim hibernation wake on Mac EFI firmware.

*Note*: OpenCore launcher path is determined from `LauncherPath` property.

<h3 id=booter-quirks-forceexitbootservices>Booter -> Quirks -> ForceExitBootServices</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Retry `ExitBootServices` with new memory map on failure.

Try to ensure that the `ExitBootServices` call succeeds. If required, an outdated `MemoryMap` key argument can be used by obtaining the current memory map and retrying the `ExitBootServices` call.

*Note*: The need for this quirk is determined by early boot crashes of the firmware. Do not use this option without a full understanding of the implications.

<h3 id=booter-quirks-protectmemoryregions>Booter -> Quirks -> ProtectMemoryRegions</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Protect memory regions from incorrect access.

Some types of firmware incorrectly map certain memory regions:
* The CSM region can be marked as boot services code, or data, which leaves it as free memory for the XNU kernel.
* MMIO regions can be marked as reserved memory and stay unmapped. They may however be required to be accessible at runtime for NVRAM support. 

This quirk attempts to fix the types of these regions, e.g. ACPI NVS for CSM or MMIO for MMIO.

*Note*: The need for this quirk is determined by artifacts, sleep wake issues, and boot failures. This quirk is typically only required by very old firmware.

<h3 id=booter-quirks-protectsecureboot>Booter -> Quirks -> ProtectSecureBoot</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Protect UEFI Secure Boot variables from being written.

Reports security violation during attempts to write to `db`, `dbx`, `PK`, and `KEK` variables from the operating system.

*Note*: This quirk attempts to avoid issues with NVRAM implementations with fragmentation issues, such as on the `MacPro5,1` as well as on certain Insyde firmware without garbage collection or with defective garbage collection.

<h3 id=booter-quirks-protectuefiservices>Booter -> Quirks -> ProtectUefiServices</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Protect UEFI services from being overridden by the firmware.

Some modern firmware, including on virtual machines such as VMware, may update pointers to UEFI services during driver loading and related actions. Consequently, this directly obstructs other quirks that affect memory management, such as `DevirtualiseMmio`, `ProtectMemoryRegions`, or `RebuildAppleMemoryMap`, and may also obstruct other quirks depending on the scope of such.

GRUB shim makes similar on-the-fly changes to various UEFI image services, which are also protected against by this quirk.

*Note 1*: On VMware, the need for this quirk may be determined by the appearance of the `'Your Mac OS guest might run unreliably with more than one virtual core.'' message.

*Note 2*: This quirk is needed for correct operation if OpenCore is chainloaded from GRUB with BIOS Secure Boot enabled.

<h3 id=booter-quirks-providecustomslide>Booter -> Quirks -> ProvideCustomSlide</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Provide custom KASLR slide on low memory.

This option performs memory map analysis of the firmware and checks whether all slides (from `1` to `255`) can be used. As `boot.efi` generates this value randomly with `rdrand` or pseudo randomly `rdtsc`, there is a chance of boot failure when it chooses a conflicting slide. In cases where potential conflicts exist, this option forces macOS to select a pseudo random value from the available values. This also ensures that the `slide=` argument is never passed to the operating system (for security reasons).

*Note*: The need for this quirk is determined by the `OCABC: Only N/256 slide values are usable!` message in the debug log.

<h3 id=booter-quirks-providemaxslide>Booter -> Quirks -> ProvideMaxSlide</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0`

**Description**: Provide maximum KASLR slide when higher ones are unavailable.

This option overrides the maximum slide of 255 by a user specified value between 1 and 254 (inclusive) when `ProvideCustomSlide` is enabled. It is assumed that modern firmware allocates pool memory from top to bottom, effectively resulting in free memory when slide scanning is used later as temporary memory during kernel loading. When such memory is not available, this option stops the evaluation of higher slides.

*Note*: The need for this quirk is determined by random boot failures when `ProvideCustomSlide` is enabled and the randomized slide falls into the unavailable range. When `AppleDebug` is enabled, the debug log typically contains messages such as `AAPL: [EB|`LD:LKC] \` Err(0x9)}. To find the optimal value, append `slide=X`, where `X` is the slide value, to the `boot-args` and select the largest one that does not result in boot failures.

<h3 id=booter-quirks-rebuildapplememorymap>Booter -> Quirks -> RebuildAppleMemoryMap</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Generate macOS compatible Memory Map.

The Apple kernel has several limitations on parsing the UEFI memory map:
* The Memory map size must not exceed 4096 bytes as the Apple kernel maps it as a single 4K page. As some types of firmware can have very large memory maps, potentially over 100 entries, the Apple kernel will crash on boot.
* The Memory attributes table is ignored. `EfiRuntimeServicesCode` memory statically gets `RX` permissions while all other memory types get `RW` permissions. As some firmware drivers may write to global variables at runtime, the Apple kernel will crash at calling UEFI runtime services unless the driver `.data` section has a `EfiRuntimeServicesData` type. 

To workaround these limitations, this quirk applies memory attribute table permissions to the memory map passed to the Apple kernel and optionally attempts to unify contiguous slots of similar types if the resulting memory map exceeds 4 KB.

*Note 1*: Since several types of firmware come with incorrect memory protection tables, this quirk often comes paired with `SyncRuntimePermissions`.

*Note 2*: The need for this quirk is determined by early boot failures. This quirk replaces `EnableWriteUnprotector` on firmware supporting Memory Attribute Tables (MAT). This quirk is typically unnecessary when using `OpenDuetPkg` but may be required to boot macOS 10.6, and earlier, for reasons that are as yet unclear.

<h3 id=booter-quirks-resizeapplegpubars>Booter -> Quirks -> ResizeAppleGpuBars</h3>

**Type**: `plist integer`

**Default**: `-1`

**Failsafe**: `-1`

**Description**: Reduce GPU PCI BAR sizes for compatibility with macOS.

This quirk reduces GPU PCI BAR sizes for Apple macOS up to the specified value or lower if it is unsupported. The specified value follows PCI Resizable BAR spec. While Apple macOS supports a theoretical 1 GB maximum, in practice all non-default values may not work correctly. For this reason the only supported value for this quirk is the minimal supported BAR size, i.e. `0`. Use `-1` to disable this quirk.

For development purposes one may take risks and try other values. Consider a GPU with 2 BARs:
* `BAR0` supports sizes from 256 MB to 8 GB. Its value is 4 GB.
* `BAR1` supports sizes from 2 MB to 256 MB. Its value is 256 MB. 

*Example 1*: Setting `ResizeAppleGpuBars` to 1 GB will change `BAR0` to 1 GB and leave `BAR1` unchanged. \*Example 2*: Setting `ResizeAppleGpuBars` to 1 MB will change `BAR0` to 256 MB and `BAR0` to 2 MB. \*Example 3*: Setting `ResizeAppleGpuBars` to 16 GB will make no changes.

*Note*: See `ResizeGpuBars` quirk for general GPU PCI BAR size configuration and more details about the technology.

<h3 id=booter-quirks-setupvirtualmap>Booter -> Quirks -> SetupVirtualMap</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Setup virtual memory at `SetVirtualAddresses`.

Some types of firmware access memory by virtual addresses after a `SetVirtualAddresses` call, resulting in early boot crashes. This quirk workarounds the problem by performing early boot identity mapping of assigned virtual addresses to physical memory.

*Note*: The need for this quirk is determined by early boot failures.

<h3 id=booter-quirks-signalappleos>Booter -> Quirks -> SignalAppleOS</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Report macOS being loaded through OS Info for any OS.

This quirk is useful on Mac firmware, which loads different operating systems with different hardware configurations. For example, it is supposed to enable Intel GPU in Windows and Linux in some dual-GPU MacBook models.

<h3 id=booter-quirks-syncruntimepermissions>Booter -> Quirks -> SyncRuntimePermissions</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Update memory permissions for the runtime environment.

Some types of firmware fail to properly handle runtime permissions:
* They incorrectly mark `OpenRuntime` as not executable in the memory map.
* They incorrectly mark `OpenRuntime` as not executable in the memory attributes table.
* They lose entries from the memory attributes table after `OpenRuntime` is loaded.
* They mark items in the memory attributes table as read-write-execute. 

This quirk attempts to update the memory map and memory attributes table to correct this.

*Note*: The need for this quirk is indicated by early boot failures (note: includes halt at black screen as well as more obvious crash). Particularly likely to affect early boot of Windows or Linux (but not always both) on affected systems. Only firmware released after 2017 is typically affected.

<h2 id=deviceproperties-add>DeviceProperties -> Add</h2>

**Type**: `plist dict`

**Description**: Sets device properties from a map (`plist dict`) of device paths to a map (`plist dict`) of variable names and their values in `plist multidata` format.

*Note 1*: Device paths must be provided in canonic string format (e.g. `PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)`).

*Note 2*: Existing properties will not be changed unless deleted in the `DeviceProperties Delete` section.

<h2 id=deviceproperties-delete>DeviceProperties -> Delete</h2>

**Type**: `plist dict`

**Description**: Removes device properties from a map (`plist dict`) of device paths to an array (`plist array`) of variable names in `plist string` format.

*Note*: Currently, existing properties may only exist on firmware with DeviceProperties drivers (e.g. Apple). Hence, there is typically no reason to delete variables unless a new driver has been installed.

<h2 id=kernel-add>Kernel -> Add</h2>

**Type**: `plist array`

**Failsafe**: Empty

**Description**: Load selected kernel extensions (kexts) from the `OC/Kexts` directory.

To be filled with `plist dict` values, describing each kext. Refer to the **Add Properties** section below for details.

*Note 1*: The load order is based on the order in which the kexts appear in the array. Hence, dependencies must appear before kexts that depend on them.

*Note 2*: To track the dependency order, inspect the `OSBundleLibraries` key in the `Info.plist` file of the kext being added. Any kext included under the key is a dependency that must appear before the kext being added.

*Note 3*: Kexts may have inner kexts (`Plugins`) included in the bundle. Such `Plugins` must be added separately and follow the same global ordering rules as other kexts.

<h3 id=kernel-add-arch>Kernel -> Add[] -> Arch</h3>

**Type**: `plist string`

**Default**: `Any`

**Failsafe**: `Any` (Apply to any supported architecture)

**Description**: Kext architecture (`i386`, `x86_64`).

<h3 id=kernel-add-bundlepath>Kernel -> Add[] -> BundlePath</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Kext bundle path (e.g. `Lilu.kext` or `MyKext.kext/Contents/PlugIns/MySubKext.kext`).

<h3 id=kernel-add-comment>Kernel -> Add[] -> Comment</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Arbitrary ASCII string used to provide human readable reference for the entry. Whether this value is used is implementation defined.

<h3 id=kernel-add-enabled>Kernel -> Add[] -> Enabled</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Set to `true` to add this kernel extension.

<h3 id=kernel-add-executablepath>Kernel -> Add[] -> ExecutablePath</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Kext executable path relative to bundle (e.g. `Contents/MacOS/Lilu`).

<h3 id=kernel-add-maxkernel>Kernel -> Add[] -> MaxKernel</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Adds kernel extension on specified macOS version or older.

<h3 id=kernel-add-minkernel>Kernel -> Add[] -> MinKernel</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Adds kernel extension on specified macOS version or newer.

*Note*: Refer to the **`Add MaxKernel` description** for matching logic.

<h3 id=kernel-add-plistpath>Kernel -> Add[] -> PlistPath</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Kext `Info.plist` path relative to bundle (e.g. `Contents/Info.plist`).

<h2 id=kernel-block>Kernel -> Block</h2>

**Type**: `plist array`

**Failsafe**: Empty

**Description**: Remove selected kernel extensions (kexts) from the prelinked kernel.

To be filled with `plist dictionary` values, describing each blocked kext. Refer to the **Block Properties** section below for details.

<h3 id=kernel-block-arch>Kernel -> Block[] -> Arch</h3>

**Type**: `plist string`

**Default**: `Any`

**Failsafe**: `Any` (Apply to any supported architecture)

**Description**: Kext block architecture (`i386`, `x86_64`).

<h3 id=kernel-block-comment>Kernel -> Block[] -> Comment</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Arbitrary ASCII string used to provide human readable reference for the entry. Whether this value is used is implementation defined.

<h3 id=kernel-block-enabled>Kernel -> Block[] -> Enabled</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Set to `true` to block this kernel extension.

<h3 id=kernel-block-identifier>Kernel -> Block[] -> Identifier</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Kext bundle identifier (e.g. `com.apple.driver.AppleTyMCEDriver`).

<h3 id=kernel-block-maxkernel>Kernel -> Block[] -> MaxKernel</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Blocks kernel extension on specified macOS version or older.

*Note*: Refer to the **`Add MaxKernel` description** for matching logic.

<h3 id=kernel-block-minkernel>Kernel -> Block[] -> MinKernel</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Blocks kernel extension on specified macOS version or newer.

*Note*: Refer to the **`Add MaxKernel` description** for matching logic.

<h3 id=kernel-block-strategy>Kernel -> Block[] -> Strategy</h3>

**Type**: `plist string`

**Default**: `Disable`

**Failsafe**: `Disable` (Forcibly make the kernel driver kmod startup code return failure)

**Description**: Determines the behaviour of kernel driver blocking.

Valid values:
* `Disable` --- Forcibly make the kernel driver kmod startup code return failure.
* `Exclude` --- Remove the kernel driver from the kernel cache by dropping plist entry and filling in zeroes. 

*Note*: It is risky to `Exclude` a kext that is a dependency of others.

*Note 2*: At this moment `Exclude` is only applied to `prelinkedkernel` and newer mechanisms.

*Note 3*: In most cases strategy `Exclude` requires the new kext to be injected as a replacement.

<h2 id=kernel-emulate>Kernel -> Emulate</h2>

**Type**: `plist dict`

**Description**: Emulate certain hardware in kernelspace via parameters described in the **Emulate Properties** section below.

<h3 id=kernel-emulate-cpuid1data>Kernel -> Emulate -> Cpuid1Data</h3>

**Type**: `plist data`, 16 bytes

**Default**: Empty

**Failsafe**: All zero

**Description**: Sequence of `EAX`, `EBX`, `ECX`, `EDX` values to replace `CPUID (1)` call in XNU kernel.

This property primarily meets three requirements:
* Enabling support for an unsupported CPU model (e.g. Intel Pentium).
* Enabling support for a CPU model not yet supported by a specific version of macOS (typically old versions).
* Enabling XCPM support for an unsupported CPU variant. 

*Note 1*: It may also be the case that the CPU model is supported but there is no power management supported (e.g. virtual machines). In this case, `MinKernel` and `MaxKernel` can be set to restrict CPU virtualisation and dummy power management patches to the particular macOS kernel version.

*Note 2*: Only the value of `EAX`, which represents the full CPUID, typically needs to be accounted for and remaining bytes should be left as zeroes. The byte order is Little Endian. For example, `C3 06 03 00` stands for CPUID `0x0306C3` (Haswell).

*Note 3*: For XCPM support it is recommended to use the following combinations. Be warned that one is required to set the correct [frequency vectors](https://github.com/dortania/bugtracker/issues/190) matching the installed CPU.
* Haswell-E (`0x0306F2`) to Haswell (`0x0306C3`):
  * `Cpuid1Data`: `C3 06 03 00 00 00 00 00 00 00 00 00 00 00 00 00`
  * `Cpuid1Mask`: `FF FF FF FF 00 00 00 00 00 00 00 00 00 00 00 00`
* Broadwell-E (`0x0406F1`) to Broadwell (`0x0306D4`):
  * `Cpuid1Data`: `D4 06 03 00 00 00 00 00 00 00 00 00 00 00 00 00`
  * `Cpuid1Mask`: `FF FF FF FF 00 00 00 00 00 00 00 00 00 00 00 00`
* Comet Lake U62 (`0x0A0660`) to Comet Lake U42 (`0x0806EC`):
  * `Cpuid1Data`: `EC 06 08 00 00 00 00 00 00 00 00 00 00 00 00 00`
  * `Cpuid1Mask`: `FF FF FF FF 00 00 00 00 00 00 00 00 00 00 00 00`
* Rocket Lake (`0x0A0670`) to Comet Lake (`0x0A0655`):
  * `Cpuid1Data`: `55 06 0A 00 00 00 00 00 00 00 00 00 00 00 00 00`
  * `Cpuid1Mask`: `FF FF FF FF 00 00 00 00 00 00 00 00 00 00 00 00`
* Alder Lake (`0x090672`) to Comet Lake (`0x0A0655`):
  * `Cpuid1Data`: `55 06 0A 00 00 00 00 00 00 00 00 00 00 00 00 00`
  * `Cpuid1Mask`: `FF FF FF FF 00 00 00 00 00 00 00 00 00 00 00 00` 

*Note 4*: Be aware that the following configurations are unsupported by XCPM (at least out of the box):
* Consumer Ivy Bridge (`0x0306A9`) as Apple disabled XCPM for Ivy Bridge and recommends legacy power management for these CPUs. `_xcpm_bootstrap` should manually be patched to enforce XCPM on these CPUs instead of this option.
* Low-end CPUs (e.g. Haswell+ Pentium) as they are not supported properly by macOS. Legacy workarounds for older models can be found in the `Special NOTES` section of [acidanthera/bugtracker#365](https://github.com/acidanthera/bugtracker/issues/365).

<h3 id=kernel-emulate-cpuid1mask>Kernel -> Emulate -> Cpuid1Mask</h3>

**Type**: `plist data`, 16 bytes

**Default**: Empty

**Failsafe**: All zero

**Description**: Bit mask of active bits in `Cpuid1Data`.

When each `Cpuid1Mask` bit is set to 0, the original CPU bit is used, otherwise set bits take the value of `Cpuid1Data`.

<h3 id=kernel-emulate-dummypowermanagement>Kernel -> Emulate -> DummyPowerManagement</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.4-12

**Description**: Disables `AppleIntelCpuPowerManagement`.

*Note 1*: This option is a preferred alternative to `NullCpuPowerManagement.kext` for CPUs without native power management driver in macOS.

*Note 2*: While this option is typically needed to disable `AppleIntelCpuPowerManagement` on unsupported platforms, it can also be used to disable this kext in other situations (e.g. with `Cpuid1Data` left blank).

<h3 id=kernel-emulate-maxkernel>Kernel -> Emulate -> MaxKernel</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Emulates CPUID and applies `DummyPowerManagement` on specified macOS version or older.

*Note*: Refer to the **`Add MaxKernel` description** for matching logic.

<h3 id=kernel-emulate-minkernel>Kernel -> Emulate -> MinKernel</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Emulates CPUID and applies `DummyPowerManagement` on specified macOS version or newer.

*Note*: Refer to the **`Add MaxKernel` description** for matching logic.

<h2 id=kernel-force>Kernel -> Force</h2>

**Type**: `plist array`

**Failsafe**: Empty

**Description**: Load kernel extensions (kexts) from the system volume if they are not cached.

To be filled with `plist dict` values, describing each kext. Refer to the **Force Properties** section below for details. This section resolves the problem of injecting kexts that depend on other kexts, which are not otherwise cached. The issue typically affects older operating systems, where various dependency kexts, such as `IOAudioFamily` or `IONetworkingFamily` may not be present in the kernel cache by default.

*Note 1*: The load order is based on the order in which the kexts appear in the array. Hence, dependencies must appear before kexts that depend on them.

*Note 2*: `Force` happens before `Add`.

*Note 3*: The signature of the `'forced'' kext is not checked in any way. This makes using this feature extremely dangerous and undesirable for secure boot.

*Note 4*: This feature may not work on encrypted partitions in newer operating systems.

<h3 id=kernel-force-arch>Kernel -> Force[] -> Arch</h3>

**Type**: `plist string`

**Default**: `Any`

**Failsafe**: `Any` (Apply to any supported architecture)

**Description**: Kext architecture (`i386`, `x86_64`).

<h3 id=kernel-force-bundlepath>Kernel -> Force[] -> BundlePath</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Kext bundle path (e.g. `System\Library \Extensions \IONetworkingFamily.kext`).

<h3 id=kernel-force-comment>Kernel -> Force[] -> Comment</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Arbitrary ASCII string used to provide human readable reference for the entry. Whether this value is used is implementation defined.

<h3 id=kernel-force-enabled>Kernel -> Force[] -> Enabled</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Set to `true` to load this kernel extension from the system volume when not present in the kernel cache.

<h3 id=kernel-force-executablepath>Kernel -> Force[] -> ExecutablePath</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Kext executable path relative to bundle (e.g. `Contents/MacOS/IONetworkingFamily`).

<h3 id=kernel-force-identifier>Kernel -> Force[] -> Identifier</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Kext identifier to perform presence checking before adding (e.g. `com.apple.iokit.IONetworkingFamily`). Only drivers which identifiers are not be found in the cache will be added.

<h3 id=kernel-force-maxkernel>Kernel -> Force[] -> MaxKernel</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Adds kernel extension on specified macOS version or older.

*Note*: Refer to the **`Add MaxKernel` description** for matching logic.

<h3 id=kernel-force-minkernel>Kernel -> Force[] -> MinKernel</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Adds kernel extension on specified macOS version or newer.

*Note*: Refer to the **`Add MaxKernel` description** for matching logic.

<h3 id=kernel-force-plistpath>Kernel -> Force[] -> PlistPath</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Kext `Info.plist` path relative to bundle (e.g. `Contents/Info.plist`).

<h2 id=kernel-patch>Kernel -> Patch</h2>

**Type**: `plist array`

**Failsafe**: Empty

**Description**: Perform binary patches in kernel and drivers prior to driver addition and removal.

To be filled with `plist dictionary` values, describing each patch. Refer to the **Patch Properties** section below for details.

<h3 id=kernel-patch-arch>Kernel -> Patch[] -> Arch</h3>

**Type**: `plist string`

**Default**: `Any`

**Failsafe**: `Any` (Apply to any supported architecture)

**Description**: Kext patch architecture (`i386`, `x86_64`).

<h3 id=kernel-patch-base>Kernel -> Patch[] -> Base</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty (Ignored)

**Description**: Selects symbol-matched base for patch lookup (or immediate replacement) by obtaining the address of the provided symbol name.

<h3 id=kernel-patch-comment>Kernel -> Patch[] -> Comment</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Arbitrary ASCII string used to provide human readable reference for the entry. Whether this value is used is implementation defined.

<h3 id=kernel-patch-count>Kernel -> Patch[] -> Count</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0`

**Description**: Number of patch occurrences to apply. `0` applies the patch to all occurrences found.

<h3 id=kernel-patch-enabled>Kernel -> Patch[] -> Enabled</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: This kernel patch will not be used unless set to `true`.

<h3 id=kernel-patch-find>Kernel -> Patch[] -> Find</h3>

**Type**: `plist data`

**Default**: Empty

**Failsafe**: Empty (Immediate replacement at `Base`)

**Description**: Data to find. Must be equal to `Replace` in size if set.

<h3 id=kernel-patch-identifier>Kernel -> Patch[] -> Identifier</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Kext bundle identifier (e.g. `com.apple.driver.AppleHDA`) or `kernel` for kernel patch.

<h3 id=kernel-patch-limit>Kernel -> Patch[] -> Limit</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0` (Search entire kext or kernel)

**Description**: Maximum number of bytes to search for.

<h3 id=kernel-patch-mask>Kernel -> Patch[] -> Mask</h3>

**Type**: `plist data`

**Default**: Empty

**Failsafe**: Empty (Ignored)

**Description**: Data bitwise mask used during find comparison. Allows fuzzy search by ignoring not masked (set to zero) bits. Must be equal to `Replace` in size if set.

<h3 id=kernel-patch-maxkernel>Kernel -> Patch[] -> MaxKernel</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Patches data on specified macOS version or older.

*Note*: Refer to the **`Add MaxKernel` description** for matching logic.

<h3 id=kernel-patch-minkernel>Kernel -> Patch[] -> MinKernel</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Patches data on specified macOS version or newer.

*Note*: Refer to the **`Add MaxKernel` description** for matching logic.

<h3 id=kernel-patch-replace>Kernel -> Patch[] -> Replace</h3>

**Type**: `plist data`

**Default**: Empty

**Failsafe**: Empty

**Description**: Replacement data of one or more bytes.

<h3 id=kernel-patch-replacemask>Kernel -> Patch[] -> ReplaceMask</h3>

**Type**: `plist data`

**Default**: Empty

**Failsafe**: Empty (Ignored)

**Description**: Data bitwise mask used during replacement. Allows fuzzy replacement by updating masked (set to non-zero) bits. Must be equal to `Replace` in size if set.

<h3 id=kernel-patch-skip>Kernel -> Patch[] -> Skip</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0` (Do not skip any occurrences)

**Description**: Number of found occurrences to skip before replacements are applied.

<h2 id=kernel-quirks>Kernel -> Quirks</h2>

**Type**: `plist dict`

**Description**: Apply individual kernel and driver quirks described in the **Quirks Properties** section below.

<h3 id=kernel-quirks-applecpupmcfglock>Kernel -> Quirks -> AppleCpuPmCfgLock</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.4

**Description**: Disables `PKG_CST_CONFIG_CONTROL` (`0xE2`) MSR modification in AppleIntelCPUPowerManagement.kext, commonly causing early kernel panic, when it is locked from writing.

*Note*: AppleIntelCPUPowerManagement.kext is removed as of macOS 13. However, a legacy version can be injected and thus get patched using this quirk.

Some types of firmware lock the `PKG_CST_CONFIG_CONTROL` MSR register and the bundled `ControlMsrE2` tool can be used to check its state. Note that some types of firmware only have this register locked on some cores. As modern firmware provide a `CFG Lock` setting that allows configuring the `PKG_CST_CONFIG_CONTROL` MSR register lock, this option should be avoided whenever possible.

On APTIO firmware that do not provide a `CFG Lock` setting in the GUI, it is possible to access the option directly:

\begin{enumerate}
* Download [UEFITool](https://github.com/LongSoft/UEFITool/releases) and [IFR-Extractor](https://github.com/LongSoft/Universal-IFR-Extractor/releases).
* Open the firmware image in UEFITool and find `CFG Lock` unicode string. If it is not present, the firmware may not have this option and the process should therefore be discontinued.
* Extract the `Setup.bin` PE32 Image Section (the UEFITool found) through the `Extract Body` menu option.
* Run IFR-Extractor on the extracted file (e.g. `./ifrextract Setup.bin Setup.txt`).
* Find `CFG Lock, VarStoreInfo (VarOffset/VarName):` in `Setup.txt` and remember the offset right after it (e.g. `0x123`).
* Download and run [Modified GRUB Shell](http://brains.by/posts/bootx64.7z) compiled by [brainsucker](https://habr.com/geektimes/post/258090) or use [a newer version](https://github.com/datasone/grub-mod-setup_var) by [datasone](https://github.com/datasone).
* Enter `setup_var 0x123 0x00` command, where `0x123` should be replaced by the actual offset, and reboot. \end{enumerate}

**Warning**: Variable offsets are unique not only to each motherboard but even to its firmware version. Never ever try to use an offset without checking.

On selected platforms, the `ControlMsrE2` tool can also change such hidden options. Pass desired argument: `lock`, `unlock` for `CFG Lock`. Or pass `interactive` to find and modify other hidden options.

As a last resort, consider [patching the BIOS](https://github.com/LongSoft/UEFITool/blob/master/UEFIPatch/patches.txt) (for advanced users only).

<h3 id=kernel-quirks-applexcpmcfglock>Kernel -> Quirks -> AppleXcpmCfgLock</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.8 (not required for older)

**Description**: Disables `PKG_CST_CONFIG_CONTROL` (`0xE2`) MSR modification in XNU kernel, commonly causing early kernel panic, when it is locked from writing (XCPM power management).

*Note*: This option should be avoided whenever possible. Refer to the `AppleCpuPmCfgLock` description for details.

<h3 id=kernel-quirks-applexcpmextramsrs>Kernel -> Quirks -> AppleXcpmExtraMsrs</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.8 (not required for older)

**Description**: Disables multiple MSR access critical for certain CPUs, which have no native XCPM support.

This is typically used in conjunction with the `Emulate` section on Haswell-E, Broadwell-E, Skylake-SP, and similar CPUs. More details on the XCPM patches are outlined in [acidanthera/bugtracker#365](https://github.com/acidanthera/bugtracker/issues/365).

*Note*: Additional not provided patches will be required for Ivy Bridge or Pentium CPUs. It is recommended to use `AppleIntelCpuPowerManagement.kext` for the former.

<h3 id=kernel-quirks-applexcpmforceboost>Kernel -> Quirks -> AppleXcpmForceBoost</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.8 (not required for older)

**Description**: Forces maximum performance in XCPM mode.

This patch writes `0xFF00` to `MSR_IA32_PERF_CONTROL` (`0x199`), effectively setting maximum multiplier for all the time.

*Note*: While this may increase the performance, this patch is strongly discouraged on all systems but those explicitly dedicated to scientific or media calculations. Only certain Xeon models typically benefit from the patch.

<h3 id=kernel-quirks-custompciserialdevice>Kernel -> Quirks -> CustomPciSerialDevice</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.7

**Description**: Performs change of PMIO register base address on a customised PCI serial device.

The patch changes the PMIO register base address that the XNU kernel uses for serial input and output, from that of the default built-in COM1 serial port `0x3F8`, to the base address stored in the first IO BAR of a specified PCI device or to a specific base address (e.g. `0x2F8` for COM2).

*Note*: By default, serial logging is disabled. `serial=3` boot argument, which enables serial input and output, should be used for XNU to print logs to the serial port.

*Note 2*: In addition to this patch, kext `Apple16X50PCI0` should be prevented from attaching to have `kprintf` method working properly. This can be achieved by using [PCIeSerialDisable](https://github.com/joevt/PCIeSerialDisable). In addition, for certain Thunderbolt cards the IOKit personality `IOPCITunnelCompatible` also needs to be set to `true`, which can be done by the `PCIeSerialThunderboltEnable.kext` attached at [acidanthera/bugtracker#2003](https://github.com/acidanthera/bugtracker/issues/2003#issuecomment-1116761087).

*Note 3*: For this patch to be correctly applied, `Override` must be enabled with all keys properly set in `Custom`, under section `Misc->Serial`.

*Note 4*: This patch is for PMIO support and is therefore not applied if `UseMmio` under section `Misc->Serial->Custom` is false. For MMIO, there are boot arguments `pcie_mmio_uart=ADDRESS` and `mmio_uart=ADDRESS` that allow the kernel to use MMIO for serial port access.

*Note 5*: The serial baud rate must be correctly set in both `BaudRate` under section `Misc->Serial->Custom` and via `serialbaud=VALUE` boot argument, both of which should match against each other. The default baud rate is `115200`.

<h3 id=kernel-quirks-customsmbiosguid>Kernel -> Quirks -> CustomSMBIOSGuid</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.4

**Description**: Performs GUID patching for `UpdateSMBIOSMode` `Custom` mode. Usually relevant for Dell laptops.

<h3 id=kernel-quirks-disableiomapper>Kernel -> Quirks -> DisableIoMapper</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.8 (not required for older)

**Description**: Disables `IOMapper` support in XNU (VT-d), which may conflict with the firmware implementation.

*Note 1*: This option is a preferred alternative to deleting `DMAR` ACPI table and disabling VT-d in firmware preferences, which does not obstruct VT-d support in other systems in case they need this.

*Note 2*: Misconfigured IOMMU in the firmware may result in broken devices such as ethernet or Wi-Fi adapters. For instance, an ethernet adapter may cycle in link-up link-down state infinitely and a Wi-Fi adapter may fail to discover networks. Gigabyte is one of the most common OEMs with these issues.

<h3 id=kernel-quirks-disableiomappermapping>Kernel -> Quirks -> DisableIoMapperMapping</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 13.3 (not required for older)

**Description**: Disables mapping PCI bridge device memory in IOMMU (VT-d).

This option resolves compatibility issues with Wi-Fi, Ethernet and Thunderbolt devices when AppleVTD is enabled on systems where the native DMAR table contains one or more Reserved Memory Regions and more than 16 GB memory is installed. On some systems, this quirk is only needed when iGPU is enabled.

*Note 1*: This quirk requires a native DMAR table that does not contain Reserved Memory Regions or a substitute SSDT-DMAR.aml in which Reserved Memory Regions have been removed.

*Note 2*: This option is not needed on AMD systems.

<h3 id=kernel-quirks-disablelinkeditjettison>Kernel -> Quirks -> DisableLinkeditJettison</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Requirement**: 11

**Description**: Disables `__LINKEDIT` jettison code.

This option lets `Lilu.kext`, and possibly other kexts, function in macOS Big Sur at their best performance levels without requiring the `keepsyms=1` boot argument.

<h3 id=kernel-quirks-disablertcchecksum>Kernel -> Quirks -> DisableRtcChecksum</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.4

**Description**: Disables primary checksum (`0x58`-`0x59`) writing in AppleRTC.

*Note 1*: This option will not protect other areas from being overwritten, see [RTCMemoryFixup](https://github.com/acidanthera/RTCMemoryFixup) kernel extension if this is desired.

*Note 2*: This option will not protect areas from being overwritten at firmware stage (e.g. macOS bootloader), see `AppleRtcRam` protocol description if this is desired.

<h3 id=kernel-quirks-extendbtfeatureflags>Kernel -> Quirks -> ExtendBTFeatureFlags</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.8-11

**Description**: Set `FeatureFlags` to `0x0F` for full functionality of Bluetooth, including Continuity.

*Note*: This option is a substitution for BT4LEContinuityFixup.kext, which does not function properly due to late patching progress.

<h3 id=kernel-quirks-externaldiskicons>Kernel -> Quirks -> ExternalDiskIcons</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.4

**Description**: Apply icon type patches to AppleAHCIPort.kext to force internal disk icons for all AHCI disks.

*Note*: This option should be avoided whenever possible. Modern firmware typically have compatible AHCI controllers.

<h3 id=kernel-quirks-forceaquantiaethernet>Kernel -> Quirks -> ForceAquantiaEthernet</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.15.4

**Description**: Enable Aquantia AQtion based 10GbE network cards support.

This option enables Aquantia AQtion based 10GbE network cards support, which used to work natively before macOS 10.15.4.

*Note*: In order for Aquantia cards to properly function, `DisableIoMapper` must be disabled, `DMAR` ACPI table must not be dropped, and `VT-d` must be enabled in BIOS.

*Note 2*: While this patch should enable ethernet support for all Aquantia AQtion series, it has only been tested on AQC-107s based 10GbE network cards.

*Note 3*: To address `AppleVTD` incompatibilities after applying this quirk, the `Reserved Memory Region` section of the corresponding device in the `DMAR` ACPI table might be removed. This table should be disassembled and edited, then recompiled to `AML` with tool `iASL`. For the patched `DMAR` table to be **added**, the original one should be **deleted**. More details can be found at [comment on commit 2441455](https://github.com/acidanthera/OpenCorePkg/commit/24414555f2c07e06a3674ec7a2aa1ce4860bbcc7#commitcomment-70530145).

<h3 id=kernel-quirks-forcesecurebootscheme>Kernel -> Quirks -> ForceSecureBootScheme</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 11

**Description**: Force `x86` scheme for IMG4 verification.

*Note*: This option is required on virtual machines when using `SecureBootModel` different from `x86legacy`.

<h3 id=kernel-quirks-increasepcibarsize>Kernel -> Quirks -> IncreasePciBarSize</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.10

**Description**: Allows IOPCIFamily to boot with 2 GB PCI BARs.

Normally macOS restricts PCI BARs to 1 GB. Enabling this option (still) does not let macOS actually use PCI devices with larger BARs.

*Note*: This option should be avoided whenever possible. A need for this option indicates misconfigured or defective firmware.

<h3 id=kernel-quirks-lapickernelpanic>Kernel -> Quirks -> LapicKernelPanic</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.6 (64-bit)

**Description**: Disables kernel panic on LAPIC interrupts.

<h3 id=kernel-quirks-legacycommpage>Kernel -> Quirks -> LegacyCommpage</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.4 - 10.6

**Description**: Replaces the default 64-bit commpage bcopy implementation with one that does not require SSSE3, useful for legacy platforms. This prevents a `commpage no match for last` panic due to no available 64-bit bcopy functions that do not require SSSE3.

<h3 id=kernel-quirks-panicnokextdump>Kernel -> Quirks -> PanicNoKextDump</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.13 (not required for older)

**Description**: Prevent kernel from printing kext dump in the panic log preventing from observing panic details. Affects 10.13 and above.

<h3 id=kernel-quirks-powertimeoutkernelpanic>Kernel -> Quirks -> PowerTimeoutKernelPanic</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.15 (not required for older)

**Description**: Disables kernel panic on setPowerState timeout.

An additional security measure was added to macOS Catalina (10.15) causing kernel panic on power change timeout for Apple drivers. Sometimes it may cause issues on misconfigured hardware, notably digital audio, which sometimes fails to wake up. For debug kernels `setpowerstate_panic=0` boot argument should be used, which is otherwise equivalent to this quirk.

<h3 id=kernel-quirks-providecurrentcpuinfo>Kernel -> Quirks -> ProvideCurrentCpuInfo</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.4 (10.14)

**Description**: Provides current CPU info to the kernel.

This quirk works differently depending on the CPU:
* For Microsoft Hyper-V it provides the correct TSC and FSB values to the kernel, as well as disables CPU topology validation (10.8+).
* For KVM and other hypervisors it provides precomputed MSR 35h values solving kernel panic with `-cpu host`.
* For Intel CPUs it adds support for asymmetrical SMP systems (e.g. Intel Alder Lake) by patching core count to thread count along with the supplemental required changes (10.14+). Cache size and cache line size are also provided when using 10.4 as Intel Penryn and newer may only have cache information in CPUID leaf 0x4 which is unsupported by 10.4.

<h3 id=kernel-quirks-setapfstrimtimeout>Kernel -> Quirks -> SetApfsTrimTimeout</h3>

**Type**: `plist integer`

**Default**: `-1`

**Failsafe**: `-1`

**Requirement**: 10.14 (not required for older)

**Description**: Set trim timeout in microseconds for APFS filesystems on SSDs.

The APFS filesystem is designed in a way that the space controlled via the spaceman structure is either used or free. This may be different in other filesystems where the areas can be marked as used, free, and *unmapped*. All free space is trimmed (unmapped/deallocated) at macOS startup. The trimming procedure for NVMe drives happens in LBA ranges due to the nature of the `DSM` command with up to 256 ranges per command. The more fragmented the memory on the drive is, the more commands are necessary to trim all the free space.

Depending on the SSD controller and the level of drive fragmenation, the trim procedure may take a considerable amount of time, causing noticeable boot slowdown. The APFS driver explicitly ignores previously unmapped areas and repeatedly trims them on boot. To mitigate against such boot slowdowns, the macOS driver introduced a timeout (`9.999999` seconds) that stops the trim operation when not finished in time.

On several controllers, such as Samsung, where the deallocation process is relatively slow, this timeout can be reached very quickly. Essentially, it means that the level of fragmentation is high, thus macOS will attempt to trim the same lower blocks that have previously been deallocated, but never have enough time to deallocate higher blocks. The outcome is that trimming on such SSDs will be non-functional soon after installation, resulting in additional wear on the flash.

One way to workaround the problem is to increase the timeout to an extremely high value, which at the cost of slow boot times (extra minutes) will ensure that all the blocks are trimmed. Setting this option to a high value, such as `4294967295` ensures that all blocks are trimmed. Alternatively, use over-provisioning, if supported, or create a dedicated unmapped partition where the reserve blocks can be found by the controller. Conversely, the trim operation can be mostly disabled by setting a very low timeout value, while `0` entirely disables it. Refer to this [article](https://interface31.ru/tech_it/2015/04/mozhno-li-effektivno-ispolzovat-ssd-bez-podderzhki-trim.html) for details.

*Note*: The failsafe value `-1` indicates that this patch will not be applied, such that `apfs.kext` will remain untouched.

*Note 2*: On macOS 12.0 and above, it is no longer possible to specify trim timeout. However, trim can be disabled by setting `0`.

*Note 3*: Trim operations are *only* affected at booting phase when the startup volume is mounted. Either specifying timeout, or completely disabling trim with `0`, will not affect normal macOS running.

<h3 id=kernel-quirks-thirdpartydrives>Kernel -> Quirks -> ThirdPartyDrives</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.6 (not required for older)

**Description**: Apply vendor patches to IOAHCIBlockStorage.kext to enable native features for third-party drives, such as TRIM on SSDs or hibernation support on 10.15 and newer.

*Note*: This option may be avoided on user preference. NVMe SSDs are compatible without the change. For AHCI SSDs on modern macOS version there is a dedicated built-in utility called `trimforce`. Starting from 10.15 this utility creates `EnableTRIM` variable in `APPLE_BOOT_VARIABLE_GUID` namespace with `01 00 00 00` value.

<h3 id=kernel-quirks-xhciportlimit>Kernel -> Quirks -> XhciPortLimit</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Requirement**: 10.11 (not required for older)

**Description**: Patch various kexts (AppleUSBXHCI.kext, AppleUSBXHCIPCI.kext, IOUSBHostFamily.kext) to remove USB port count limit of 15 ports.

*Note*: This option should be avoided whenever possible. USB port limit is imposed by the amount of used bits in locationID format and there is no possible way to workaround this without heavy OS modification. The only valid solution is to limit the amount of used ports to 15 (discarding some). More details can be found on [AppleLife.ru](https://applelife.ru/posts/550233).

<h2 id=kernel-scheme>Kernel -> Scheme</h2>

**Type**: `plist dict`

**Description**: Define kernelspace operation mode via parameters described in the **Scheme Properties** section below.

<h3 id=kernel-scheme-customkernel>Kernel -> Scheme -> CustomKernel</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Use customised kernel cache from the `Kernels` directory located at the root of the ESP partition.

Unsupported platforms including `Atom` and `AMD` require modified versions of XNU kernel in order to boot. This option provides the possibility to using a customised kernel cache which contains such modifications from ESP partition.

<h3 id=kernel-scheme-fuzzymatch>Kernel -> Scheme -> FuzzyMatch</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Use `kernelcache` with different checksums when available.

On macOS 10.6 and earlier, `kernelcache` filename has a checksum, which essentially is `adler32` from SMBIOS product name and EfiBoot device path. On certain firmware, the EfiBoot device path differs between UEFI and macOS due to ACPI or hardware specifics, rendering `kernelcache` checksum as always different.

This setting allows matching the latest `kernelcache` with a suitable architecture when the `kernelcache` without suffix is unavailable, improving macOS 10.6 boot performance on several platforms.

<h3 id=kernel-scheme-kernelarch>Kernel -> Scheme -> KernelArch</h3>

**Type**: `plist string`

**Default**: `Auto`

**Failsafe**: `Auto` (Choose the preferred architecture automatically)

**Description**: Prefer specified kernel architecture (`i386`, `i386-user32`, `x86_64`) when available.

On macOS 10.7 and earlier, the XNU kernel can boot with architectures different from the usual `x86_64`. This setting will use the specified architecture to boot macOS when it is supported by the macOS and the configuration:
* `i386` --- Use `i386` (32-bit) kernel when available.
* `i386-user32` --- Use `i386` (32-bit) kernel when available and force the use of 32-bit userspace on 64-bit capable processors if supported by the operating system.
* On macOS, 64-bit capable processors are assumed to support `SSSE3`. This is not the case for older 64-bit capable Pentium processors, which cause some applications to crash on macOS~10.6. This behaviour corresponds to the `-legacy` kernel boot argument.
* This option is unavailable on macOS~10.4 and 10.5 when running on 64-bit firmware due to an uninitialised 64-bit segment in the XNU kernel, which causes AppleEFIRuntime to incorrectly execute 64-bit code as 16-bit code. 
* `x86_64` --- Use `x86_64` (64-bit) kernel when available. 

The algorithm used to determine the preferred kernel architecture is set out below.

\begin{enumerate}
* `arch` argument in image arguments (e.g. when launched via UEFI Shell) or in `boot-args` variable overrides any compatibility checks and forces the specified architecture, completing this algorithm.
* OpenCore build architecture restricts capabilities to `i386` and `i386-user32` mode for the 32-bit firmware variant.
* Determined EfiBoot version restricts architecture choice:
* 10.4-10.5 --- `i386` or `i386-user32` (only on 32-bit firmware)
* 10.6 --- `i386`, `i386-user32`, or `x86_64`
* 10.7 --- `i386` or `x86_64`
* 10.8 or newer --- `x86_64` 
* If `KernelArch` is set to `Auto` and `SSSE3` is not supported by the CPU, capabilities are restricted to `i386-user32` if supported by EfiBoot.
* Board identifier (from SMBIOS) based on EfiBoot version disables `x86_64` support on an unsupported model if any `i386` variant is supported. `Auto` is not consulted here as the list is not overridable in EfiBoot.
* `KernelArch` restricts the support to the explicitly specified architecture (when not set to `Auto`) if the architecture remains present in the capabilities.
* The best supported architecture is chosen in this order: `x86_64`, `i386`, `i386-user32`. \end{enumerate}

Unlike macOS~10.7 (where certain board identifiers are treated as the `i386` only machines), and macOS~10.5 or earlier (where `x86_64` is not supported by the macOS kernel), macOS~10.6 is very special. The architecture choice on macOS~10.6 depends on many factors including not only the board identifier, but also the macOS product type (client vs server), macOS point release, and amount of RAM. The detection of all these is complicated and impractical, as several point releases had implementation flaws resulting in a failure to properly execute the server detection in the first place. For this reason, OpenCore on macOS~10.6 falls back on the `x86_64` architecture whenever it is supported by the board, as it is on macOS~10.7.

A 64-bit Mac model compatibility matrix corresponding to actual EfiBoot behaviour on macOS 10.6.8 and 10.7.5 is outlined below.

\begin{center} \begin{tabular}{|p{0.9in}|c|c|c|c|} \hline **Model** & **10.6 (minimal)** & **10.6 (client)** & **10.6 (server)** & **10.7 (any)** \\hline Macmini & 4,x (Mid 2010) & 5,x (Mid 2011) & 4,x (Mid 2010) & 3,x (Early 2009) \\hline MacBook & Unsupported & Unsupported & Unsupported & 5,x (2009/09) \\hline MacBookAir & Unsupported & Unsupported & Unsupported & 2,x (Late 2008) \\hline MacBookPro & 4,x (Early 2008) & 8,x (Early 2011) & 8,x (Early 2011) & 3,x (Mid 2007) \\hline iMac & 8,x (Early 2008) & 12,x (Mid 2011) & 12,x (Mid 2011) & 7,x (Mid 2007) \\hline MacPro & 3,x (Early 2008) & 5,x (Mid 2010) & 3,x (Early 2008) & 3,x (Early 2008) \\hline Xserve & 2,x (Early 2008) & 2,x (Early 2008) & 2,x (Early 2008) & 2,x (Early 2008) \\hline \end{tabular} \end{center}

*Note*: `3+2` and `6+4` hotkeys to choose the preferred architecture are unsupported as they are handled by EfiBoot and hence, difficult to detect.

<h3 id=kernel-scheme-kernelcache>Kernel -> Scheme -> KernelCache</h3>

**Type**: `plist string`

**Default**: `Auto`

**Failsafe**: `Auto`

**Description**: Prefer specified kernel cache type (`Auto`, `Cacheless`, `Mkext`, `Prelinked`) when available.

Different variants of macOS support different kernel caching variants designed to improve boot performance. This setting prevents the use of faster kernel caching variants if slower variants are available for debugging and stability reasons. That is, by specifying `Mkext`, `Prelinked` will be disabled for e.g. 10.6 but not for 10.7.

The list of available kernel caching types and its current support in OpenCore is listed below.

\begin{center} \begin{tabular}{|p{0.67in}|c|c|c|c|c|c|c|} \hline **macOS** & **i386 NC** & **i386 MK** & **i386 PK** & **x86_64 NC** & **x86_64 MK** & **x86_64 PK** & **x86_64 KC** \\hline 10.4 & YES & YES (V1) & NO (V1) & --- & --- & --- & --- \\hline 10.5 & YES & YES (V1) & NO (V1) & --- & --- & --- & --- \\hline 10.6 & YES & YES (V2) & YES (V2) & YES & YES (V2) & YES (V2) & --- \\hline 10.7 & YES & --- & YES (V3) & YES & --- & YES (V3) & --- \\hline 10.8-10.9 & --- & --- & --- & YES & --- & YES (V3) & --- \\hline 10.10-10.15 & --- & --- & --- & --- & --- & YES (V3) & --- \\hline 11+ & --- & --- & --- & --- & --- & YES (V3) & YES \\hline \end{tabular} \end{center}

*Note*: The first version (V1) of the 32-bit `prelinkedkernel` is unsupported due to the corruption of kext symbol tables by the tools. On this version, the `Auto` setting will block `prelinkedkernel` booting. This also results in the `keepsyms=1` boot argument being non-functional for kext frames on these systems.

<h2 id=misc-blessoverride>Misc -> BlessOverride</h2>

**Type**: `plist array`

**Default**: Empty

**Failsafe**: Empty

**Description**: Add custom scanning paths through the bless model.

To be filled with `plist string` entries containing absolute UEFI paths to customised bootloaders such as `\EFI\debian\grubx64.efi` for the Debian bootloader. This allows non-standard boot paths to be automatically discovered by the OpenCore picker. Designwise, they are equivalent to predefined blessed paths, such as `\System\Library\CoreServices\boot.efi` or `\EFI\Microsoft\Boot\bootmgfw.efi`, but unlike predefined bless paths, they have the highest priority.

<h2 id=misc-boot>Misc -> Boot</h2>

**Type**: `plist dict`

**Description**: Apply the boot configuration described in the **Boot Properties** section below.

<h3 id=misc-boot-consoleattributes>Misc -> Boot -> ConsoleAttributes</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0`

**Description**: Sets specific attributes for the console.

The text renderer supports colour arguments as a sum of foreground and background colours based on the UEFI specification. The value for black background and for black foreground, `0`, is reserved.

List of colour values and names:
* `0x00` --- `EFI_BLACK`
* `0x01` --- `EFI_BLUE`
* `0x02` --- `EFI_GREEN`
* `0x03` --- `EFI_CYAN`
* `0x04` --- `EFI_RED`
* `0x05` --- `EFI_MAGENTA`
* `0x06` --- `EFI_BROWN`
* `0x07` --- `EFI_LIGHTGRAY`
* `0x08` --- `EFI_DARKGRAY`
* `0x09` --- `EFI_LIGHTBLUE`
* `0x0A` --- `EFI_LIGHTGREEN`
* `0x0B` --- `EFI_LIGHTCYAN`
* `0x0C` --- `EFI_LIGHTRED`
* `0x0D` --- `EFI_LIGHTMAGENTA`
* `0x0E` --- `EFI_YELLOW`
* `0x0F` --- `EFI_WHITE`
* `0x00` --- `EFI_BACKGROUND_BLACK`
* `0x10` --- `EFI_BACKGROUND_BLUE`
* `0x20` --- `EFI_BACKGROUND_GREEN`
* `0x30` --- `EFI_BACKGROUND_CYAN`
* `0x40` --- `EFI_BACKGROUND_RED`
* `0x50` --- `EFI_BACKGROUND_MAGENTA`
* `0x60` --- `EFI_BACKGROUND_BROWN`
* `0x70` --- `EFI_BACKGROUND_LIGHTGRAY` 

*Note*: This option may not work well with the `System` text renderer. Setting a background different from black could help with testing GOP functionality.

<h3 id=misc-boot-hibernatemode>Misc -> Boot -> HibernateMode</h3>

**Type**: `plist string`

**Default**: `None`

**Failsafe**: `None`

**Description**: Hibernation detection mode. The following modes are supported:
* `None` --- Ignore hibernation state.
* `Auto` --- Use RTC and NVRAM detection.
* `RTC` --- Use RTC detection.
* `NVRAM` --- Use NVRAM detection. 

*Note*: If the firmware can handle hibernation itself (valid for Mac EFI firmware), then `None` should be specified to hand-off hibernation state as is to OpenCore.

<h3 id=misc-boot-hibernateskipspicker>Misc -> Boot -> HibernateSkipsPicker</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Do not show picker if waking from macOS hibernation.

Limitations:
* Only supports macOS hibernation wake, Windows and Linux are currently out of scope.
* Should only be used on systems with reliable hibernation wake in macOS, otherwise users may notbe able to visually see boot loops that may occur.
* Highly recommended to pair this option with `PollAppleHotKeys`, allows to enter picker in case of issues with hibernation wake.
* Visual indication for hibernation wake is currently out of scope.

<h3 id=misc-boot-hideauxiliary>Misc -> Boot -> HideAuxiliary</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Set to `true` to hide auxiliary entries from the picker menu.

An entry is considered auxiliary when at least one of the following applies:
* Entry is macOS recovery.
* Entry is macOS Time Machine.
* Entry is explicitly marked as `Auxiliary`.
* Entry is system (e.g. `Reset NVRAM`). 

To display all entries, the picker menu can be reloaded into `'Extended Mode'' by pressing the `Spacebar` key. Hiding auxiliary entries may increase boot performance on multi-disk systems.

<h3 id=misc-boot-launcheroption>Misc -> Boot -> LauncherOption</h3>

**Type**: `plist string`

**Default**: `Disabled`

**Failsafe**: `Disabled`

**Description**: Register the launcher option in the firmware preferences for persistence.

Valid values:
* `Disabled` --- do nothing.
* `Full` --- create or update the top priority boot option in UEFI variable storage at bootloader startup.
* For this option to work, `RequestBootVarRouting` is required to be enabled. 
* `Short` --- create a short boot option instead of a complete one.
* This variant is useful for some older types of firmware, typically from Insyde, that are unable to manage full device paths. 
* `System` --- create no boot option but assume specified custom option is blessed.
* This variant is useful when relying on `ForceBooterSignature` quirk and OpenCore launcher path management happens through `bless` utilities without involving OpenCore.  \medskip 

This option allows integration with third-party operating system installation and upgrades (which may overwrite the `\EFI\BOOT\BOOTx64.efi` file). The BOOTx64.efi file is no longer used for bootstrapping OpenCore if a custom option is created. The custom path used for bootstrapping can be specified by using the `LauncherPath` option.

*Note 1*: Some types of firmware may have NVRAM implementation flaws, no boot option support, or other incompatibilities. While unlikely, the use of this option may result in boot failures and should only be used exclusively on boards known to be compatible. Refer to [acidanthera/bugtracker#1222](https://github.com/acidanthera/bugtracker/issues/1222) for some known issues affecting Haswell and other boards.

*Note 2*: While NVRAM resets executed from OpenCore would not typically erase the boot option created in `Bootstrap`, executing NVRAM resets prior to loading OpenCore will erase the boot option. Therefore, for significant implementation updates, such as was the case with OpenCore 0.6.4, an NVRAM reset should be executed with `Bootstrap` disabled, after which it can be re-enabled.

*Note 3*: Some versions of Intel Visual BIOS (e.g. on Intel NUC) have an unfortunate bug whereby if any boot option is added referring to a path on a USB drive, from then on that is the only boot option which will be shown when any USB drive is inserted. If OpenCore is started from a USB drive on this firmware with `LauncherOption` set to `Full` or `Short`, this applies and only the OpenCore boot entry will be seen afterwards, when any other USB is inserted (this highly non-standard BIOS behaviour affects other software as well). The best way to avoid this is to leave `LauncherOption` set to `Disabled` or `System` on any version of OpenCore which will be started from a USB drive on this firmware. If the problem has already occurred the quickest reliable fix is:
* Enable the system UEFI Shell in Intel Visual BIOS
* With power off, insert an OpenCore USB
* Power up and select the system UEFI Shell
* Since the system shell does not include `bcfg`, use the system shell to start OpenCore's OpenShell (e.g. by entering the command `FS2:\EFI\OC\Tools\OpenShell.efi` , but you will need to work out which drive is correct for OpenCore and modify the drive number `FS#:` accordingly)
* Within OpenShell, use `bcfg boot dump` to display the NVRAM boot options and then use `bcfg boot rm #` (where `#` is the number of the OpenCore boot entry) to remove the OpenCore entry  It is alternatively possible to start OpenShell directly from the OpenCore boot menu, if you have a working configured OpenCore for the system. In that case, and if OpenCore has `RequestBootVarRouting` enabled, it will be necessary to run the command `\EFI\OC\Tools\OpenControl.efi disable` before using `bcfg`. (After `OpenControl disable`, it is necessary to either reboot or run `OpenControl restore`, before booting an operating system.) It is also possible to use `efibootmgr` within Linux to remove the offending entry, if you have a working version of Linux on the machine. Linux must be started either not via OpenCore, or via OpenCore with `RequestBootVarRouting` disabled for this to work.

<h3 id=misc-boot-launcherpath>Misc -> Boot -> LauncherPath</h3>

**Type**: `plist string`

**Default**: `Default`

**Failsafe**: `Default`

**Description**: Launch path for the `LauncherOption` property.

`Default` points to `OpenCore.efi`. User specified paths, e.g. `\EFI\SomeLauncher.efi`, can be used to provide custom loaders, which are supposed to load `OpenCore.efi` themselves.

<h3 id=misc-boot-pickerattributes>Misc -> Boot -> PickerAttributes</h3>

**Type**: `plist integer`

**Default**: `17`

**Failsafe**: `0`

**Description**: Sets specific attributes for the OpenCore picker.

Different OpenCore pickers may be configured through the attribute mask containing OpenCore-reserved (`BIT0`\textasciitilde`BIT15`) and OEM-specific (`BIT16`\textasciitilde`BIT31`) values.

Current OpenCore values include:
* `0x0001` --- `OC_ATTR_USE_VOLUME_ICON`, provides custom icons for boot entries:

OpenCore will attempt loading a volume icon by searching as follows, and will fallback to the default icon on failure:
* `.VolumeIcon.icns` file at `Preboot` volume in per-volume directory(`/System/Volumes/Preboot/{GUID\`/} when mounted at the default location withinmacOS) for APFS (if present).
* `.VolumeIcon.icns` file at the `Preboot` volume root (`/System/Volumes/Preboot/`, when mounted at the default location within macOS) for APFS (otherwise).
* `.VolumeIcon.icns` file at the volume root for other filesystems.  \medskip

*Note 1*: The Apple picker partially supports placing a volume icon file at the operating system's `Data` volume root, `/System/Volumes/Data/`, when mounted at the default location within macOS. This approach is flawed: the file is neither accessible to OpenCanopy nor to the Apple picker when FileVault 2, which is meant to be the default choice, is enabled. Therefore, OpenCanopy does not attempt supporting Apple's approach. A volume icon file may be placed at the root of the `Preboot` volume for compatibility with both OpenCanopy and the Apple picker, or use the `Preboot` per-volume location as above with OpenCanopy as a preferred alternative to Apple's approach. \medskip

*Note 2*: Be aware that using a volume icon on any drive overrides the normal OpenCore picker behaviour for that drive of selecting the appropriate icon depending on whether the drive is internal or external. \medskip
* `0x0002` --- `OC_ATTR_USE_DISK_LABEL_FILE`, use custom prerendered titles for boot entries from `.disk_label` (`.disk_label_2x`) file next to the bootloader for all filesystems. These labels can be generated via the `disklabel` utility or the `bless -{`-folder {FOLDER_PATH} -{}-label {LABEL_TEXT}} command. When prerendered labels are disabled or missing, use label text in `.contentDetails` (or `.disk_label.contentDetails`) file next to bootloader if present instead, otherwise the entry name itself will be rendered.
* `0x0004` --- `OC_ATTR_USE_GENERIC_LABEL_IMAGE`, provides predefined label images for boot entries without custom entries. This may however give less detail for the actual boot entry.
* `0x0008` --- `OC_ATTR_HIDE_THEMED_ICONS`, prefers builtin icons for certain icon categories to match the theme style. For example, this could force displaying the builtin Time Machine icon. Requires `OC_ATTR_USE_VOLUME_ICON`.
* `0x0010` --- `OC_ATTR_USE_POINTER_CONTROL`, enables pointer control in the OpenCore picker when available. For example, this could make use of mouse or trackpad to control UI elements.
* `0x0020` --- `OC_ATTR_SHOW_DEBUG_DISPLAY`, enable display of additional timing and debug information, in Builtin picker in `DEBUG` and `NOOPT` builds only.
* `0x0040` --- `OC_ATTR_USE_MINIMAL_UI`, use minimal UI display, no Shutdown or Restart buttons, affects OpenCanopy and builtin picker.
* `0x0080` --- `OC_ATTR_USE_FLAVOUR_ICON`\label{oc-attr-use-flavour-icon}, provides flexible boot entry content description, suitable for picking the best media across different content sets:

When enabled, the entry icon in OpenCanopy and the audio assist entry sound in OpenCanopy and builtin boot picker are chosen by something called content flavour. To determine content flavour the following algorithm is used:
* For a Tool the value is read from `Flavour` field.
* For an automatically discovered entry, including for boot entry protocol entries such as those generated by the OpenLinuxBoot driver, it is read from the `.contentFlavour` file next to the bootloader, if present.
* For a custom entry specified in the `Entries` section it is read from the `.contentFlavour` file next to the bootloader if `Flavour` is `Auto`, otherwise it is specified via the `Flavour` value itself.
* If read flavour is `Auto` or there is no `.contentFlavour`, entry flavour is chosen based on the entry type (e.g. Windows automatically gets Windows flavour).  \medskip

The Flavour value is a sequence of `:` separated names limited to 64 characters of printable 7-bit ASCII. This is designed to support up to approximately five names. Each name refers to a flavour, with the first name having the highest priority and the last name having the lowest priority. Such a structure allows describing an entry in a more specific way, with icons selected flexibly depending on support by the audio-visual pack. A missing audio or icon file means the next flavour should be tried, and if all are missing the choice happens based on the type of the entry. Example flavour values: `BigSur:Apple`, `Windows10:Windows`. `OpenShell:UEFIShell:Shell`. \medskip

Using flavours means that you can switch between icon sets easily, with the flavour selecting the best available icons from each set. E.g. specifying icon flavour `Debian:Linux` will use the icon `Debian.icns` if provided, then will try `Linux.icns`, then will fall back to the default for an OS, which is `HardDrive.icns`. \medskip

Things to keep in mind:
* For security reasons `Ext<Flavour>.icns` and `<Flavour>.icns` are both supported, and only `Ext<Flavour>.icns` will be used if the entry is on an external drive (followed by default fallback `ExtHardDrive.icns`).
* Where both apply `.VolumeIcon.icns` takes precence over `.contentFlavour`.
* In order to allow icons and audio assist to work correctly for tools (e.g. for UEFI Shell), system default boot entry icons (see `Docs/Flavours.md`) specified in the `Flavour` setting for `Tools` or `Entries` will continue to apply even when flavour is disabled. Non-system icons will be ignored in thiscase. In addition, the flavours `UEFIShell` and `NVRAMReset` are given special processing, identifying their respective tools to apply correct audio-assist, default builtin labels, etc.
* A list of recommended flavours is provided in `Docs/Flavours.md`.  \medskip

<h3 id=misc-boot-pickeraudioassist>Misc -> Boot -> PickerAudioAssist</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Enable screen reader by default in the OpenCore picker.

For the macOS bootloader, screen reader preference is set in the `preferences.efires` archive in the `isVOEnabled.int32` file and is controlled by the operating system. For OpenCore screen reader support, this option is an independent equivalent. Toggling screen reader support in both the OpenCore picker and the macOS bootloader FileVault 2 login window can also be done by using the `Command` + `F5` key combination.

*Note*: The screen reader requires working audio support. Refer to the **`UEFI Audio Properties`** section for details.

<h3 id=misc-boot-pickermode>Misc -> Boot -> PickerMode</h3>

**Type**: `plist string`

**Default**: `Builtin`

**Failsafe**: `Builtin`

**Description**: Choose picker used for boot management.

`PickerMode` describes the underlying boot management with an optional user interface responsible for handling boot options.

The following values are supported:
* `Builtin` --- boot management is handled by OpenCore, a simple text-only user interface is used.
* `External` --- an external boot management protocol is used if available. Otherwise, the `Builtin` mode is used.
* `Apple` --- Apple boot management is used if available. Otherwise, the `Builtin` mode is used. 

Upon success, the `External` mode may entirely disable all boot management in OpenCore except for policy enforcement. In the `Apple` mode, it may additionally bypass policy enforcement. Refer to the **OpenCanopy** plugin for an example of a custom user interface.

The OpenCore built-in picker contains a set of actions chosen during the boot process. The list of supported actions is similar to Apple BDS and typically can be accessed by holding `action hotkeys` during the boot process.

The following actions are currently considered:
* `Default` --- this is the default option, and it lets the built-in OpenCore picker load the default boot option as specified in the [Startup Disk](https://support.apple.com/HT202796) preference pane.
* `ShowPicker` --- this option forces the OpenCore picker to be displayed. This can typically be achieved by holding the `OPT` key during boot. Setting `ShowPicker` to `true` will make `ShowPicker` the default option.
* `BootApple` --- this options performs booting to the first Apple operating system found unless the chosen default operating system is one from Apple. Hold the `X` key down to choose this option.
* `BootAppleRecovery` --- this option performs booting into the Apple operating system recovery partition. This is either that related to the default chosen operating system, or first one found when the chosen default operating system is not from Apple or does not have a recovery partition. Hold the `CMD+R` hotkey combination down to choose this option. 

*Note 1*: On non-Apple firmware `KeySupport`, `OpenUsbKbDxe`, or similar drivers are required for key handling. However, not all of the key handling functions can be implemented on several types of firmware.

*Note 2*: In addition to `OPT`, OpenCore supports using both the `Escape` and `Zero` keys to enter the OpenCore picker when `ShowPicker` is disabled. `Escape` exists to support co-existence with the Apple picker (including OpenCore `Apple` picker mode) and to support firmware that fails to report held `OPT` key, as on some PS/2 keyboards. In addition, `Zero` is provided to support systems on which `Escape` is already assigned to some other pre-boot firmware feature. In systems which do not require `KeySupport`, pressing and holding one of these keys from after power on until the picker appears should always be successful. The same should apply when using `KeySupport` mode if it is correctly configured for the system, i.e. with a long enough `KeyForgetThreshold`. If pressing and holding the key is not successful to reliably enter the picker, multiple repeated keypresses may be tried instead.

*Note 3*: On Macs with problematic GOP, it may be difficult to re-bless OpenCore if its bless status is lost. The `BootKicker` utility can be used to work around this problem, if set up as a Tool in OpenCore with `FullNvramAccess` enabled. It will launch the Apple picker, which allows selection of an item to boot next (with `Enter`), or next and from then on until the next change (with `CTRL+Enter`). Note that after the selection is made, the system *will reboot* before the chosen entry is booted. While this behaviour might seem surprising, it can be used both to switch which OpenCore installation is blessed, with `CTRL+Enter`, e.g. from a recovery OpenCore installation on CD (selected with the `C` key on boot) back to the main installion of OpenCore on the hard drive, if this is lost after an NVRAM reset. It can also be used, even when the native picker cannot be shown normally (unsupported GPU), to do a one-shot boot without OpenCore, e.g. to another OS or tool, or to an earlier version of macOS.

<h3 id=misc-boot-pickervariant>Misc -> Boot -> PickerVariant</h3>

**Type**: `plist string`

**Default**: `Auto`

**Failsafe**: `Auto`

**Description**: Choose specific icon set to be used for boot management.

An icon set is a directory path relative to `Resources\Image`, where the icons and an optional manifest are located. It is recommended for the artists to use provide their sets in the `Vendor\Set` format, e.g. `Acidanthera\GoldenGate`.

Sample resources provided as a part of [OcBinaryData repository](https://github.com/acidanthera/OcBinaryData) provide the following icon set:
* `Acidanthera\GoldenGate` --- macOS 11 styled icon set.
* `Acidanthera\Syrah` --- macOS 10.10 styled icon set.
* `Acidanthera\Chardonnay` --- macOS 10.4 styled icon set. 

For convenience purposes there also are predefined aliases:
* `Auto` --- Automatically select one set of icons based on the `DefaultBackground` colour: `Acidanthera\GoldenGate` for Syrah Black and `Acidanthera\Chardonnay` for Light Gray.
* `Default` --- `Acidanthera\GoldenGate`.

<h3 id=misc-boot-pollapplehotkeys>Misc -> Boot -> PollAppleHotKeys</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Enable `modifier hotkey` handling in the OpenCore picker.

In addition to `action hotkeys`, which are partially described in the `PickerMode` section and are typically handled by Apple BDS, modifier keys handled by the operating system bootloader (`boot.efi`) also exist. These keys allow changing the behaviour of the operating system by providing different boot modes.

On certain firmware, using modifier keys may be problematic due to driver incompatibilities. To workaround this problem, this option allows registering certain hotkeys in a more permissive manner from within the OpenCore picker. Such extensions include support for tapping on key combinations before selecting the boot item, and for reliable detection of the `Shift` key when selecting the boot item, in order to work around the fact that hotkeys which are continuously held during boot cannot be reliably detected on many PS/2 keyboards.

This list of known `modifier hotkeys` includes:
* `CMD+C+MINUS` --- disable board compatibility checking.
* `CMD+K` --- boot release kernel, similar to `kcsuffix=release`.
* `CMD+S` --- single user mode.
* `CMD+S+MINUS` --- disable KASLR slide, requires disabled SIP.
* `CMD+V` --- verbose mode.
* `Shift+Enter`, `Shift+Index` --- safe mode, may be used in combination with `CTRL+Enter`, `CTRL+Index`.

<h3 id=misc-boot-showpicker>Misc -> Boot -> ShowPicker</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Show a simple picker to allow boot entry selection.

<h3 id=misc-boot-takeoffdelay>Misc -> Boot -> TakeoffDelay</h3>

**Type**: `plist integer`, 32 bit

**Default**: `0`

**Failsafe**: `0`

**Description**: Delay in microseconds executed before handling the OpenCore picker startup and `action hotkeys`.

Introducing a delay may give extra time to hold the right `action hotkey` sequence to, for instance, boot into recovery mode. On most systems, the appearance of the initial boot logo is a good indication of the time from which hotkeys can be held down. Earlier than this, the key press may not be registered. On some platforms, setting this option to a minimum of `5000-10000` microseconds is also required to access `action hotkeys` due to the nature of the keyboard driver.

If the boot chime is configured (see audio configuration options) then at the expense of slower startup, an even longer delay of half to one second (`500000-1000000`) may be used to create behaviour similar to a real Mac, where the chime itself can be used as a signal for when hotkeys can be pressed. The boot chime is inevitably later in the boot sequence in OpenCore than on Apple hardware, due to the fact that non-native drivers have to be loaded and connected first. Configuring the boot chime and adding this longer additional delay can also be useful in systems where fast boot time and/or slow monitor signal synchronisation may cause the boot logo not to be shown at all on some boots or reboots.

<h3 id=misc-boot-timeout>Misc -> Boot -> Timeout</h3>

**Type**: `plist integer`, 32 bit

**Default**: `5`

**Failsafe**: `0`

**Description**: Timeout in seconds in the OpenCore picker before automatic booting of the default boot entry. Set to `0` to disable.

<h2 id=misc-debug>Misc -> Debug</h2>

**Type**: `plist dict`

**Description**: Apply debug configuration described in the **Debug Properties** section below.

<h3 id=misc-debug-appledebug>Misc -> Debug -> AppleDebug</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Enable writing the `boot.efi` debug log to the OpenCore log.

*Note*: This option only applies to 10.15.4 and newer.

<h3 id=misc-debug-applepanic>Misc -> Debug -> ApplePanic</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Save macOS kernel panic output to the OpenCore root partition.

The file is saved as `panic-YYYY-MM-DD-HHMMSS.txt`. It is strongly recommended to set the `keepsyms=1` boot argument to see debug symbols in the panic log. In cases where it is not present, the `kpdescribe.sh` utility (bundled with OpenCore) may be used to partially recover the stacktrace.

Development and debug kernels produce more useful kernel panic logs. Consider downloading and installing the `KernelDebugKit` from [developer.apple.com](https://developer.apple.com) when debugging a problem. To activate a development kernel, the boot argument `kcsuffix=development` should be added. Use the `uname -a` command to ensure that the current loaded kernel is a development (or a debug) kernel.

In cases where the OpenCore kernel panic saving mechanism is not used, kernel panic logs may still be found in the `/Library/Logs/DiagnosticReports` directory.

Starting with macOS Catalina, kernel panics are stored in JSON format and thus need to be preprocessed before passing to `kpdescribe.sh`:

<h3 id=misc-debug-disablewatchdog>Misc -> Debug -> DisableWatchDog</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Some types of firmware may not succeed in booting the operating system quickly, especially in debug mode. This results in the watchdog timer aborting the process. This option turns off the watchdog timer.

<h3 id=misc-debug-displaydelay>Misc -> Debug -> DisplayDelay</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0`

**Description**: Delay in microseconds executed after every printed line visible onscreen (i.e. console).

<h3 id=misc-debug-displaylevel>Misc -> Debug -> DisplayLevel</h3>

**Type**: `plist integer`, 64 bit

**Default**: `2147483650`

**Failsafe**: `0`

**Description**: EDK II debug level bitmask (sum) showed onscreen. Unless `Target` enables console (onscreen) printing, onscreen debug output will not be visible.

The following levels are supported (discover more in [DebugLib.h](https://github.com/acidanthera/audk/blob/master/MdePkg/Include/Library/DebugLib.h)):
* `0x00000002` (bit `1`) --- `DEBUG_WARN` in `DEBUG`, `NOOPT`, `RELEASE`.
* `0x00000040` (bit `6`) --- `DEBUG_INFO` in `DEBUG`, `NOOPT`.
* `0x00400000` (bit `22`) --- `DEBUG_VERBOSE` in custom builds.
* `0x80000000` (bit `31`) --- `DEBUG_ERROR` in `DEBUG`, `NOOPT`, `RELEASE`.

<h3 id=misc-debug-logmodules>Misc -> Debug -> LogModules</h3>

**Type**: `plist string`

**Default**: `*`

**Failsafe**: `*`

**Description**: Filter log entries by module.

This option filters logging generated by specific modules, both in the log and onscreen. Two modes are supported:
* `+` --- Positive filtering: Only present selected modules.
* `-` --- Negative filtering: Exclude selected modules.  When multiple log line identifiers are selected, comma (`,`) should be used as the splitter. For instance, `+OCCPU,OCA,OCB` means only `OCCPU`, `OCA`, `OCB` should be logged, while `-OCCPU,OCA,OCB` indicates these modules should be filtered out (i.e. not logged). Since there may be lines in the log with no valid prefix (i.e. log lines which are not generated by parts of OpenCore, but by other loaded drivers) then the special module name question mark (`?`) can be included in the list to include (with positive filtering) or exclude (with negative filtering) these non-standard lines. When no `+` or `-` symbol is specified, positive filtering (`+`) will be used. `*` alone as the option value indicates all modules being logged.

*Note 1*: Acronyms of libraries can be found in the **`Libraries`** section below.

*Note 2*: Messages printed before the configuration of the log protocol cannot be filtered from the early on screen log, but on being de-buffered from the early log buffer, will be filtered as requested for other log targets.

*Note 3*: To avoid missing key issues, warning and error log messages are not filtered.

<h3 id=misc-debug-sysreport>Misc -> Debug -> SysReport</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Produce system report on ESP folder.

This option will create a `SysReport` directory in the ESP partition unless already present. The directory will contain ACPI, SMBIOS, and audio codec dumps. Audio codec dumps require an audio backend driver to be loaded.

*Note*: To maintain system integrity, the `SysReport` option is **not** available in `RELEASE` builds. Use a `DEBUG` build if this option is required.

<h3 id=misc-debug-target>Misc -> Debug -> Target</h3>

**Type**: `plist integer`

**Default**: `3`

**Failsafe**: `0`

**Description**: A bitmask (sum) of enabled logging targets. Logging output is hidden by default and this option must be set when such output is required, such as when debugging.

The following logging targets are supported:
* `0x01` (bit `0`) --- Enable logging, otherwise all log is discarded.
* `0x02` (bit `1`) --- Enable basic console (onscreen) logging.
* `0x04` (bit `2`) --- Enable logging to Data Hub.
* `0x08` (bit `3`) --- Enable serial port logging.
* `0x10` (bit `4`) --- Enable UEFI variable logging.
* `0x20` (bit `5`) --- Enable `non-volatile` UEFI variable logging.
* `0x40` (bit `6`) --- Enable logging to file.
* `0x80` (bit `7`) --- In combination with `0x40`, enable faster but unsafe (see Warning 2 below) file logging. 

Console logging prints less than the other variants. Depending on the build type (`RELEASE`, `DEBUG`, or `NOOPT`) different amount of logging may be read (from least to most).

To obtain Data Hub logs, use the following command in macOS (Note that Data Hub logs do not log kernel and kext patches):

<h2 id=misc-entries>Misc -> Entries</h2>

**Type**: `plist array`

**Failsafe**: Empty

**Description**: Add boot entries to OpenCore picker.

To be filled with `plist dict` values, describing each load entry. Refer to the **Entry Properties** section below for details.

<h3 id=misc-entries-arguments>Misc -> Entries[] -> Arguments</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Arbitrary ASCII string used as boot arguments (load options) of the specified entry.

<h3 id=misc-entries-auxiliary>Misc -> Entries[] -> Auxiliary</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Set to `true` to hide this entry when `HideAuxiliary` is also set to `true`. Press the `Spacebar` key to enter `'Extended Mode'' and display the entry when hidden.

<h3 id=misc-entries-comment>Misc -> Entries[] -> Comment</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Arbitrary ASCII string used to provide a human readable reference for the entry. Whether this value is used is implementation defined.

<h3 id=misc-entries-enabled>Misc -> Entries[] -> Enabled</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Set to `true` activate this entry.

<h3 id=misc-entries-flavour>Misc -> Entries[] -> Flavour</h3>

**Type**: `plist string`

**Default**: `Auto`

**Failsafe**: `Auto`

**Description**: Specify the content flavour for this entry. See **`OC_ATTR_USE_FLAVOUR_ICON`** flag for documentation.

<h3 id=misc-entries-name>Misc -> Entries[] -> Name</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Human readable entry name displayed in the OpenCore picker.

<h3 id=misc-entries-path>Misc -> Entries[] -> Path</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Entry location depending on entry type.
* `Entries` specify external boot options, and therefore take device paths in the `Path` key. Care should be exercised as these values are not checked. Example: `PciRoot(0x0)/Pci(0x1,0x1)/.../\EFI\COOL.EFI`
* `Tools` specify internal boot options, which are part of the bootloader vault, and therefore take file paths relative to the `OC/Tools` directory. Example: `OpenShell.efi`.

<h3 id=misc-entries-textmode>Misc -> Entries[] -> TextMode</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Run the entry in text mode instead of graphics mode.

This setting may be beneficial for some older tools that require text output as all the tools are launched in graphics mode by default. Refer to the **Output Properties** section below for information on text modes.

<h2 id=misc-security>Misc -> Security</h2>

**Type**: `plist dict`

**Description**: Apply the security configuration described in the **Security Properties** section below.

<h3 id=misc-security-allowsetdefault>Misc -> Security -> AllowSetDefault</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Allow `CTRL+Enter` and `CTRL+Index` handling to set the default boot option in the OpenCore picker.

*Note 1*: May be used in combination with `Shift+Enter` or `Shift+Index` when `PollAppleHotKeys` is enabled.

*Note 2*: In order to support systems with unresponsive modifiers during preboot (which includes `V1` and `V2` `KeySupport` mode on some firmware) OpenCore also allows holding the `=/+` key in order to trigger 'set default' mode.

<h3 id=misc-security-apecid>Misc -> Security -> ApECID</h3>

**Type**: `plist integer`, 64 bit

**Default**: `0`

**Failsafe**: `0`

**Description**: Apple Enclave Identifier.

Setting this value to any non-zero 64-bit integer will allow using personalised Apple Secure Boot identifiers. To use this setting, generate a random 64-bit number with a cryptographically secure random number generator. As an alternative, the first 8 bytes of `SystemUUID` can be used for `ApECID`, this is found in macOS 11 for Macs without the T2 chip.

With this value set and `SecureBootModel` valid (and not `Disabled`), it is possible to achieve [`Full Security`](https://support.apple.com/en-us/HT208330) of Apple Secure Boot.

To start using personalised Apple Secure Boot, the operating system must be reinstalled or personalised. Until the operating system is personalised, only macOS DMG recovery can be loaded. In cases where DMG recovery is missing, it can be downloaded by using the `macrecovery` utility and saved in `com.apple.recovery.boot` as explained in the **Tips and Tricks** section. Note that **DMG loading** needs to be set to `Signed` to use any DMG with Apple Secure Boot.

To personalise an existing operating system, use the `bless` command after loading to macOS DMG recovery. Mount the system volume partition, unless it has already been mounted, and execute the following command:

<h3 id=misc-security-authrestart>Misc -> Security -> AuthRestart</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Enable `VirtualSMC`-compatible authenticated restart.

Authenticated restart is a way to reboot FileVault 2 enabled macOS without entering the password. A dedicated terminal command can be used to perform authenticated restarts: `sudo fdesetup authrestart`. It is also used when installing operating system updates.

VirtualSMC performs authenticated restarts by splitting and saving disk encryption keys between NVRAM and RTC, which despite being removed as soon as OpenCore starts, may be considered a security risk and thus is optional.

<h3 id=misc-security-blacklistappleupdate>Misc -> Security -> BlacklistAppleUpdate</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Ignore boot options trying to update Apple peripheral firmware (e.g. `MultiUpdater.efi`).

*Note*: Certain operating systems, such as macOS Big Sur, are [incapable](https://github.com/acidanthera/bugtracker/issues/1255) of disabling firmware updates by using the `run-efi-updater` NVRAM variable.

<h3 id=misc-security-dmgloading>Misc -> Security -> DmgLoading</h3>

**Type**: `plist string`

**Default**: `Signed`

**Failsafe**: `Signed`

**Description**: Define Disk Image (DMG) loading policy used for macOS Recovery.

Valid values:
* `Disabled` --- loading DMG images will fail. The `Disabled` policy will still let the macOS Recovery load in most cases as typically, there are `boot.efi` files compatible with Apple Secure Boot. Manually downloaded DMG images stored in `com.apple.recovery.boot` directories will not load, however.
* `Signed` --- only Apple-signed DMG images will load. Due to the design of Apple Secure Boot, the `Signed` policy will let any Apple-signed macOS Recovery load regardless of the Apple Secure Boot state, which may not always be desired. While using signed DMG images is more desirable, verifying the image signature may slightly slow the boot time down (by up to 1 second).
* `Any` --- any DMG images will mount as normal filesystems. The `Any` policy is strongly discouraged and will result in boot failures when Apple Secure Boot is active.

<h3 id=misc-security-enablepassword>Misc -> Security -> EnablePassword</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Enable password protection to facilitate sensitive operations.

Password protection ensures that sensitive operations such as booting a non-default operating system (e.g. macOS recovery or a tool), resetting NVRAM storage, trying to boot into a non-default mode (e.g. verbose mode or safe mode) are not allowed without explicit user authentication by a custom password. Currently, password and salt are hashed with 5000000 iterations of SHA-512.

*Note*: This functionality is still under development and is not ready for production environments.

<h3 id=misc-security-exposesensitivedata>Misc -> Security -> ExposeSensitiveData</h3>

**Type**: `plist integer`

**Default**: `6`

**Failsafe**: `0x6`

**Description**: Sensitive data exposure bitmask (sum) to operating system.
* `0x01` --- Expose the printable booter path as a UEFI variable.
* `0x02` --- Expose the OpenCore version as a UEFI variable.
* `0x04` --- Expose the OpenCore version in the OpenCore picker menu title.
* `0x08` --- Expose OEM information as a set of UEFI variables. 

The exposed booter path points to OpenCore.efi or its booter depending on the load order. To obtain the booter path, use the following command in macOS:

<h3 id=misc-security-haltlevel>Misc -> Security -> HaltLevel</h3>

**Type**: `plist integer`, 64 bit

**Default**: `2147483648`

**Failsafe**: `0x80000000` (`DEBUG_ERROR`)

**Description**: EDK II debug level bitmask (sum) causing CPU to halt (stop execution) after obtaining a message of `HaltLevel`. Possible values match `DisplayLevel` values.

*Note 1*: A halt will only occur if bit `0` (i.e. enable logging) for `Target` under section `Misc->Debug` is set.

*Note 2*: A halt will only occur after the configuration is loaded and logging is configured. If any log messages occur at the specified halt level in early log (i.e. before this), they will cause a halt when they are flushed to the log once it has been configured.

<h3 id=misc-security-passwordhash>Misc -> Security -> PasswordHash</h3>

**Type**: `plist data` 64 bytes

**Default**: Empty

**Failsafe**: all zero

**Description**: Password hash used when `EnablePassword` is set.

<h3 id=misc-security-passwordsalt>Misc -> Security -> PasswordSalt</h3>

**Type**: `plist data`

**Default**: Empty

**Failsafe**: empty

**Description**: Password salt used when `EnablePassword` is set.

<h3 id=misc-security-scanpolicy>Misc -> Security -> ScanPolicy</h3>

**Type**: `plist integer`, 32 bit

**Default**: `17760515`

**Failsafe**: `0x10F0103`

**Description**: Define operating system detection policy.

This value allows preventing scanning (and booting) untrusted sources based on a bitmask (sum) of a set of flags. As it is not possible to reliably detect every file system or device type, this feature cannot be fully relied upon in open environments, and additional measures are to be applied.

Third party drivers may introduce additional security (and performance) consideratons following the provided scan policy. The active Scan policy is exposed in the `scan-policy` variable of `4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102` GUID for UEFI Boot Services only.
* `0x00000001` (bit `0`) --- `OC_SCAN_FILE_SYSTEM_LOCK`, restricts scanning to only known file systems defined as a part of this policy. File system drivers may not be aware of this policy. Hence, to avoid mounting of undesired file systems, drivers for such file systems should not be loaded. This bit does not affect DMG mounting, which may have any file system. Known file systems are prefixed with `OC_SCAN_ALLOW_FS_`.
* `0x00000002` (bit `1`) --- `OC_SCAN_DEVICE_LOCK`, restricts scanning to only known device types defined as a part of this policy. It is not always possible to detect protocol tunneling, so be aware that on some systems, it may be possible for e.g. USB HDDs to be recognised as SATA instead. Cases like this must be reported. Known device types are prefixed with `OC_SCAN_ALLOW_DEVICE_`.
* `0x00000100` (bit `8`) --- `OC_SCAN_ALLOW_FS_APFS`, allows scanning of APFS file system.
* `0x00000200` (bit `9`) --- `OC_SCAN_ALLOW_FS_HFS`, allows scanning of HFS file system.
* `0x00000400` (bit `10`) --- `OC_SCAN_ALLOW_FS_ESP`, allows scanning of EFI System Partition file system.
* `0x00000800` (bit `11`) --- `OC_SCAN_ALLOW_FS_NTFS`, allows scanning of NTFS (Msft Basic Data) file system.
* `0x00001000` (bit `12`) --- `OC_SCAN_ALLOW_FS_LINUX_ROOT`, allows scanning of Linux Root file systems.
* `0x00002000` (bit `13`) --- `OC_SCAN_ALLOW_FS_LINUX_DATA`, allows scanning of Linux Data file systems.
* `0x00004000` (bit `14`) --- `OC_SCAN_ALLOW_FS_XBOOTLDR`, allows scanning the Extended Boot Loader Partition as defined by the [Boot Loader Specification](https://systemd.io/BOOT_LOADER_SPECIFICATION/).
* `0x00010000` (bit `16`) --- `OC_SCAN_ALLOW_DEVICE_SATA`, allow scanning SATA devices.
* `0x00020000` (bit `17`) --- `OC_SCAN_ALLOW_DEVICE_SASEX`, allow scanning SAS and Mac NVMe devices.
* `0x00040000` (bit `18`) --- `OC_SCAN_ALLOW_DEVICE_SCSI`, allow scanning SCSI devices.
* `0x00080000` (bit `19`) --- `OC_SCAN_ALLOW_DEVICE_NVME`, allow scanning NVMe devices.
* `0x00100000` (bit `20`) --- `OC_SCAN_ALLOW_DEVICE_ATAPI`, allow scanning CD/DVD devices and old SATA.
* `0x00200000` (bit `21`) --- `OC_SCAN_ALLOW_DEVICE_USB`, allow scanning USB devices.
* `0x00400000` (bit `22`) --- `OC_SCAN_ALLOW_DEVICE_FIREWIRE`, allow scanning FireWire devices.
* `0x00800000` (bit `23`) --- `OC_SCAN_ALLOW_DEVICE_SDCARD`, allow scanning card reader devices.
* `0x01000000` (bit `24`) --- `OC_SCAN_ALLOW_DEVICE_PCI`, allow scanning devices directly connected to PCI bus (e.g. VIRTIO). 

*Note*: Given the above description, a value of `0xF0103` is expected to do the following:
* Permit scanning SATA, SAS, SCSI, and NVMe devices with APFS file systems.
* Prevent scanning any devices with HFS or FAT32 file systems.
* Prevent scanning APFS file systems on USB, CD, and FireWire drives. 

The combination reads as:
* `OC_SCAN_FILE_SYSTEM_LOCK`
* `OC_SCAN_DEVICE_LOCK`
* `OC_SCAN_ALLOW_FS_APFS`
* `OC_SCAN_ALLOW_DEVICE_SATA`
* `OC_SCAN_ALLOW_DEVICE_SASEX`
* `OC_SCAN_ALLOW_DEVICE_SCSI`
* `OC_SCAN_ALLOW_DEVICE_NVME`

<h3 id=misc-security-securebootmodel>Misc -> Security -> SecureBootModel</h3>

**Type**: `plist string`

**Default**: `Default`

**Failsafe**: `Default`

**Description**: Apple Secure Boot hardware model.

Sets Apple Secure Boot hardware model and policy. Specifying this value defines which operating systems will be bootable. Operating systems shipped before the specified model was released will not boot.

Valid values:
* `Default` --- Matching model for current SMBIOS.
* `Disabled` --- No model, Secure Boot will be disabled.
* `j137` --- `iMacPro1,1 (December 2017). Minimum macOS 10.13.2 (17C2111)`
* `j680` --- `MacBookPro15,1 (July 2018). Minimum macOS 10.13.6 (17G2112)`
* `j132` --- `MacBookPro15,2 (July 2018). Minimum macOS 10.13.6 (17G2112)`
* `j174` --- `Macmini8,1 (October 2018). Minimum macOS 10.14 (18A2063)`
* `j140k` --- `MacBookAir8,1 (October 2018). Minimum macOS 10.14.1 (18B2084)`
* `j780` --- `MacBookPro15,3 (May 2019). Minimum macOS 10.14.5 (18F132)`
* `j213` --- `MacBookPro15,4 (July 2019). Minimum macOS 10.14.5 (18F2058)`
* `j140a` --- `MacBookAir8,2 (July 2019). Minimum macOS 10.14.5 (18F2058)`
* `j152f` --- `MacBookPro16,1 (November 2019). Minimum macOS 10.15.1 (19B2093)`
* `j160` --- `MacPro7,1 (December 2019). Minimum macOS 10.15.1 (19B88)`
* `j230k` --- `MacBookAir9,1 (March 2020). Minimum macOS 10.15.3 (19D2064)`
* `j214k` --- `MacBookPro16,2 (May 2020). Minimum macOS 10.15.4 (19E2269)`
* `j223` --- `MacBookPro16,3 (May 2020). Minimum macOS 10.15.4 (19E2265)`
* `j215` --- `MacBookPro16,4 (June 2020). Minimum macOS 10.15.5 (19F96)`
* `j185` --- `iMac20,1 (August 2020). Minimum macOS 10.15.6 (19G2005)`
* `j185f` --- `iMac20,2 (August 2020). Minimum macOS 10.15.6 (19G2005)`
* `x86legacy` --- `Macs without T2 chip and VMs. Minimum macOS 11.0.1 (20B29)` 

*Warning*: Not all Apple Secure Boot models are supported on all hardware configurations.

Apple Secure Boot appeared in macOS 10.13 on models with T2 chips. Prior to macOS 12 `PlatformInfo` and `SecureBootModel` were independent, allowing Apple Secure Boot can be used with any SMBIOS with and without T2. Starting with macOS 12 `SecureBootModel` must match the SMBIOS Mac model. `Default` model derives the model based on SMBIOS board identifier, either set automatically via the `Generic` section or set manually via the `SMBIOS` section. If there is no board identifier override the model will be derived heuristically from OEM SMBIOS.

Setting `SecureBootModel` to any valid value but `Disabled` is equivalent to [`Medium Security`](https://support.apple.com/en-us/HT208330) of Apple Secure Boot. The `ApECID` value must also be specified to achieve `Full Security`. Check `ForceSecureBootScheme` when using Apple Secure Boot on a virtual machine.

Note that enabling Apple Secure Boot is demanding on invalid configurations, faulty macOS installations, and on unsupported setups.

Things to consider:

\begin{enumerate}
* As with T2 Macs, all unsigned kernel extensions as well as several signed kernel extensions, including NVIDIA Web Drivers, cannot be installed.
* The list of cached kernel extensions may be different, resulting in a need to change the list of `Added` or `Forced` kernel extensions. For example, `IO80211Family` cannot be injected in this case.
* System volume alterations on operating systems with sealing, such as macOS~11, may result in the operating system being unbootable. Do not try to disable system volume encryption unless Apple Secure Boot is disabled.
* Boot failures might occur when the platform requires certain settings, but they have not been enabled because the associated issues were not discovered earlier. Be extra careful with `IgnoreInvalidFlexRatio` or `HashServices`.
* Operating systems released before Apple Secure Boot was released (e.g. macOS~10.12 or earlier), will still boot until UEFI Secure Boot is enabled. This is so because Apple Secure Boot treats these as incompatible and they are then handled by the firmware (as Microsoft Windows is).
* On older CPUs (e.g. before Sandy Bridge), enabling Apple Secure Boot might cause slightly slower loading (by up to 1 second).
* As the `Default` value will increase with time to support the latest major released operating system, it is not recommended to use the `ApECID` and the `Default` settings together.
* Installing macOS with Apple Secure Boot enabled is not possible while using HFS+ target volumes. This may include HFS+ formatted drives when no spare APFS drive is available. \end{enumerate}

The installed operating system may have sometimes outdated Apple Secure Boot manifests on the `Preboot` partition, resulting in boot failures. This is likely to be the case when an `'OCB: Apple Secure Boot prohibits this boot entry, enforcing!'' message is logged.

When this happens, either reinstall the operating system or copy the manifests (files with `.im4m` extension, such as `boot.efi.j137.im4m`) from `/usr/standalone/i386` to `/Volumes/Preboot/<UUID>/System/Library/CoreServices`. Here, `<UUID>` is the system volume identifier. On HFS+ installations, the manifests should be copied to `/System/Library/CoreServices` on the system volume.

For more details on how to configure Apple Secure Boot with UEFI Secure Boot, refer to the **UEFI Secure Boot** section.

<h3 id=misc-security-vault>Misc -> Security -> Vault</h3>

**Type**: `plist string`

**Default**: `Secure`

**Failsafe**: `Secure`

**Description**: Enables the OpenCore vaulting mechanism.

Valid values:
* `Optional` --- require nothing, no vault is enforced, insecure.
* `Basic` --- require `vault.plist` file present in `OC` directory. This provides basic filesystem integrity verification and may protect from unintentional filesystem corruption.
* `Secure` --- require `vault.sig` signature file for `vault.plist` in `OC` directory. This includes `Basic` integrity checking but also attempts to build a trusted bootchain. 

The `vault.plist` file should contain SHA-256 hashes for all files used by OpenCore. The presence of this file is highly recommended to ensure that unintentional file modifications (including filesystem corruption) do not go unnoticed. To create this file automatically, use the [`create_vault.sh`](https://github.com/acidanthera/OpenCorePkg/tree/master/Utilities/CreateVault) script. Notwithstanding the underlying file system, the path names and cases between `config.plist` and `vault.plist` must match.

The `vault.sig` file should contain a raw 256 byte RSA-2048 signature from a SHA-256 hash of `vault.plist`. The signature is verified against the public key embedded into `OpenCore.efi`.

To embed the public key, either one of the following should be performed:
* Provide public key during the `OpenCore.efi` compilation in [`OpenCoreVault.c`](https://github.com/acidanthera/OpenCorePkg/blob/master/Platform/OpenCore/OpenCoreVault.c) file.
* Binary patch `OpenCore.efi` replacing zeroes with the public key between `=BEGIN OC VAULT=` and `==END OC VAULT==` ASCII markers. 

The RSA public key 520 byte format description can be found in Chromium OS documentation. To convert the public key from X.509 certificate or from PEM file use [RsaTool](https://github.com/acidanthera/OpenCorePkg/tree/master/Utilities/CreateVault).

The complete set of commands to:
* Create `vault.plist`.
* Create a new RSA key (always do this to avoid loading old configuration).
* Embed RSA key into `OpenCore.efi`.
* Create `vault.sig`. 

Can look as follows:

<h2 id=misc-serial>Misc -> Serial</h2>

**Type**: `plist dict`

**Description**: Perform serial port initialisation and configure PCD values required by `BaseSerialPortLib16550` for serial ports to properly function. Values are listed and described in the **Serial Properties** and **Serial Custom Properties** section below.

By enabling `Init`, this section ensures that the serial port is initialised when it is not done by firmware. In order for OpenCore to print logs to the serial port, bit `3` (i.e. serial logging) for `Target` under section `Misc->Debug` must be set.

When debugging with serial ports, `BaseSerialPortLib16550` only recognises internal ones provided by the motherboard by default. If the option `Override` is enabled, this section will override the PCD values listed in [BaseSerialPortLib16550.inf](https://github.com/acidanthera/audk/blob/master/MdeModulePkg/Library/BaseSerialPortLib16550/BaseSerialPortLib16550.inf) such that external serial ports (e.g. from a PCI card) will also function properly. Specifically, when troubleshooting macOS, in addition to overriding these PCD values, it is also necessary to turn the `CustomPciSerialDevice` kernel quirk on in order for the XNU to use such exterior serial ports.

Refer to [MdeModulePkg.dec](https://github.com/acidanthera/audk/blob/master/MdeModulePkg/MdeModulePkg.dec) for the explanations of each key.

<h3 id=misc-serial-custom>Misc -> Serial -> Custom</h3>

**Type**: `plist dict`

**Description**: Update serial port properties in `BaseSerialPortLib16550`.

This section lists the PCD values that are used by the `BaseSerialPortLib16550`. When option `Override` is set to `false`, this dictionary is optional.

<h4 id=misc-serial-custom-baudrate>Misc -> Serial -> Custom -> BaudRate</h4>

**Type**: `plist integer`

**Failsafe**: `115200`

**Description**: Set the baud rate for serial port.

This option will override the value of `gEfiMdeModulePkgTokenSpaceGuid.PcdSerialBaudRate` defined in [MdeModulePkg.dec](https://github.com/acidanthera/audk/blob/master/MdeModulePkg/MdeModulePkg.dec).

<h4 id=misc-serial-custom-clockrate>Misc -> Serial -> Custom -> ClockRate</h4>

**Type**: `plist integer`

**Failsafe**: `1843200`

**Description**: Set the clock rate for serial port.

This option will override the value of `gEfiMdeModulePkgTokenSpaceGuid.PcdSerialClockRate` defined in [MdeModulePkg.dec](https://github.com/acidanthera/audk/blob/master/MdeModulePkg/MdeModulePkg.dec).

<h4 id=misc-serial-custom-detectcable>Misc -> Serial -> Custom -> DetectCable</h4>

**Type**: `plist boolean`

**Failsafe**: `false`

**Description**: Enable serial port cable detection.

This option will override the value of `gEfiMdeModulePkgTokenSpaceGuid.PcdSerialDetectCable` defined in [MdeModulePkg.dec](https://github.com/acidanthera/audk/blob/master/MdeModulePkg/MdeModulePkg.dec).

<h4 id=misc-serial-custom-extendedtxfifosize>Misc -> Serial -> Custom -> ExtendedTxFifoSize</h4>

**Type**: `plist integer`

**Failsafe**: `64`

**Description**: Set the extended transmit FIFO size for serial port.

This option will override the value of `gEfiMdeModulePkgTokenSpaceGuid.PcdSerialExtendedTxFifoSize` defined in [MdeModulePkg.dec](https://github.com/acidanthera/audk/blob/master/MdeModulePkg/MdeModulePkg.dec).

<h4 id=misc-serial-custom-fifocontrol>Misc -> Serial -> Custom -> FifoControl</h4>

**Type**: `plist integer`

**Failsafe**: `0x07`

**Description**: Configure serial port FIFO Control settings.

This option will override the value of `gEfiMdeModulePkgTokenSpaceGuid.PcdSerialFifoControl` defined in [MdeModulePkg.dec](https://github.com/acidanthera/audk/blob/master/MdeModulePkg/MdeModulePkg.dec).

<h4 id=misc-serial-custom-linecontrol>Misc -> Serial -> Custom -> LineControl</h4>

**Type**: `plist integer`

**Failsafe**: `0x07`

**Description**: Configure serial port Line Control settings.

This option will override the value of `gEfiMdeModulePkgTokenSpaceGuid.PcdSerialLineControl` defined in [MdeModulePkg.dec](https://github.com/acidanthera/audk/blob/master/MdeModulePkg/MdeModulePkg.dec).

<h4 id=misc-serial-custom-pcideviceinfo>Misc -> Serial -> Custom -> PciDeviceInfo</h4>

**Type**: `plist data`

**Failsafe**: `0xFF`

**Description**: Set PCI serial device information.

This option will override the value of `gEfiMdeModulePkgTokenSpaceGuid.PcdSerialPciDeviceInfo` defined in [MdeModulePkg.dec](https://github.com/acidanthera/audk/blob/master/MdeModulePkg/MdeModulePkg.dec).

*Note*: The maximum allowed size of this option is 41 bytes. Refer to [acidanthera/bugtracker#1954](https://github.com/acidanthera/bugtracker/issues/1954#issuecomment-1084220743) for more details.

*Note 2*: This option can be set by running the [`FindSerialPort`](https://github.com/acidanthera/OpenCorePkg/tree/master/Utilities/FindSerialPort) tool.

<h4 id=misc-serial-custom-registeraccesswidth>Misc -> Serial -> Custom -> RegisterAccessWidth</h4>

**Type**: `plist integer`

**Failsafe**: `8`

**Description**: Set serial port register access width.

This option will override the value of `gEfiMdeModulePkgTokenSpaceGuid.PcdSerialRegisterAccessWidth` defined in [MdeModulePkg.dec](https://github.com/acidanthera/audk/blob/master/MdeModulePkg/MdeModulePkg.dec).

<h4 id=misc-serial-custom-registerbase>Misc -> Serial -> Custom -> RegisterBase</h4>

**Type**: `plist integer`

**Failsafe**: `0x03F8`

**Description**: Set the base address of serial port registers.

This option will override the value of `gEfiMdeModulePkgTokenSpaceGuid.PcdSerialRegisterBase` defined in [MdeModulePkg.dec](https://github.com/acidanthera/audk/blob/master/MdeModulePkg/MdeModulePkg.dec).

<h4 id=misc-serial-custom-registerstride>Misc -> Serial -> Custom -> RegisterStride</h4>

**Type**: `plist integer`

**Failsafe**: `1`

**Description**: Set the serial port register stride in bytes.

This option will override the value of `gEfiMdeModulePkgTokenSpaceGuid.PcdSerialRegisterStride` defined in [MdeModulePkg.dec](https://github.com/acidanthera/audk/blob/master/MdeModulePkg/MdeModulePkg.dec).

<h4 id=misc-serial-custom-usehardwareflowcontrol>Misc -> Serial -> Custom -> UseHardwareFlowControl</h4>

**Type**: `plist boolean`

**Failsafe**: `false`

**Description**: Enable serial port hardware flow control.

This option will override the value of `gEfiMdeModulePkgTokenSpaceGuid.PcdSerialUseHardwareFlowControl` defined in [MdeModulePkg.dec](https://github.com/acidanthera/audk/blob/master/MdeModulePkg/MdeModulePkg.dec).

<h4 id=misc-serial-custom-usemmio>Misc -> Serial -> Custom -> UseMmio</h4>

**Type**: `plist boolean`

**Failsafe**: `false`

**Description**: Indicate whether the serial port registers are in MMIO space.

This option will override the value of `gEfiMdeModulePkgTokenSpaceGuid.PcdSerialUseMmio` defined in [MdeModulePkg.dec](https://github.com/acidanthera/audk/blob/master/MdeModulePkg/MdeModulePkg.dec).

<h3 id=misc-serial-init>Misc -> Serial -> Init</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Perform serial port initialisation.

This option will perform serial port initialisation within OpenCore prior to enabling (any) debug logging.

Refer to the **`Debugging`** section for details.

<h3 id=misc-serial-override>Misc -> Serial -> Override</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Override serial port properties. When this option is set to `false`, no keys from `Custom` will be overridden.

This option will override serial port properties listed in the **`Serial Custom Properties`** section below.

<h2 id=misc-tools>Misc -> Tools</h2>

**Type**: `plist array`

**Failsafe**: Empty

**Description**: Add tool entries to the OpenCore picker.

To be filled with `plist dict` values, describing each load entry. Refer to the **Entry Properties** section below for details.

*Note*: Certain UEFI tools, such as UEFI Shell, can be very dangerous and **MUST NOT** appear in production configurations, paticularly in vaulted configurations as well as those protected by secure boot, as such tools can be used to bypass the secure boot chain. Refer to the **UEFI** section for examples of UEFI tools.

<h3 id=misc-tools-arguments>Misc -> Tools[] -> Arguments</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Arbitrary ASCII string used as boot arguments (load options) of the specified entry.

<h3 id=misc-tools-auxiliary>Misc -> Tools[] -> Auxiliary</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Set to `true` to hide this entry when `HideAuxiliary` is also set to `true`. Press the `Spacebar` key to enter `'Extended Mode'' and display the entry when hidden.

<h3 id=misc-tools-comment>Misc -> Tools[] -> Comment</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Arbitrary ASCII string used to provide a human readable reference for the entry. Whether this value is used is implementation defined.

<h3 id=misc-tools-enabled>Misc -> Tools[] -> Enabled</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Set to `true` activate this entry.

<h3 id=misc-tools-flavour>Misc -> Tools[] -> Flavour</h3>

**Type**: `plist string`

**Default**: `Auto`

**Failsafe**: `Auto`

**Description**: Specify the content flavour for this entry. See **`OC_ATTR_USE_FLAVOUR_ICON`** flag for documentation.

<h3 id=misc-tools-fullnvramaccess>Misc -> Tools[] -> FullNvramAccess</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Disable `OpenRuntime` NVRAM protection during usage of a tool.

This disables all of the NVRAM protections provided by `OpenRuntime.efi`, during the time a tool is in use. It should normally be avoided, but may be required for instance if a tool needs to access NVRAM directly without the redirections put in place by `RequestBootVarRouting`.

*Note*: This option is only valid for `Tools` and cannot be specified for `Entries` (is always `false`).

<h3 id=misc-tools-name>Misc -> Tools[] -> Name</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Human readable entry name displayed in the OpenCore picker.

<h3 id=misc-tools-path>Misc -> Tools[] -> Path</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Entry location depending on entry type.
* `Entries` specify external boot options, and therefore take device paths in the `Path` key. Care should be exercised as these values are not checked. Example: `PciRoot(0x0)/Pci(0x1,0x1)/.../\EFI\COOL.EFI`
* `Tools` specify internal boot options, which are part of the bootloader vault, and therefore take file paths relative to the `OC/Tools` directory. Example: `OpenShell.efi`.

<h3 id=misc-tools-realpath>Misc -> Tools[] -> RealPath</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Pass full path to the tool when launching.

This should typically be disabled as passing the tool directory may be unsafe with tools that accidentally attempt to access files without checking their integrity. Reasons to enable this property may include cases where tools cannot work without external files or may need them for enhanced functionality such as `memtest86` (for logging and configuration), or `Shell` (for automatic script execution).

*Note*: This option is only valid for `Tools` and cannot be specified for `Entries` (is always `true`).

<h3 id=misc-tools-textmode>Misc -> Tools[] -> TextMode</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Run the entry in text mode instead of graphics mode.

This setting may be beneficial for some older tools that require text output as all the tools are launched in graphics mode by default. Refer to the **Output Properties** section below for information on text modes.

<h2 id=nvram-add>NVRAM -> Add</h2>

**Type**: `plist dict`

**Description**: Sets NVRAM variables from a map (`plist dict`) of GUIDs to a map (`plist dict`) of variable names and their values in `plist multidata` format. GUIDs must be provided in canonic string format in upper or lower case (e.g. `8BE4DF61-93CA-11D2-AA0D-00E098032B8C`).

The `EFI_VARIABLE_BOOTSERVICE_ACCESS` and `EFI_VARIABLE_RUNTIME_ACCESS` attributes of created variables are set. Variables will only be set if not present or deleted. That is, to overwrite an existing variable value, add the variable name to the `Delete` section. This approach enables the provision of default values until the operating system takes the lead.

*Note*: The implementation behaviour is undefined when the `plist key` does not conform to the GUID format.

<h2 id=nvram-delete>NVRAM -> Delete</h2>

**Type**: `plist dict`

**Description**: Removes NVRAM variables from a map (`plist dict`) of GUIDs to an array (`plist array`) of variable names in `plist string` format.

<h2 id=nvram-legacyoverwrite>NVRAM -> LegacyOverwrite</h2>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Permits overwriting firmware variables from `nvram.plist`.

*Note*: Only variables accessible from the operating system will be overwritten.

<h2 id=nvram-legacyschema>NVRAM -> LegacySchema</h2>

**Type**: `plist dict`

**Description**: Allows setting certain NVRAM variables from a map (`plist dict`) of GUIDs to an array (`plist array`) of variable names in `plist string` format.

`*` value can be used to accept all variables for certain GUID.

**WARNING**: Choose variables carefully, as the nvram.plist file is not vaulted. For instance, do not include `boot-args` or `csr-active-config`, as these can be used to bypass SIP.

<h2 id=nvram-writeflash>NVRAM -> WriteFlash</h2>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Enables writing to flash memory for all added variables.

*Note*: This value should be enabled on most types of firmware but is left configurable to account for firmware that may have issues with NVRAM variable storage garbage collection or similar.

<h2 id=platforminfo-automatic>PlatformInfo -> Automatic</h2>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Generate PlatformInfo based on the `Generic` section instead of using values from the `DataHub`, `NVRAM`, and `SMBIOS` sections.

Enabling this option is useful when `Generic` section is flexible enough:
* When enabled `SMBIOS`, `DataHub`, and `PlatformNVRAM` data is unused.
* When disabled `Generic` section is unused. 

**Warning**: Setting this option to `false` is strongly discouraged when intending to update platform information. A `false` setting is typically only valid for minor corrections to SMBIOS values on legacy Apple hardware. In all other cases, setting `Automatic` to `false` may lead to hard-to-debug errors resulting from inconsistent or invalid settings.

<h2 id=platforminfo-custommemory>PlatformInfo -> CustomMemory</h2>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Use custom memory configuration defined in the `Memory` section. This completely replaces any existing memory configuration in SMBIOS, and is only active when `UpdateSMBIOS` is set to `true`.

<h2 id=platforminfo-datahub>PlatformInfo -> DataHub</h2>

**Type**: `plist dictionary`

**Description**: Update Data Hub fields in non-`Automatic` mode.

*Note*: This section is ignored and may be removed when `Automatic` is `true`.

<h3 id=platforminfo-datahub-artfrequency>PlatformInfo -> DataHub -> ARTFrequency</h3>

**Type**: `plist integer`, 64-bit

**Failsafe**: `0` (Automatic)

**Description**: Sets `ARTFrequency` in `gEfiProcessorSubClassGuid`.

This value contains CPU ART frequency, also known as crystal clock frequency. Its existence is exclusive to the Skylake generation and newer. The value is specified in Hz, and is normally 24 MHz for the client Intel segment, 25 MHz for the server Intel segment, and 19.2 MHz for Intel Atom CPUs. macOS till 10.15 inclusive assumes 24 MHz by default.

*Note*: On Intel Skylake X ART frequency may be a little less (approx. 0.25%) than 24 or 25 MHz due to special EMI-reduction circuit as described in [Acidanthera Bugtracker](https://github.com/acidanthera/bugtracker/issues/448#issuecomment-524914166).

<h3 id=platforminfo-datahub-boardproduct>PlatformInfo -> DataHub -> BoardProduct</h3>

**Type**: `plist string`

**Failsafe**: Empty (Not installed)

**Description**: Sets `board-id` in `gEfiMiscSubClassGuid`. The value found on Macs is equal to SMBIOS `BoardProduct` in ASCII.

<h3 id=platforminfo-datahub-boardrevision>PlatformInfo -> DataHub -> BoardRevision</h3>

**Type**: `plist data`, 1 byte

**Failsafe**: `0`

**Description**: Sets `board-rev` in `gEfiMiscSubClassGuid`. The value found on Macs seems to correspond to internal board revision (e.g. `01`).

<h3 id=platforminfo-datahub-devicepathssupported>PlatformInfo -> DataHub -> DevicePathsSupported</h3>

**Type**: `plist integer`, 32-bit

**Failsafe**: `0` (Not installed)

**Description**: Sets `DevicePathsSupported` in `gEfiMiscSubClassGuid`. Must be set to `1` for AppleACPIPlatform.kext to append SATA device paths to `Boot####` and `efi-boot-device-data` variables. Set to `1` on all modern Macs.

<h3 id=platforminfo-datahub-fsbfrequency>PlatformInfo -> DataHub -> FSBFrequency</h3>

**Type**: `plist integer`, 64-bit

**Failsafe**: `0` (Automatic)

**Description**: Sets `FSBFrequency` in `gEfiProcessorSubClassGuid`.

Sets CPU FSB frequency. This value equals to CPU nominal frequency divided by CPU maximum bus ratio and is specified in Hz. Refer to `MSR_NEHALEM_PLATFORM_INFO`~(`CEh`) MSR value to determine maximum bus ratio on modern Intel CPUs.

*Note*: This value is not used on Skylake and newer but is still provided to follow suit.

<h3 id=platforminfo-datahub-initialtsc>PlatformInfo -> DataHub -> InitialTSC</h3>

**Type**: `plist integer`, 64-bit

**Failsafe**: `0`

**Description**: Sets `InitialTSC` in `gEfiProcessorSubClassGuid`. Sets initial TSC value, normally 0.

<h3 id=platforminfo-datahub-platformname>PlatformInfo -> DataHub -> PlatformName</h3>

**Type**: `plist string`

**Failsafe**: Empty (Not installed)

**Description**: Sets `name` in `gEfiMiscSubClassGuid`. The value found on Macs is `platform` in ASCII.

<h3 id=platforminfo-datahub-smcbranch>PlatformInfo -> DataHub -> SmcBranch</h3>

**Type**: `plist data`, 8 bytes

**Failsafe**: Empty (Not installed)

**Description**: Sets `RBr` in `gEfiMiscSubClassGuid`. Custom property read by `VirtualSMC` or `FakeSMC` to generate SMC `RBr` key.

<h3 id=platforminfo-datahub-smcplatform>PlatformInfo -> DataHub -> SmcPlatform</h3>

**Type**: `plist data`, 8 bytes

**Failsafe**: Empty (Not installed)

**Description**: Sets `RPlt` in `gEfiMiscSubClassGuid`. Custom property read by `VirtualSMC` or `FakeSMC` to generate SMC `RPlt` key.

<h3 id=platforminfo-datahub-smcrevision>PlatformInfo -> DataHub -> SmcRevision</h3>

**Type**: `plist data`, 6 bytes

**Failsafe**: Empty (Not installed)

**Description**: Sets `REV` in `gEfiMiscSubClassGuid`. Custom property read by `VirtualSMC` or `FakeSMC` to generate SMC `REV` key.

<h3 id=platforminfo-datahub-startuppowerevents>PlatformInfo -> DataHub -> StartupPowerEvents</h3>

**Type**: `plist integer`, 64-bit

**Failsafe**: `0`

**Description**: Sets `StartupPowerEvents` in `gEfiMiscSubClassGuid`. The value found on Macs is power management state bitmask, normally 0. Known bits read by
`X86PlatformPlugin.kext`:
* `0x00000001` --- Shutdown cause was a `PWROK` event (Same as `GEN_PMCON_2` bit 0)
* `0x00000002` --- Shutdown cause was a `SYS_PWROK` event (Same as `GEN_PMCON_2` bit 1)
* `0x00000004` --- Shutdown cause was a `THRMTRIP#` event (Same as `GEN_PMCON_2` bit 3)
* `0x00000008` --- Rebooted due to a SYS_RESET# event (Same as `GEN_PMCON_2` bit 4)
* `0x00000010` --- Power Failure (Same as `GEN_PMCON_3` bit 1 `PWR_FLR`)
* `0x00000020` --- Loss of RTC Well Power (Same as `GEN_PMCON_3` bit 2 `RTC_PWR_STS`)
* `0x00000040` --- General Reset Status (Same as `GEN_PMCON_3` bit 9 `GEN_RST_STS`)
* `0xffffff80` --- SUS Well Power Loss (Same as `GEN_PMCON_3` bit 14)
* `0x00010000` --- Wake cause was a ME Wake event (Same as PRSTS bit 0, `ME_WAKE_STS`)
* `0x00020000` --- Cold Reboot was ME Induced event (Same as `PRSTS` bit 1 `ME_HRST_COLD_STS`)
* `0x00040000` --- Warm Reboot was ME Induced event (Same as `PRSTS` bit 2 `ME_HRST_WARM_STS`)
* `0x00080000` --- Shutdown was ME Induced event (Same as `PRSTS` bit 3 `ME_HOST_PWRDN`)
* `0x00100000` --- Global reset ME Watchdog Timer event (Same as `PRSTS` bit 6)
* `0x00200000` --- Global reset PowerManagement Watchdog Timer event (Same as `PRSTS` bit 15)

<h3 id=platforminfo-datahub-systemproductname>PlatformInfo -> DataHub -> SystemProductName</h3>

**Type**: `plist string`

**Failsafe**: Empty (Not installed)

**Description**: Sets `Model` in `gEfiMiscSubClassGuid`. The value found on Macs is equal to SMBIOS `SystemProductName` in Unicode.

<h3 id=platforminfo-datahub-systemserialnumber>PlatformInfo -> DataHub -> SystemSerialNumber</h3>

**Type**: `plist string`

**Failsafe**: Empty (Not installed)

**Description**: Sets `SystemSerialNumber` in `gEfiMiscSubClassGuid`. The value found on Macs is equal to SMBIOS `SystemSerialNumber` in Unicode.

<h3 id=platforminfo-datahub-systemuuid>PlatformInfo -> DataHub -> SystemUUID</h3>

**Type**: `plist string`, GUID

**Failsafe**: Empty (Not installed)

**Description**: Sets `system-id` in `gEfiMiscSubClassGuid`. The value found on Macs is equal to SMBIOS `SystemUUID` (with swapped byte order).

<h2 id=platforminfo-generic>PlatformInfo -> Generic</h2>

**Type**: `plist dictionary`

**Description**: Update all fields in `Automatic` mode.

*Note*: This section is ignored but may not be removed when `Automatic` is `false`.

<h3 id=platforminfo-generic-advisefeatures>PlatformInfo -> Generic -> AdviseFeatures</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Updates `FirmwareFeatures` with supported bits.

Added bits to `FirmwareFeatures`:
* `FW_FEATURE_SUPPORTS_CSM_LEGACY_MODE` (`0x1`) - Without this bit, it is not possible to reboot to Windows installed on a drive with an EFI partition that is not the first partition on the disk.
* `FW_FEATURE_SUPPORTS_UEFI_WINDOWS_BOOT` (`0x20000000`) - Without this bit, it is not possible to reboot to Windows installed on a drive with an EFI partition that is the first partition on the disk.
* `FW_FEATURE_SUPPORTS_APFS` (`0x00080000`) - Without this bit, it is not possible to install macOS on an APFS disk.
* `FW_FEATURE_SUPPORTS_LARGE_BASESYSTEM` (`0x800000000`) - Without this bit, it is not possible to install macOS versions with large BaseSystem images, such as macOS 12. 

*Note*: On most newer firmwares these bits are already set, the option may be necessary when "upgrading" the firmware with new features.

<h3 id=platforminfo-generic-mlb>PlatformInfo -> Generic -> MLB</h3>

**Type**: `plist string`

**Default**: `M0000000000000001`

**Failsafe**: Empty (OEM specified or not installed)

**Description**: Refer to SMBIOS `BoardSerialNumber`.

Specify special string value `OEM` to extract current value from NVRAM (`MLB` variable) or SMBIOS and use it throughout the sections. This feature can only be used on Mac-compatible firmware.

<h3 id=platforminfo-generic-maxbiosversion>PlatformInfo -> Generic -> MaxBIOSVersion</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Sets `BIOSVersion` to `9999.999.999.999.999`, recommended for legacy Macs when using `Automatic` PlatformInfo, to avoid BIOS updates in unofficially supported macOS versions.

<h3 id=platforminfo-generic-processortype>PlatformInfo -> Generic -> ProcessorType</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0` (Automatic)

**Description**: Refer to SMBIOS `ProcessorType`.

<h3 id=platforminfo-generic-rom>PlatformInfo -> Generic -> ROM</h3>

**Type**: `plist multidata`, 6 bytes

**Default**: `0x112233445566`

**Failsafe**: Empty (OEM specified or not installed)

**Description**: Refer to `4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14:ROM`.

Specify special string value `OEM` to extract current value from NVRAM (`ROM` variable) and use it throughout the sections. This feature can only be used on Mac-compatible firmware.

<h3 id=platforminfo-generic-spoofvendor>PlatformInfo -> Generic -> SpoofVendor</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Sets SMBIOS vendor fields to `Acidanthera`.

It can be dangerous to use `'Apple'' in SMBIOS vendor fields for reasons outlined in the `SystemManufacturer` description. However, certain firmware may not provide valid values otherwise, which could obstruct the operation of some software.

<h3 id=platforminfo-generic-systemmemorystatus>PlatformInfo -> Generic -> SystemMemoryStatus</h3>

**Type**: `plist string`

**Default**: `Auto`

**Failsafe**: `Auto`

**Description**: Indicates whether system memory is upgradable in `PlatformFeature`. This controls the visibility of the Memory tab in `'About This Mac''.

Valid values:
* `Auto` --- use the original `PlatformFeature` value.
* `Upgradable` --- explicitly unset `PT_FEATURE_HAS_SOLDERED_SYSTEM_MEMORY` (`0x2`) in `PlatformFeature`.
* `Soldered` --- explicitly set `PT_FEATURE_HAS_SOLDERED_SYSTEM_MEMORY` (`0x2`) in `PlatformFeature`. 

*Note*: On certain Mac models, such as the `MacBookPro10,x` and any `MacBookAir`, SPMemoryReporter.spreporter will ignore `PT_FEATURE_HAS_SOLDERED_SYSTEM_MEMORY` and assume that system memory is non-upgradable.

<h3 id=platforminfo-generic-systemproductname>PlatformInfo -> Generic -> SystemProductName</h3>

**Type**: `plist string`

**Default**: `iMac19,1`

**Failsafe**: Empty (OEM specified or not installed)

**Description**: Refer to SMBIOS `SystemProductName`.

<h3 id=platforminfo-generic-systemserialnumber>PlatformInfo -> Generic -> SystemSerialNumber</h3>

**Type**: `plist string`

**Default**: `W00000000001`

**Failsafe**: Empty (OEM specified or not installed)

**Description**: Refer to SMBIOS `SystemSerialNumber`.

Specify special string value `OEM` to extract current value from NVRAM (`SSN` variable) or SMBIOS and use it throughout the sections. This feature can only be used on Mac-compatible firmware.

<h3 id=platforminfo-generic-systemuuid>PlatformInfo -> Generic -> SystemUUID</h3>

**Type**: `plist string`, GUID

**Default**: `00000000-0000-0000-0000-000000000000`

**Failsafe**: Empty (OEM specified or not installed)

**Description**: Refer to SMBIOS `SystemUUID`.

Specify special string value `OEM` to extract current value from NVRAM (`system-id` variable) or SMBIOS and use it throughout the sections. Since not every firmware implementation has valid (and unique) values, this feature is not applicable to some setups, and may provide unexpected results. It is highly recommended to specify the UUID explicitly. Refer to `UseRawUuidEncoding` to determine how SMBIOS value is parsed.

<h2 id=platforminfo-memory>PlatformInfo -> Memory</h2>

**Type**: `plist dictionary`

**Description**: Define custom memory configuration.

*Note*: This section is ignored and may be removed when `CustomMemory` is `false`.

<h3 id=platforminfo-memory-datawidth>PlatformInfo -> Memory -> DataWidth</h3>

**Type**: `plist integer`, 16-bit

**Failsafe**: `0xFFFF` (unknown)\**SMBIOS**: Memory Device (Type 17) --- Data Width

**Description**: Specifies the data width, in bits, of the memory. A `DataWidth` of `0` and a `TotalWidth` of `8` indicates that the device is being used solely to provide 8 error-correction bits.

<h3 id=platforminfo-memory-devices>PlatformInfo -> Memory -> Devices</h3>

**Type**: `plist array`

**Failsafe**: Empty

**Description**: Specifies the custom memory devices to be added.

To be filled with `plist dictionary` values, describing each memory device. Refer to the **Memory Devices Properties** section below. This should include all memory slots, even if unpopulated.

<h4 id=platforminfo-memory-devices-assettag>PlatformInfo -> Memory -> Devices[] -> AssetTag</h4>

**Type**: `plist string`

**Failsafe**: `Unknown`\**SMBIOS**: Memory Device (Type 17) --- Asset Tag

**Description**: Specifies the asset tag of this memory device.

<h4 id=platforminfo-memory-devices-banklocator>PlatformInfo -> Memory -> Devices[] -> BankLocator</h4>

**Type**: `plist string`

**Failsafe**: `Unknown`\**SMBIOS**: Memory Device (Type 17) --- Bank Locator

**Description**: Specifies the physically labeled bank where the memory device is located.

<h4 id=platforminfo-memory-devices-devicelocator>PlatformInfo -> Memory -> Devices[] -> DeviceLocator</h4>

**Type**: `plist string`

**Failsafe**: `Unknown`\**SMBIOS**: Memory Device (Type 17) --- Device Locator

**Description**: Specifies the physically-labeled socket or board position where the memory device is located.

<h4 id=platforminfo-memory-devices-manufacturer>PlatformInfo -> Memory -> Devices[] -> Manufacturer</h4>

**Type**: `plist string`

**Failsafe**: `Unknown`\**SMBIOS**: Memory Device (Type 17) --- Manufacturer

**Description**: Specifies the manufacturer of this memory device.

For empty slot this must be set to `NO DIMM` for macOS System Profiler to correctly display memory slots on certain Mac models, e.g. `MacPro7,1`. `MacPro7,1` imposes additional requirements on the memory layout:
* The amount of installed sticks must one of the following: 4, 6, 8, 10, 12. Using any different value will cause an error in the System Profiler.
* The amount of memory slots must equal to 12. Using any different value will cause an error in the System Profiler.
* Memory sticks must be installed in dedicated memory slots as explained on the [support page](https://support.apple.com/HT210103). SMBIOS memory devices are mapped to the following slots: `8, 7, 10, 9, 12, 11, 5, 6, 3, 4, 1, 2`.

<h4 id=platforminfo-memory-devices-partnumber>PlatformInfo -> Memory -> Devices[] -> PartNumber</h4>

**Type**: `plist string`

**Failsafe**: `Unknown`\**SMBIOS**: Memory Device (Type 17) --- Part Number

**Description**: Specifies the part number of this memory device.

<h4 id=platforminfo-memory-devices-serialnumber>PlatformInfo -> Memory -> Devices[] -> SerialNumber</h4>

**Type**: `plist string`

**Failsafe**: `Unknown`\**SMBIOS**: Memory Device (Type 17) --- Serial Number

**Description**: Specifies the serial number of this memory device.

<h4 id=platforminfo-memory-devices-size>PlatformInfo -> Memory -> Devices[] -> Size</h4>

**Type**: `plist integer`, 32-bit

**Failsafe**: `0`\**SMBIOS**: Memory Device (Type 17) --- Size

**Description**: Specifies the size of the memory device, in megabytes. `0` indicates this slot is not populated.

<h4 id=platforminfo-memory-devices-speed>PlatformInfo -> Memory -> Devices[] -> Speed</h4>

**Type**: `plist integer`, 16-bit

**Failsafe**: `0`\**SMBIOS**: Memory Device (Type 17) --- Speed

**Description**: Specifies the maximum capable speed of the device, in megatransfers per second (MT/s). `0` indicates an unknown speed.

<h3 id=platforminfo-memory-errorcorrection>PlatformInfo -> Memory -> ErrorCorrection</h3>

**Type**: `plist integer`, 8-bit

**Failsafe**: `0x03`\**SMBIOS**: Physical Memory Array (Type 16) --- Memory Error Correction

**Description**: Specifies the primary hardware error correction or detection method supported by the memory.
* `0x01` --- Other
* `0x02` --- Unknown
* `0x03` --- None
* `0x04` --- Parity
* `0x05` --- Single-bit ECC
* `0x06` --- Multi-bit ECC
* `0x07` --- CRC

<h3 id=platforminfo-memory-formfactor>PlatformInfo -> Memory -> FormFactor</h3>

**Type**: `plist integer`, 8-bit

**Failsafe**: `0x02`\**SMBIOS**: Memory Device (Type 17) --- Form Factor

**Description**: Specifies the form factor of the memory. On Macs, this should typically be DIMM or SODIMM. Commonly used form factors are listed below.

When `CustomMemory` is `false`, this value is automatically set based on Mac product name.

When `Automatic` is `true`, the original value from the the corresponding Mac model will be set if available. Otherwise, the value from `OcMacInfoLib` will be set. When `Automatic` is `false`, a user-specified value will be set if available. Otherwise, the original value from the firmware will be set. If no value is provided, the failsafe value will be set.
* `0x01` --- Other
* `0x02` --- Unknown
* `0x09` --- DIMM
* `0x0D` --- SODIMM
* `0x0F` --- FB-DIMM

<h3 id=platforminfo-memory-maxcapacity>PlatformInfo -> Memory -> MaxCapacity</h3>

**Type**: `plist integer`, 64-bit

**Failsafe**: `0`\**SMBIOS**: Physical Memory Array (Type 16) --- Maximum Capacity

**Description**: Specifies the maximum amount of memory, in bytes, supported by the system.

<h3 id=platforminfo-memory-totalwidth>PlatformInfo -> Memory -> TotalWidth</h3>

**Type**: `plist integer`, 16-bit

**Failsafe**: `0xFFFF` (unknown)\**SMBIOS**: Memory Device (Type 17) --- Total Width

**Description**: Specifies the total width, in bits, of the memory, including any check or error-correction bits. If there are no error-correction bits, this value should be equal to `DataWidth`.

<h3 id=platforminfo-memory-type>PlatformInfo -> Memory -> Type</h3>

**Type**: `plist integer`, 8-bit

**Failsafe**: `0x02`\**SMBIOS**: Memory Device (Type 17) --- Memory Type

**Description**: Specifies the memory type. Commonly used types are listed below.
* `0x01` --- Other
* `0x02` --- Unknown
* `0x0F` --- SDRAM
* `0x12` --- DDR
* `0x13` --- DDR2
* `0x14` --- DDR2 FB-DIMM
* `0x18` --- DDR3
* `0x1A` --- DDR4
* `0x1B` --- LPDDR
* `0x1C` --- LPDDR2
* `0x1D` --- LPDDR3
* `0x1E` --- LPDDR4

<h3 id=platforminfo-memory-typedetail>PlatformInfo -> Memory -> TypeDetail</h3>

**Type**: `plist integer`, 16-bit

**Failsafe**: `0x4`\**SMBIOS**: Memory Device (Type 17) --- Type Detail

**Description**: Specifies additional memory type information.
* `Bit 0` --- Reserved, set to 0
* `Bit 1` --- Other
* `Bit 2` --- Unknown
* `Bit 7` --- Synchronous
* `Bit 13` --- Registered (buffered)
* `Bit 14` --- Unbuffered (unregistered)

<h2 id=platforminfo-platformnvram>PlatformInfo -> PlatformNVRAM</h2>

**Type**: `plist dictionary`

**Description**: Update platform NVRAM fields in non-`Automatic` mode.

*Note*: This section is ignored and may be removed when `Automatic` is `true`.

<h3 id=platforminfo-platformnvram-bid>PlatformInfo -> PlatformNVRAM -> BID</h3>

**Type**: `plist string`

**Failsafe**: Empty (Not installed)

**Description**: Specifies the value of NVRAM variable `4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14:HW_BID`.

<h3 id=platforminfo-platformnvram-firmwarefeatures>PlatformInfo -> PlatformNVRAM -> FirmwareFeatures</h3>

**Type**: `plist data`, 8 bytes

**Failsafe**: Empty (Not installed)

**Description**: This variable comes in pair with `FirmwareFeaturesMask`. Specifies the values of NVRAM variables:
* `4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14:FirmwareFeatures`
* `4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14:ExtendedFirmwareFeatures`

<h3 id=platforminfo-platformnvram-firmwarefeaturesmask>PlatformInfo -> PlatformNVRAM -> FirmwareFeaturesMask</h3>

**Type**: `plist data`, 8 bytes

**Failsafe**: Empty (Not installed)

**Description**: This variable comes in pair with `FirmwareFeatures`. Specifies the values of NVRAM variables:
* `4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14:FirmwareFeaturesMask`
* `4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14:ExtendedFirmwareFeaturesMask`

<h3 id=platforminfo-platformnvram-mlb>PlatformInfo -> PlatformNVRAM -> MLB</h3>

**Type**: `plist string`

**Failsafe**: Empty (Not installed)

**Description**: Specifies the values of NVRAM variables `4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14:HW_MLB` and `4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14:MLB`.

<h3 id=platforminfo-platformnvram-rom>PlatformInfo -> PlatformNVRAM -> ROM</h3>

**Type**: `plist data`, 6 bytes

**Failsafe**: Empty (Not installed)

**Description**: Specifies the values of NVRAM variables `4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14:HW_ROM` and `4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14:ROM`.

<h3 id=platforminfo-platformnvram-systemserialnumber>PlatformInfo -> PlatformNVRAM -> SystemSerialNumber</h3>

**Type**: `plist string`

**Failsafe**: Empty (Not installed)

**Description**: Specifies the values of NVRAM variables `4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14:HW_SSN` and `4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14:SSN`.

<h3 id=platforminfo-platformnvram-systemuuid>PlatformInfo -> PlatformNVRAM -> SystemUUID</h3>

**Type**: `plist string`

**Failsafe**: Empty (Not installed)

**Description**: Specifies the value of NVRAM variable `4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14:system-id` for boot services only. The value found on Macs is equal to SMBIOS `SystemUUID`.

<h2 id=platforminfo-smbios>PlatformInfo -> SMBIOS</h2>

**Type**: `plist dictionary`

**Description**: Update SMBIOS fields in non-`Automatic` mode.

*Note*: This section is ignored and may be removed when `Automatic` is `true`.

<h3 id=platforminfo-smbios-biosreleasedate>PlatformInfo -> SMBIOS -> BIOSReleaseDate</h3>

**Type**: `plist string`

**Failsafe**: Empty (OEM specified)\**SMBIOS**: BIOS Information (Type 0) --- BIOS Release Date

**Description**: Firmware release date. Similar to `BIOSVersion`. May look like `12/08/2017`.

<h3 id=platforminfo-smbios-biosvendor>PlatformInfo -> SMBIOS -> BIOSVendor</h3>

**Type**: `plist string`

**Failsafe**: Empty (OEM specified)\**SMBIOS**: BIOS Information (Type 0) --- Vendor

**Description**: BIOS Vendor. All rules of `SystemManufacturer` do apply.

<h3 id=platforminfo-smbios-biosversion>PlatformInfo -> SMBIOS -> BIOSVersion</h3>

**Type**: `plist string`

**Failsafe**: Empty (OEM specified)\**SMBIOS**: BIOS Information (Type 0) --- BIOS Version

**Description**: Firmware version. This value gets updated and takes part in update delivery configuration and macOS version compatibility. This value could look like `MM71.88Z.0234.B00.1809171422` in older firmware and is described in [BiosId.h](https://github.com/acidanthera/OpenCorePkg/blob/master/Include/Apple/Guid/BiosId.h). In newer firmware, it should look like `236.0.0.0.0` or `220.230.16.0.0 (iBridge: 16.16.2542.0.0,0)`. iBridge version is read from `BridgeOSVersion` variable, and is only present on macs with T2.

<h3 id=platforminfo-smbios-boardassettag>PlatformInfo -> SMBIOS -> BoardAssetTag</h3>

**Type**: `plist string`

**Failsafe**: Empty (OEM specified)\**SMBIOS**: Baseboard (or Module) Information (Type 2) --- Asset Tag

**Description**: Asset tag number. Varies, may be empty or `Type2 - Board Asset Tag`.

<h3 id=platforminfo-smbios-boardlocationinchassis>PlatformInfo -> SMBIOS -> BoardLocationInChassis</h3>

**Type**: `plist string`

**Failsafe**: Empty (OEM specified)\**SMBIOS**: Baseboard (or Module) Information (Type 2) --- Location in Chassis

**Description**: Varies, may be empty or `Part Component`.

<h3 id=platforminfo-smbios-boardmanufacturer>PlatformInfo -> SMBIOS -> BoardManufacturer</h3>

**Type**: `plist string`

**Failsafe**: Empty (OEM specified)\**SMBIOS**: Baseboard (or Module) Information (Type 2) - Manufacturer

**Description**: Board manufacturer. All rules of `SystemManufacturer` do apply.

<h3 id=platforminfo-smbios-boardproduct>PlatformInfo -> SMBIOS -> BoardProduct</h3>

**Type**: `plist string`

**Failsafe**: Empty (OEM specified)\**SMBIOS**: Baseboard (or Module) Information (Type 2) - Product

**Description**: Mac Board ID (`board-id`). May look like `Mac-7BA5B2D9E42DDD94` or `Mac-F221BEC8` in older models.

<h3 id=platforminfo-smbios-boardserialnumber>PlatformInfo -> SMBIOS -> BoardSerialNumber</h3>

**Type**: `plist string`

**Failsafe**: Empty (OEM specified)\**SMBIOS**: Baseboard (or Module) Information (Type 2) --- Serial Number

**Description**: Board serial number in defined format. Known formats are described in [macserial](https://github.com/acidanthera/macserial/blob/master/FORMAT.md).

<h3 id=platforminfo-smbios-boardtype>PlatformInfo -> SMBIOS -> BoardType</h3>

**Type**: `plist integer`

**Failsafe**: `0` (OEM specified)\**SMBIOS**: Baseboard (or Module) Information (Type 2) --- Board Type

**Description**: Either `0xA` (Motherboard (includes processor, memory, and I/O) or `0xB` (Processor/Memory Module). Refer to Table 15 -- Baseboard: Board Type for details.

<h3 id=platforminfo-smbios-boardversion>PlatformInfo -> SMBIOS -> BoardVersion</h3>

**Type**: `plist string`

**Failsafe**: Empty (OEM specified)\**SMBIOS**: Baseboard (or Module) Information (Type 2) - Version

**Description**: Board version number. Varies, may match `SystemProductName` or `SystemProductVersion`.

<h3 id=platforminfo-smbios-chassisassettag>PlatformInfo -> SMBIOS -> ChassisAssetTag</h3>

**Type**: `plist string`

**Failsafe**: Empty (OEM specified)\**SMBIOS**: System Enclosure or Chassis (Type 3) --- Asset Tag Number

**Description**: Chassis type name. Varies, could be empty or `MacBook-Aluminum`.

<h3 id=platforminfo-smbios-chassismanufacturer>PlatformInfo -> SMBIOS -> ChassisManufacturer</h3>

**Type**: `plist string`

**Failsafe**: Empty (OEM specified)\**SMBIOS**: System Enclosure or Chassis (Type 3) --- Manufacturer

**Description**: Board manufacturer. All rules of `SystemManufacturer` do apply.

<h3 id=platforminfo-smbios-chassisserialnumber>PlatformInfo -> SMBIOS -> ChassisSerialNumber</h3>

**Type**: `plist string`

**Failsafe**: Empty (OEM specified)\**SMBIOS**: System Enclosure or Chassis (Type 3) --- Version

**Description**: Should match `SystemSerialNumber`.

<h3 id=platforminfo-smbios-chassistype>PlatformInfo -> SMBIOS -> ChassisType</h3>

**Type**: `plist integer`

**Failsafe**: `0` (OEM specified)\**SMBIOS**: System Enclosure or Chassis (Type 3) --- Type

**Description**: Chassis type. Refer to Table 17 --- System Enclosure or Chassis Types for details.

<h3 id=platforminfo-smbios-chassisversion>PlatformInfo -> SMBIOS -> ChassisVersion</h3>

**Type**: `plist string`

**Failsafe**: Empty (OEM specified)\**SMBIOS**: System Enclosure or Chassis (Type 3) --- Version

**Description**: Should match `BoardProduct`.

<h3 id=platforminfo-smbios-firmwarefeatures>PlatformInfo -> SMBIOS -> FirmwareFeatures</h3>

**Type**: `plist data`, 8 bytes

**Failsafe**: `0` (OEM specified on Apple hardware, 0 otherwise)\**SMBIOS**: `APPLE_SMBIOS_TABLE_TYPE128` - `FirmwareFeatures` and `ExtendedFirmwareFeatures`

**Description**: 64-bit firmware features bitmask. Refer to [AppleFeatures.h](https://github.com/acidanthera/OpenCorePkg/blob/master/Include/Apple/IndustryStandard/AppleFeatures.h) for details. Lower 32 bits match `FirmwareFeatures`. Upper 64 bits match `ExtendedFirmwareFeatures`.

<h3 id=platforminfo-smbios-firmwarefeaturesmask>PlatformInfo -> SMBIOS -> FirmwareFeaturesMask</h3>

**Type**: `plist data`, 8 bytes

**Failsafe**: `0` (OEM specified on Apple hardware, 0 otherwise)\**SMBIOS**: `APPLE_SMBIOS_TABLE_TYPE128` - `FirmwareFeaturesMask` and `ExtendedFirmwareFeaturesMask`

**Description**: Supported bits of extended firmware features bitmask. Refer to [AppleFeatures.h](https://github.com/acidanthera/OpenCorePkg/blob/master/Include/Apple/IndustryStandard/AppleFeatures.h) for details. Lower 32 bits match `FirmwareFeaturesMask`. Upper 64 bits match `ExtendedFirmwareFeaturesMask`.

<h3 id=platforminfo-smbios-platformfeature>PlatformInfo -> SMBIOS -> PlatformFeature</h3>

**Type**: `plist integer`, 32-bit

**Failsafe**: `0xFFFFFFFF` (OEM specified on Apple hardware, do not provide the table otherwise)\**SMBIOS**: `APPLE_SMBIOS_TABLE_TYPE133` - `PlatformFeature`

**Description**: Platform features bitmask (Missing on older Macs). Refer to [AppleFeatures.h](https://github.com/acidanthera/OpenCorePkg/blob/master/Include/Apple/IndustryStandard/AppleFeatures.h) for details.

<h3 id=platforminfo-smbios-processortype>PlatformInfo -> SMBIOS -> ProcessorType</h3>

**Type**: `plist integer`, 16-bit

**Failsafe**: `0` (Automatic)\**SMBIOS**: `APPLE_SMBIOS_TABLE_TYPE131` - `ProcessorType`

**Description**: Combined of Processor Major and Minor types.

Automatic value generation attempts to provide the most accurate value for the currently installed CPU. When this fails, please raise an [issue](https://github.com/acidanthera/bugtracker/issues) and provide `sysctl machdep.cpu` and [`dmidecode`](https://github.com/acidanthera/dmidecode) output. For a full list of available values and their limitations (the value will only apply if the CPU core count matches), refer to the Apple SMBIOS definitions header [here](https://github.com/acidanthera/OpenCorePkg/blob/master/Include/Apple/IndustryStandard/AppleSmBios.h).

<h3 id=platforminfo-smbios-smcversion>PlatformInfo -> SMBIOS -> SmcVersion</h3>

**Type**: `plist data`, 16 bytes

**Failsafe**: All zero (OEM specified on Apple hardware, do not provide the table otherwise)\**SMBIOS**: `APPLE_SMBIOS_TABLE_TYPE134` - `Version`

**Description**: ASCII string containing SMC version in upper case. Missing on T2 based Macs.

<h3 id=platforminfo-smbios-systemfamily>PlatformInfo -> SMBIOS -> SystemFamily</h3>

**Type**: `plist string`

**Failsafe**: Empty (OEM specified)\**SMBIOS**: System Information (Type 1) --- Family

**Description**: Family name. May look like `iMac Pro`.

<h3 id=platforminfo-smbios-systemmanufacturer>PlatformInfo -> SMBIOS -> SystemManufacturer</h3>

**Type**: `plist string`

**Failsafe**: Empty (OEM specified)\**SMBIOS**: System Information (Type 1) --- Manufacturer

**Description**: OEM manufacturer of the particular board. Use failsafe unless strictly required. Do not override to contain `Apple Inc.` on non-Apple hardware, as this confuses numerous services present in the operating system, such as firmware updates, eficheck, as well as kernel extensions developed in Acidanthera, such as Lilu and its plugins. In addition it will also make some operating systems such as Linux unbootable.

<h3 id=platforminfo-smbios-systemproductname>PlatformInfo -> SMBIOS -> SystemProductName</h3>

**Type**: `plist string`

**Failsafe**: Empty (OEM specified)\**SMBIOS**: System Information (Type 1), Product Name

**Description**: Preferred Mac model used to mark the device as supported by the operating system. This value must be specified by any configuration for later automatic generation of the related values in this and other SMBIOS tables and related configuration parameters. If `SystemProductName` is not compatible with the target operating system, `-no_compat_check` boot argument may be used as an override.

*Note*: If `SystemProductName` is unknown, and related fields are unspecified, default values should be assumed as being set to `MacPro6,1` data. The list of known products can be found in `AppleModels`.

<h3 id=platforminfo-smbios-systemskunumber>PlatformInfo -> SMBIOS -> SystemSKUNumber</h3>

**Type**: `plist string`

**Failsafe**: Empty (OEM specified)\**SMBIOS**: System Information (Type 1) --- SKU Number

**Description**: Mac Board ID (`board-id`). May look like `Mac-7BA5B2D9E42DDD94` or `Mac-F221BEC8` in older models. Sometimes it can be just empty.

<h3 id=platforminfo-smbios-systemserialnumber>PlatformInfo -> SMBIOS -> SystemSerialNumber</h3>

**Type**: `plist string`

**Failsafe**: Empty (OEM specified)\**SMBIOS**: System Information (Type 1) --- Serial Number

**Description**: Product serial number in defined format. Known formats are described in [macserial](https://github.com/acidanthera/OpenCorePkg/blob/master/Utilities/macserial/FORMAT.md).

<h3 id=platforminfo-smbios-systemuuid>PlatformInfo -> SMBIOS -> SystemUUID</h3>

**Type**: `plist string`, GUID

**Failsafe**: Empty (OEM specified)\**SMBIOS**: System Information (Type 1) --- UUID

**Description**: A UUID is an identifier that is designed to be unique across both time and space. It requires no central registration process.

<h3 id=platforminfo-smbios-systemversion>PlatformInfo -> SMBIOS -> SystemVersion</h3>

**Type**: `plist string`

**Failsafe**: Empty (OEM specified)\**SMBIOS**: System Information (Type 1) --- Version

**Description**: Product iteration version number. May look like `1.1`.

<h2 id=platforminfo-updatedatahub>PlatformInfo -> UpdateDataHub</h2>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Update Data Hub fields. These fields are read from the `Generic` or `DataHub` sections depending on the setting of the `Automatic` property.

*Note*: The implementation of the Data Hub protocol in EFI firmware on virtually all systems, including Apple hardware, means that existing Data Hub entries cannot be overridden. New entries are added to the end of the Data Hub instead, with macOS ignoring old entries. This can be worked around by replacing the Data Hub protocol using the `ProtocolOverrides` section. Refer to the `DataHub` protocol override description for details.

<h2 id=platforminfo-updatenvram>PlatformInfo -> UpdateNVRAM</h2>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Update NVRAM fields related to platform information.

These fields are read from the `Generic` or `PlatformNVRAM` sections depending on the setting of the `Automatic` property. All the other fields are to be specified with the `NVRAM` section.

If `UpdateNVRAM` is set to `false`, the aforementioned variables can be updated with the **`NVRAM`** section. If `UpdateNVRAM` is set to `true`, the behaviour is undefined when any of the fields are present in the `NVRAM` section.

<h2 id=platforminfo-updatesmbios>PlatformInfo -> UpdateSMBIOS</h2>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Update SMBIOS fields. These fields are read from the `Generic` or `SMBIOS` sections depending on the setting of the `Automatic` property.

<h2 id=platforminfo-updatesmbiosmode>PlatformInfo -> UpdateSMBIOSMode</h2>

**Type**: `plist string`

**Default**: `Create`

**Failsafe**: `Create`

**Description**: Update SMBIOS fields approach:
* `TryOverwrite` --- `Overwrite` if new size is \textless{}= than the page-aligned original and there are no issues with legacy region unlock. `Create` otherwise. Has issues on some types of firmware.
* `Create` --- Replace the tables with newly allocated EfiReservedMemoryType at AllocateMaxAddress without any fallbacks.
* `Overwrite` --- Overwrite existing gEfiSmbiosTableGuid and gEfiSmbiosTable3Guid data if it fits new size. Abort with unspecified state otherwise.
* `Custom` --- Write SMBIOS tables (`gEfiSmbios(3)TableGuid`) to `gOcCustomSmbios(3)TableGuid` to workaround firmware overwriting SMBIOS contents at ExitBootServices. Otherwise equivalent to `Create`. Requires patching AppleSmbios.kext and AppleACPIPlatform.kext to read from another GUID: `"EB9D2D31"` - `"EB9D2D35"` (in ASCII), done automatically by `CustomSMBIOSGuid` quirk. 

*Note*: A side effect of using the `Custom` approach that it makes SMBIOS updates exclusive to macOS, avoiding a collision with existing Windows activation and custom OEM software but potentially obstructing the operation of Apple-specific tools.

<h2 id=platforminfo-userawuuidencoding>PlatformInfo -> UseRawUuidEncoding</h2>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Use raw encoding for SMBIOS UUIDs.

Each UUID `AABBCCDD-EEFF-GGHH-IIJJ-KKLLMMNNOOPP` is essentially a hexadecimal 16-byte number. It can be encoded in two ways:
* `Big Endian` --- by writing all the bytes as they are without making any order changes (`{AA BB CC DD EE FF GG HH II JJ KK LL MM NN OO PP\`}). This method is also known as [RFC 4122](https://tools.ietf.org/html/rfc4122) encoding or `Raw` encoding.
* `Little Endian` --- by interpreting the bytes as numbers and using Little Endian byte representation (`{DD CC BB AA FF EE HH GG II JJ KK LL MM NN OO PP\`}). 

The SMBIOS specification did not explicitly specify the encoding format for the UUID up to SMBIOS 2.6, where it stated that `Little Endian` encoding shall be used. This led to the confusion in both firmware implementations and system software as different vendors used different encodings prior to that.
* Apple uses the `Big Endian` format everywhere but it ignores SMBIOS UUID within macOS.
* `dmidecode` uses the `Big Endian` format for SMBIOS 2.5.x or lower and the `Little Endian` format for 2.6 and newer. Acidanthera [dmidecode](https://github.com/acidanthera/dmidecode) prints all three.
* Windows uses the `Little Endian` format everywhere, but this only affects the visual representation of the values. 

OpenCore always sets a recent SMBIOS version (currently 3.2) when generating the modified DMI tables. If `UseRawUuidEncoding` is enabled, the `Big Endian` format is used to store the `SystemUUID` data. Otherwise, the `Little Endian` format is used.

*Note*: This preference does not affect UUIDs used in DataHub and NVRAM as they are not standardised and are added by Apple. Unlike SMBIOS, they are always stored in the `Big Endian` format.

<h2 id=uefi-apfs>UEFI -> APFS</h2>

**Type**: `plist dict`

**Description**: Provide APFS support as configured in the **APFS Properties** section below.

<h3 id=uefi-apfs-enablejumpstart>UEFI -> APFS -> EnableJumpstart</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Load embedded APFS drivers from APFS containers.

An APFS EFI driver is bundled in all bootable APFS containers. This option performs the loading of signed APFS drivers (consistent with the `ScanPolicy`). Refer to the `'EFI Jumpstart'' section of the [Apple File System Reference](https://developer.apple.com/support/apple-file-system/Apple-File-System-Reference.pdf) for details.

<h3 id=uefi-apfs-globalconnect>UEFI -> APFS -> GlobalConnect</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Perform full device connection during APFS loading.

Every handle is connected recursively instead of the partition handle connection typically used for APFS driver loading. This may result in additional time being taken but can sometimes be the only way to access APFS partitions on certain firmware, such as those on older HP laptops.

<h3 id=uefi-apfs-hideverbose>UEFI -> APFS -> HideVerbose</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Hide verbose output from APFS driver.

APFS verbose output can be useful for debugging.

<h3 id=uefi-apfs-jumpstarthotplug>UEFI -> APFS -> JumpstartHotPlug</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Load APFS drivers for newly connected devices.

Permits APFS USB hot plug which enables loading APFS drivers, both at OpenCore startup and during OpenCore picker display. Disable if not required.

<h3 id=uefi-apfs-mindate>UEFI -> APFS -> MinDate</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0`

**Description**: Minimal allowed APFS driver date.

The APFS driver date connects the APFS driver with the calendar release date. Apple ultimately drops support for older macOS releases and APFS drivers from such releases may contain vulnerabilities that can be used to compromise a computer if such drivers are used after support ends. This option permits restricting APFS drivers to current macOS versions.
* `0` --- require the default supported release date of APFS in OpenCore. The default release date will increase with time and thus this setting is recommended. Currently set to 2021/01/01.
* `-1` --- permit any release date to load (strongly discouraged).
* Other --- use custom minimal APFS release date, e.g. `20200401` for 2020/04/01. APFS release dates can be found in OpenCore boot log and [`OcApfsLib`](https://github.com/acidanthera/OpenCorePkg/blob/master/Include/Acidanthera/Library/OcApfsLib.h).

<h3 id=uefi-apfs-minversion>UEFI -> APFS -> MinVersion</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0`

**Description**: Minimal allowed APFS driver version.

The APFS driver version connects the APFS driver with the macOS release. Apple ultimately drops support for older macOS releases and APFS drivers from such releases may contain vulnerabilities that can be used to compromise a computer if such drivers are used after support ends. This option permits restricting APFS drivers to current macOS versions.
* `0` --- require the default supported version of APFS in OpenCore. The default version will increase with time and thus this setting is recommended. Currently set to allow macOS Big Sur and newer (`1600000000000000`).
* `-1` --- permit any version to load (strongly discouraged).
* Other --- use custom minimal APFS version, e.g. `1412101001000000` from macOS Catalina 10.15.4. APFS versions can be found in OpenCore boot log and [`OcApfsLib`](https://github.com/acidanthera/OpenCorePkg/blob/master/Include/Acidanthera/Library/OcApfsLib.h).

<h2 id=uefi-appleinput>UEFI -> AppleInput</h2>

**Type**: `plist dict`

**Description**: Configure the re-implementation of the Apple Event protocol described in the **AppleInput Properties** section below.

<h3 id=uefi-appleinput-appleevent>UEFI -> AppleInput -> AppleEvent</h3>

**Type**: `plist string`

**Default**: `Builtin`

**Failsafe**: `Auto`

**Description**: Determine whether the OpenCore builtin or the OEM Apple Event protocol is used.

This option determines whether the OEM Apple Event protocol is used (where available), or whether OpenCore's reversed engineered and updated re-implementation is used. In general OpenCore's re-implementation should be preferred, since it contains updates such as noticeably improved fine mouse cursor movement and configurable key repeat delays.
* `Auto` --- Use the OEM Apple Event implementation if available, connected and recent enough to be used, otherwise use the OpenCore re-implementation. On non-Apple hardware, this will use the OpenCore builtin implementation. On some Macs such as Classic Mac Pros, this will prefer the Apple implementation but on both older and newer Mac models than these, this option will typically use the OpenCore re-implementation instead. On older Macs, this is because the implementation available is too old to be used while on newer Macs, it is because of optimisations added by Apple which do not connect the Apple Event protocol except when needed -- e.g. except when the Apple boot picker is explicitly started. Due to its somewhat unpredicatable results, this option is not typically recommended.
* `Builtin` ---Always use OpenCore's updated re-implementation of the Apple Event protocol. Use of this setting is recommended even on Apple hardware, due to improvements (better fine mouse control, configurable key delays) made in the OpenCore re-implementation of the protocol.
* `OEM` --- Assume Apple's protocol will be available at driver connection. On all Apple hardware where a recent enough Apple OEM version of the protocol is available -- whether or not connected automatically by Apple's firmware -- this option will reliably access the Apple implementation. On all other systems, this option will result in no keyboard or mouse support. For the reasons stated, `Builtin` is recommended in preference to this option in most cases.

<h3 id=uefi-appleinput-customdelays>UEFI -> AppleInput -> CustomDelays</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Enable custom key repeat delays when using the OpenCore re-implementation of the Apple Event protocol. Has no effect when using the OEM Apple implementation (see `AppleEvent` setting).
* `true` --- The values of `KeyInitialDelay` and `KeySubsequentDelay` are used.
* `false` --- Apple default values of 500ms (`50`) and 50ms (`5`) are used.

<h3 id=uefi-appleinput-graphicsinputmirroring>UEFI -> AppleInput -> GraphicsInputMirroring</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Apple’s own implementation of AppleEvent prevents keyboard input during graphics applications from appearing on the basic console input stream.

With the default setting of `false`, OpenCore's builtin implementation of AppleEvent replicates this behaviour.

On non-Apple hardware this can stop keyboard input working in graphics-based applications such as Windows BitLocker which use non-Apple key input methods.

The recommended setting on all hardware is `true`.

*Note*: AppleEvent's default behaviour is intended to prevent unwanted queued keystrokes from appearing after exiting graphics-based UEFI applications; this issue is already handled separately within OpenCore.
* `true` --- Allow keyboard input to reach graphics mode apps which are not using Apple input protocols.
* `false` --- Prevent key input mirroring to non-Apple protocols when in graphics mode.

<h3 id=uefi-appleinput-keyinitialdelay>UEFI -> AppleInput -> KeyInitialDelay</h3>

**Type**: `plist integer`

**Default**: `50`

**Failsafe**: `50` (500ms before first key repeat)

**Description**: Configures the initial delay before keyboard key repeats in the OpenCore re-implementation of the Apple Event protocol, in units of 10ms.

The Apple OEM default value is `50` (500ms).

*Note 1*: On systems not using `KeySupport`, this setting may be freely used to configure key repeat behaviour.

*Note 2*: On systems using `KeySupport`, but which do not show the 'two long delays' behavior (see Note 3) and/or which always show a solid 'set default' indicator (see `KeyForgetThreshold`) then this setting may also be freely used to configure key repeat initial delay behaviour, except that it should never be set to less than `KeyForgetThreshold` to avoid uncontrolled key repeats.

*Note 3*: On some systems using `KeySupport`, you may find that you see one additional slow key repeat before normal speed key repeat starts, when holding a key down. If so, you may wish to configure `KeyInitialDelay` and `KeySubsequentDelay` according to the instructions at Note 3 of `KeySubsequentDelay`.

<h3 id=uefi-appleinput-keysubsequentdelay>UEFI -> AppleInput -> KeySubsequentDelay</h3>

**Type**: `plist integer`

**Default**: `5`

**Failsafe**: `5` (50ms between subsequent key repeats)

**Description**: Configures the gap between keyboard key repeats in the OpenCore re-implementation of the Apple Event protocol, in units of 10ms.

The Apple OEM default value is `5` (50ms). `0` is an invalid value for this option (will issue a debug log warning and use `1` instead).

*Note 1*: On systems not using `KeySupport`, this setting may be freely used to configure key repeat behaviour.

*Note 2*: On systems using `KeySupport`, but which do not show the 'two long delays' behaviour (see Note 3) and/or which always show a solid 'set default' indicator (see `KeyForgetThreshold`) (which should apply to many/most systems using `AMI` `KeySupport` mode) then this setting may be freely used to configure key repeat subsequent delay behaviour, except that it should never be set to less than `KeyForgetThreshold` to avoid uncontrolled key repeats.

*Note 3*: On some systems using `KeySupport`, particularly `KeySupport` in non-`AMI` mode, you may find that after configuring `KeyForgetThreshold` you get one additional slow key repeat before normal speed key repeat starts, when holding a key down. On systems where this is the case, it is an unavoidable artefect of using `KeySupport` to emulate raw keyboard data, which is not made available by UEFI. While this 'two long delays' issue has minimal effect on overall usability, nevertheless you may wish to resolve it, and it is possible to do so as follows:
* Set `CustomDelays` to `true`
* Set `KeyInitialDelay` to `0`
* Set `KeySubsequentDelay` to at least the value of your `KeyForgetThreshold` setting  The above procedure works as follows:
* Setting `KeyInitialDelay` to `0` cancels the Apple Event initial repeat delay (when using the OpenCore builtin Apple Event implementation with `CustomDelays` enabled), therefore the only long delay you will see is the the non-configurable and non-avoidable initial long delay introduced by the BIOS key support on these machines.
* Key-smoothing parameter `KeyForgetThreshold` effectively acts as the shortest time for which a key can appear to be held, therefore a key repeat delay of less than this will guarantee at least one extra repeat for every key press, however quickly the key is physically tapped.
* In the unlikely event that you still get frequent, or occasional, double key responses after setting `KeySubsequentDelay` equal to your system's value of `KeyForgetThreshold`, then increase `KeySubsequentDelay` by one or two more until this effect goes away.

<h3 id=uefi-appleinput-pointerdwellclicktimeout>UEFI -> AppleInput -> PointerDwellClickTimeout</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0`

**Description**: Configure pointer dwell-clicking single left click timeout in milliseconds in the OpenCore re-implementation of the Apple Event protocol. Has no effect when using the OEM Apple implementation (see `AppleEvent` setting).

When the timeout expires, a single left click is issued at the current position. `0` indicates the timeout is disabled.

<h3 id=uefi-appleinput-pointerdwelldoubleclicktimeout>UEFI -> AppleInput -> PointerDwellDoubleClickTimeout</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0`

**Description**: Configure pointer dwell-clicking single left double click timeout in milliseconds in the OpenCore re-implementation of the Apple Event protocol. Has no effect when using the OEM Apple implementation (see `AppleEvent` setting).

When the timeout expires, a single left double click is issued at the current position. `0` indicates the timeout is disabled.

<h3 id=uefi-appleinput-pointerdwellradius>UEFI -> AppleInput -> PointerDwellRadius</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0`

**Description**: Configure pointer dwell-clicking tolerance radius in pixels in the OpenCore re-implementation of the Apple Event protocol. Has no effect when using the OEM Apple implementation (see `AppleEvent` setting).

The radius is scaled by `UIScale`. When the pointer leaves this radius, the timeouts for `PointerDwellClickTimeout` and `PointerDwellDoubleClickTimeout` are reset and the new position is the centre for the new dwell-clicking tolerance radius.

<h3 id=uefi-appleinput-pointerpollmask>UEFI -> AppleInput -> PointerPollMask</h3>

**Type**: `plist integer, 32 bit`

**Default**: `-1`

**Failsafe**: `-1`

**Description**: Configure indices of polled pointers.

Selects pointer devices to poll for AppleEvent motion events. `-1` implies all devices. A bit sum is used to determine particular devices. E.g. to enable devices 0, 2, 3 the value will be `1+4+8` (corresponding powers of two). A total of 32 configurable devices is supported.

Certain pointer devices can be present in the firmware even when no corresponding physical devices are available. These devices usually are placeholders, aggregate devices, or proxies. Gathering information from these devices may result in inaccurate motion activity in the user interfaces and even cause performance issues. Disabling such pointer devices is recommended for laptop setups having issues of this kind.

The amount of pointer devices available in the system can be found in the log. Refer to `Found N pointer devices` message for more details.

*Note*: Has no effect when using the OEM Apple implementation (see `AppleEvent` setting).

<h3 id=uefi-appleinput-pointerpollmax>UEFI -> AppleInput -> PointerPollMax</h3>

**Type**: `plist integer`

**Default**: `80`

**Failsafe**: `0`

**Description**: Configure maximum pointer polling period in ms.

This is the maximum period the OpenCore builtin AppleEvent driver polls pointer devices (e.g. mice, trackpads) for motion events. The period is increased up to this value as long as the devices do not respond in time. The current implementation defaults to 80 ms. Setting `0` leaves this default unchanged.

Certain trackpad drivers often found in Dell laptops can be very slow to respond when no physical movement happens. This can affect OpenCanopy and FileVault 2 user interface responsiveness and loading times. Increasing the polling periods can reduce the impact.

*Note*: The OEM Apple implementation uses a polling rate of 2 ms.

<h3 id=uefi-appleinput-pointerpollmin>UEFI -> AppleInput -> PointerPollMin</h3>

**Type**: `plist integer`

**Default**: `10`

**Failsafe**: `0`

**Description**: Configure minimal pointer polling period in ms.

This is the minimal period the OpenCore builtin AppleEvent driver polls pointer devices (e.g. mice, trackpads) for motion events. The current implementation defaults to 10 ms. Setting `0` leaves this default unchanged.

*Note*: The OEM Apple implementation uses a polling rate of 2 ms.

<h3 id=uefi-appleinput-pointerspeeddiv>UEFI -> AppleInput -> PointerSpeedDiv</h3>

**Type**: `plist integer`

**Default**: `1`

**Failsafe**: `1`

**Description**: Configure pointer speed divisor in the OpenCore re-implementation of the Apple Event protocol. Has no effect when using the OEM Apple implementation (see `AppleEvent` setting).

Configures the divisor for pointer movements. The Apple OEM default value is `1`. `0` is an invalid value for this option.

*Note*: The recommended value for this option is `1`. This value may optionally be modified in combination with `PointerSpeedMul`, according to user preference, to achieve customised mouse movement scaling.

<h3 id=uefi-appleinput-pointerspeedmul>UEFI -> AppleInput -> PointerSpeedMul</h3>

**Type**: `plist integer`

**Default**: `1`

**Failsafe**: `1`

**Description**: Configure pointer speed multiplier in the OpenCore re-implementation of the Apple Event protocol. Has no effect when using the OEM Apple implementation (see `AppleEvent` setting).

Configures the multiplier for pointer movements. The Apple OEM default value is `1`.

*Note*: The recommended value for this option is `1`. This value may optionally be modified in combination with `PointerSpeedDiv`, according to user preference, to achieve customised mouse movement scaling.

<h2 id=uefi-audio>UEFI -> Audio</h2>

**Type**: `plist dict`

**Description**: Configure audio backend support described in the **`Audio Properties`** section below.

Unless documented otherwise (e.g. `ResetTrafficClass`) settings in this section are for UEFI audio support only (e.g. OpenCore generated boot chime and audio assist) and are unrelated to any configuration needed for OS audio support (e.g. `AppleALC`).

UEFI audio support provides a way for upstream protocols to interact with the selected audio hardware and resources. All audio resources should reside in `\EFI\OC\Resources\Audio` directory. Currently the supported audio file formats are MP3 and WAVE PCM. While it is driver-dependent which audio stream format is supported, most common audio cards support 16-bit signed stereo audio at 44100 or 48000 Hz.

Audio file path is determined by audio type, audio localisation, and audio path. Each filename looks as follows: `[audio type]_[audio localisation]_[audio path].[audio ext]`. For unlocalised files filename does not include the language code and looks as follows: `[audio type]_[audio path].[audio ext]`. Audio extension can either be `mp3` or `wav`.
* Audio type can be `OCEFIAudio` for OpenCore audio files or `AXEFIAudio` for macOS bootloader audio files.
* Audio localisation is a two letter language code (e.g. `en`) with an exception for Chinese, Spanish, and Portuguese. Refer to [`APPLE_VOICE_OVER_LANGUAGE_CODE` definition](https://github.com/acidanthera/OpenCorePkg/blob/master/Include/Apple/Protocol/AppleVoiceOver.h) for the list of all supported localisations.
* Audio path is the base filename corresponding to a file identifier. For macOS bootloader audio paths refer to [`APPLE_VOICE_OVER_AUDIO_FILE` definition](https://github.com/acidanthera/OpenCorePkg/blob/master/Include/Apple/Protocol/AppleVoiceOver.h). For OpenCore audio paths refer to [`OC_VOICE_OVER_AUDIO_FILE` definition](https://github.com/acidanthera/OpenCorePkg/blob/master/Include/Acidanthera/Protocol/OcAudio.h). The only exception is OpenCore boot chime file, which is `OCEFIAudio_VoiceOver_Boot.mp3`. 

Audio localisation is determined separately for macOS bootloader and OpenCore. For macOS bootloader it is set in `preferences.efires` archive in `systemLanguage.utf8` file and is controlled by the operating system. For OpenCore the value of `prev-lang:kbd` variable is used. When native audio localisation of a particular file is missing, English language (`en`) localisation is used. Sample audio files can be found in [OcBinaryData repository](https://github.com/acidanthera/OcBinaryData).

<h3 id=uefi-audio-audiocodec>UEFI -> Audio -> AudioCodec</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0`

**Description**: Codec address on the specified audio controller for audio support.

This typically contains the first audio codec address on the builtin analog audio controller (`HDEF`). Audio codec addresses, e.g. `2`, can be found in the debug log (marked in bold-italic):
* `OCAU: 1/3 PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x1)/VenMsg(<redacted>,***00000000***) (4 outputs)`
* `OCAU: 2/3 PciRoot(0x0)/Pci(0x3,0x0)/VenMsg(<redacted>,***00000000***) (1 outputs)`
* `OCAU: 3/3 PciRoot(0x0)/Pci(0x1B,0x0)/VenMsg(<redacted>,***02000000***) (7 outputs)`

As an alternative, this value can be obtained from `IOHDACodecDevice` class in I/O Registry containing it in `IOHDACodecAddress` field.

<h3 id=uefi-audio-audiodevice>UEFI -> Audio -> AudioDevice</h3>

**Type**: `plist string`

**Default**: `PciRoot(0x0)/Pci(0x1b,0x0)`

**Failsafe**: Empty

**Description**: Device path of the specified audio controller for audio support.

This typically contains builtin analog audio controller (`HDEF`) device path, e.g. `PciRoot(0x0)/Pci(0x1b,0x0)`. The list of recognised audio controllers can be found in the debug log (marked in bold-italic):
* `OCAU: 1/3 ***PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x1)***/VenMsg(<redacted>,00000000) (4 outputs)`
* `OCAU: 2/3 ***PciRoot(0x0)/Pci(0x3,0x0)***/VenMsg(<redacted>,00000000) (1 outputs)`
* `OCAU: 3/3 ***PciRoot(0x0)/Pci(0x1B,0x0)***/VenMsg(<redacted>,02000000) (7 outputs)`

If using `AudioDxe`, the available controller device paths are also output on lines formatted like this:
* `HDA: Connecting controller - ***PciRoot(0x0)/Pci(0x1B,0x0)***`

Finally, `gfxutil -f HDEF` command can be used in macOS to obtain the device path.

Specifying an empty device path results in the first available codec and audio controller being used. The value of `AudioCodec` is ignored in this case. This can be a convenient initial option to try to get UEFI audio working. Manual settings as above will be required when this default value does not work.

<h3 id=uefi-audio-audiooutmask>UEFI -> Audio -> AudioOutMask</h3>

**Type**: `plist integer`

**Default**: `1`

**Failsafe**: `-1`

**Description**: Bit field indicating which output channels to use for UEFI sound.

Audio mask is 1 << audio output (equivalently 2 `^{`} audio output). E.g. for audio output `0` the bitmask is `1`, for output `3` it is `8`, and for outputs `0` and `3` it is `9`.

The number of available output nodes (`N`) for each HDA codec is shown in the debug log (marked in bold-italic), audio outputs `0` to `N - 1` may be selected:
* `OCAU: 1/3 PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x1)/VenMsg(<redacted>,00000000) (***4 outputs***)`
* `OCAU: 2/3 PciRoot(0x0)/Pci(0x3,0x0)/VenMsg(<redacted>,00000000) (***1 outputs***)`
* `OCAU: 3/3 PciRoot(0x0)/Pci(0x1B,0x0)/VenMsg(<redacted>,02000000) (***7 outputs***)`

When `AudioDxe` is used then additional information about each output channel is logged during driver binding, including the bitmask for each output. The bitmask values for the desired outputs should be added together to obtain the `AudioOutMask` value:
* `HDA:| Port widget @ 0x9 is an output (pin defaults 0x2B4020) (***bitmask 1***)`
* `HDA:| Port widget @ 0xA is an output (pin defaults 0x90100112) (***bitmask 2***)`
* `HDA:| Port widget @ 0xB is an output (pin defaults 0x90100110) (***bitmask 4***)`
* `HDA:| Port widget @ 0x10 is an output (pin defaults 0x4BE030) (***bitmask 8***)`

Further information on the available output channels may be found from a Linux codec dump using the command:

`cat /proc/asound/card{n\`/codec#{m}}

Using `AudioOutMask`, it is possible to play sound to more than one channel (e.g. main speaker plus bass speaker; headphones plus speakers) as long as all the chosen outputs support the sound file format in use; if any do not then no sound will play and a warning will be logged.

When all available output channels on the codec support the available sound file format then a value of `-1` will play sound to all channels simultaneously. If this does not work it will usually be quickest to try each available output channel one by one, by setting `AudioOutMask` to `1`, `2`, `4`, etc., up to 2 `^{`} `N - 1`, in order to work out which channel(s) produce sound.

<h3 id=uefi-audio-audiosupport>UEFI -> Audio -> AudioSupport</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Activate audio support by connecting to a backend driver.

Enabling this setting routes audio playback from builtin protocols to specified (`AudioOutMask`) dedicated audio ports of the specified codec (`AudioCodec`), located on the specified audio controller (`AudioDevice`).

<h3 id=uefi-audio-disconnecthda>UEFI -> Audio -> DisconnectHda</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Disconnect HDA controller before loading drivers.

May be required on some systems (e.g. Apple hardware, VMware Fusion guest) to allow a UEFI sound driver (such as `AudioDxe`) to take control of the audio hardware.

*Note*: In addition to this option, most Apple hardware also requires the `-{`-gpio-setup} driver argument which is dealt with in the **AudioDxe** section.

<h3 id=uefi-audio-maximumgain>UEFI -> Audio -> MaximumGain</h3>

**Type**: `plist integer`

**Default**: `-15`

**Failsafe**: `-15`

**Description**: Maximum gain to use for UEFI audio, specified in decibels (dB) with respect to amplifier reference level of 0 dB (see note 1).

All UEFI audio will use this gain setting when the system amplifier gain read from the `SystemAudioVolumeDB` NVRAM variable is higher than this. This is to avoid over-loud UEFI audio when the system volume is set very high, or the `SystemAudioVolumeDB` NVRAM value has been misconfigured.

*Note 1*: Decibels (dB) specify gain (postive values; increase in volume) or attenuation (negative values; decrease in volume) compared to some reference level. When you hear the sound level of a jet plane expressed as 120 decibels, say, the reference level is the sound level just audible to an average human. However generally in acoustic science and computer audio any reference level can be specified. Intel HDA and macOS natively use decibels to specify volume level. On most Intel HDA hardware the reference level of 0 dB is the *loudest* volume of the hardware, and all lower volumes are therefore negative numbers. The quietest volume on typical sound hardware is around -55 dB to -60 dB.

*Note 2*: Matching how macOS handles decibel values, this value is converted to a signed byte; therefore values outside $-128$ dB to $+127$ dB (which are well beyond physically plausible volume levels) are not allowed.

*Note 3*: Digital audio output -- which does not have a volume slider in-OS -- ignores this and all other gain settings, only mute settings are relevant.

<h3 id=uefi-audio-minimumassistgain>UEFI -> Audio -> MinimumAssistGain</h3>

**Type**: `plist integer`

**Default**: `-30`

**Failsafe**: `-30`

**Description**: Minimum gain in decibels (dB) to use for picker audio assist.

The screen reader will use this amplifier gain if the system amplifier gain read from the `SystemAudioVolumeDB` NVRAM variable is lower than this.

*Note 1*: In addition to this setting, because audio assist must be audible to serve its function, audio assist is not muted even if the OS sound is muted or the `StartupMute` NVRAM variable is set.

*Note 2*: See `MaximumGain` for an explanation of decibel volume levels.

<h3 id=uefi-audio-minimumaudiblegain>UEFI -> Audio -> MinimumAudibleGain</h3>

**Type**: `plist integer`

**Default**: `-55`

**Failsafe**: `-128`

**Description**: Minimum gain in decibels (dB) at which to attempt to play any sound.

The boot chime will not play if the system amplifier gain level in the `SystemAudioVolumeDB` NVRAM variable is lower than this.

*Note 1*: This setting is designed to save unecessary pauses due to audio setup at inaudible volume levels, when no sound will be heard anyway. Whether there are inaudible volume levels depends on the hardware. On some hardware (including Apple) the audio values are well enough matched to the hardware that the lowest volume levels available are very quiet but audible, whereas on some other hardware combinations, the lowest part of the volume range may not be audible at all.

*Note 2*: See `MaximumGain` for an explanation of decibel volume levels.

<h3 id=uefi-audio-playchime>UEFI -> Audio -> PlayChime</h3>

**Type**: `plist string`

**Default**: `Auto`

**Failsafe**: `Auto`

**Description**: Play chime sound at startup.

Enabling this setting plays the boot chime using the builtin audio support. The volume level is determined by the `SystemAudioVolumeDB` NVRAM variable. Supported values are:
* `Auto` --- Enables chime when `StartupMute` NVRAM variable is not present or set to `00`.
* `Enabled` --- Enables chime unconditionally.
* `Disabled` --- Disables chime unconditionally. 

*Note 1*: `Enabled` can be used separately from the `StartupMute` NVRAM variable to avoid conflicts when the firmware is able to play the boot chime.

*Note 2*: Regardless of this setting, the boot chime will not play if system audio is muted, i.e.~if the `SystemAudioVolume` NVRAM variable has bit `0x80` set.

<h3 id=uefi-audio-resettrafficclass>UEFI -> Audio -> ResetTrafficClass</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Set HDA Traffic Class Select Register to `TC0`.

AppleHDA kext will function correctly only if `TCSEL` register is configured to use `TC0` traffic class. Refer to Intel I/O Controller Hub 9 (ICH9) Family Datasheet (or any other ICH datasheet) for more details about this register.

*Note*: This option is independent from `AudioSupport`. If AppleALC is used it is preferred to use AppleALC `alctcsel` property instead.

<h3 id=uefi-audio-setupdelay>UEFI -> Audio -> SetupDelay</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0`

**Description**: Audio codec reconfiguration delay in milliseconds.

Some codecs require a vendor-specific delay after the reconfiguration (e.g. volume setting). This option makes it configurable. A typical delay can be up to 0.5 seconds.

<h2 id=uefi-connectdrivers>UEFI -> ConnectDrivers</h2>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Perform UEFI controller connection after driver loading.

This option is useful for loading drivers following UEFI driver model as they may not start by themselves. Examples of such drivers are filesystem or audio drivers. While effective, this option may not be necessary for drivers performing automatic connection, and may slightly slowdown the boot.

*Note*: Some types of firmware, particularly those made by Apple, only connect the boot drive to speed up the boot process. Enable this option to be able to see all the boot options when running multiple drives.

<h2 id=uefi-drivers>UEFI -> Drivers</h2>

**Type**: `plist array`

**Failsafe**: Empty

**Description**: Load selected drivers from `OC/Drivers` directory.

To be filled with `plist dict` values, describing each driver. Refer to the **Drivers Properties** section below.

<h3 id=uefi-drivers-arguments>UEFI -> Drivers[] -> Arguments</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Some OpenCore plugins accept optional additional arguments which may be specified as a string here.

<h3 id=uefi-drivers-comment>UEFI -> Drivers[] -> Comment</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Arbitrary ASCII string used to provide human readable reference for the entry. Whether this value is used is implementation defined.

<h3 id=uefi-drivers-enabled>UEFI -> Drivers[] -> Enabled</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: If `false` this driver entry will be ignored.

<h3 id=uefi-drivers-loadearly>UEFI -> Drivers[] -> LoadEarly</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Load the driver early in the OpenCore boot process, before NVRAM setup.

*Note*: Do not enable this option unless specifically recommended to do so for a given driver and purpose.

<h3 id=uefi-drivers-path>UEFI -> Drivers[] -> Path</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Path of file to be loaded as a UEFI driver from `OC/Drivers` directory.

<h2 id=uefi-input>UEFI -> Input</h2>

**Type**: `plist dict`

**Description**: Apply individual settings designed for input (keyboard and mouse) in the **Input Properties** section below.

<h3 id=uefi-input-keyfiltering>UEFI -> Input -> KeyFiltering</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Enable keyboard input sanity checking.

Apparently some boards such as the GA Z77P-D3 may return uninitialised data in `EFI_INPUT_KEY` with all input protocols. This option discards keys that are neither ASCII, nor are defined in the UEFI specification (see tables 107 and 108 in version 2.8).

<h3 id=uefi-input-keyforgetthreshold>UEFI -> Input -> KeyForgetThreshold</h3>

**Type**: `plist integer`

**Default**: `5`

**Failsafe**: `0`

**Description**: Treat duplicate key presses as held keys if they arrive during this timeout, in 10 ms units. Only applies to systems using `KeySupport`.

`AppleKeyMapAggregator` protocol is supposed to contain a fixed length buffer of currently pressed keys. However, the majority of the drivers which require `KeySupport` report key presses as interrupts, with automatically generated key repeat behaviour with some defined initial and subsequent delay. As a result, to emulate the raw key behaviour required by several Apple boot systems, we use a timeout to merge multiple repeated keys which are submitted within a small timeout window.

This option allows setting this timeout based on the platform. The recommended value for the majority of platforms is from `5` (`50` milliseconds) to `7` (`70` milliseconds), although values up to `9` (`90` milliseconds) have been observed to be required on some PS/2 systems. For reference, holding a key on VMware will repeat roughly every `20` milliseconds and the equivalent value for APTIO V is `30-40` milliseconds. `KeyForgetThreshold` should be configured to be longer than this. Thus, it is possible to configure a lower `KeyForgetThreshold` value on platforms with a faster native driver key repeat rate, for more responsive input, and it is required to set a higher value on slower platforms.

Pressing keys one after the other results in delays of at least `60` and `100` milliseconds for the same platforms. Ideally, `KeyForgetThreshold` should remain lower than this value, to avoid merging real key presses.

Tuning the value of `KeyForgetThreshold` is necessary for accurate and responsive keyboard input on systems on which `KeySupport` is enabled, and it is recommended to follow the instructions below to tune it correctly for your system.

*Note 1*: To tune `KeyForgetThreshold`, you may use the 'set default' indicator within either OpenCanopy or the builtin picker. If `KeyForgetThreshold` is too low then the 'set default' indicator will continue to flicker while `CTRL` or `=/+` is held down. You should configure the lowest value which avoids this flicker. On some systems (e.g. Aptio IV and potentially other systems using `AMI` `KeySupport` mode) you will be able to find a minimum `KeyForgetThreshold` value at which the 'set default' indicator goes on and stays on with no flicker at all - if so, use this value. On most other systems using `KeySupport`, you will find that the 'set default' indicator will flicker once, when first pressing and holding the `CTRL` or `=/+` key, and then after a further very brief interval will go on and stay on. On such systems, you should chose the lowest value of `KeyForgetThreshold` at which you see only one initial flicker and then no subsequent flickering. (Where this happens, it is an unavoidable artefect on those systems of using `KeySupport` to emulate raw keyboard data, which is not made available by UEFI.)

*Note 2*: `KeyForgetThreshold` should never need to be more than about `9` or `10` at most. If it is set to a value much higher than this, it will result in noticeably unresponsive keyboard input. Therefore, for overall key responsiveness, it is strongly recommended to configure a relatively lower value, at which the 'set default' indicator flickers once and then does not flicker, rather than using a much higher value (i.e. significantly greater than `10`), which you may be able to find but should not use, where the 'set default' indicator does not flicker at all.

<h3 id=uefi-input-keysupport>UEFI -> Input -> KeySupport</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Enable internal keyboard input translation to `AppleKeyMapAggregator` protocol.

This option activates the internal keyboard interceptor driver, based on `AppleGenericInput`, also known as `AptioInputFix`, to fill the `AppleKeyMapAggregator` database for input functioning. In cases where a separate driver such as `OpenUsbKbDxe` is used, this option should never be enabled. Additionally, this option is not required and should not be enabled with Apple firmware.

<h3 id=uefi-input-keysupportmode>UEFI -> Input -> KeySupportMode</h3>

**Type**: `plist string`

**Default**: `Auto`

**Failsafe**: `Auto`

**Description**: Set internal keyboard input translation to `AppleKeyMapAggregator` protocol mode.
* `Auto` --- Performs automatic choice as available with the following preference: `AMI`, `V2`, `V1`.
* `V1` --- Uses UEFI standard legacy input protocol `EFI_SIMPLE_TEXT_INPUT_PROTOCOL`.
* `V2` --- Uses UEFI standard modern input protocol `EFI_SIMPLE_TEXT_INPUT_EX_PROTOCOL`.
* `AMI` --- Uses APTIO input protocol `AMI_EFIKEYCODE_PROTOCOL`. 

*Note*: Currently `V1`, `V2`, and `AMI` unlike `Auto` only do filtering of the particular specified protocol. This may change in the future versions.

<h3 id=uefi-input-keyswap>UEFI -> Input -> KeySwap</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Swap `Command` and `Option` keys during submission.

This option may be useful for keyboard layouts with `Option` key situated to the right of `Command` key.

<h3 id=uefi-input-pointersupport>UEFI -> Input -> PointerSupport</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Enable internal pointer driver.

This option implements standard UEFI pointer protocol (`EFI_SIMPLE_POINTER_PROTOCOL`) through certain OEM protocols. The option may be useful on Z87 ASUS boards, where `EFI_SIMPLE_POINTER_PROTOCOL` is defective.

<h3 id=uefi-input-pointersupportmode>UEFI -> Input -> PointerSupportMode</h3>

**Type**: `plist string`

**Default**: `ASUS`

**Failsafe**: Empty

**Description**: Set OEM protocol used for internal pointer driver.

Currently the only supported variant is `ASUS`, using specialised protocol available on certain Z87 and Z97 ASUS boards. More details can be found in [`LongSoft/UefiTool#116`](https://github.com/LongSoft/UEFITool/pull/116). The value of this property cannot be empty if `PointerSupport` is enabled.

<h3 id=uefi-input-timerresolution>UEFI -> Input -> TimerResolution</h3>

**Type**: `plist integer`

**Default**: `50000`

**Failsafe**: `0`

**Description**: Set architecture timer resolution.

This option allows updating the firmware architecture timer period with the specified value in `100` nanosecond units. Setting a lower value typically improves performance and responsiveness of the interface and input handling.

The recommended value is `50000` (`5` milliseconds) or slightly higher. Select ASUS Z87 boards use `60000` for the interface. Apple boards use `100000`. In case of issues, this option can be left as `0` to not change the timer resolution.

<h2 id=uefi-output>UEFI -> Output</h2>

**Type**: `plist dict`

**Description**: Apply individual settings designed for output (text and graphics) in the **Output Properties** section below.

<h3 id=uefi-output-clearscreenonmodeswitch>UEFI -> Output -> ClearScreenOnModeSwitch</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Some types of firmware only clear part of the screen when switching from graphics to text mode, leaving a fragment of previously drawn images visible. This option fills the entire graphics screen with black colour before switching to text mode.

*Note*: This option only applies to `System` renderer.

<h3 id=uefi-output-consolefont>UEFI -> Output -> ConsoleFont</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty (use OpenCore builtin console font)

**Description**: Specify the console font to use for OpenCore `Builtin` text renderer.

The font file must be located in `EFI/OC/Resources/Font/{font-name\`.hex} and must be 8x16 resolution. Various console fonts can be found online in either `.bdf` or `.hex` format. `.bdf` can be converted to `.hex` format using `gbdfed` (available for Linux or macOS).

There is often no need to change console font, the main use-case being to provide an extended character set for those relatively rare EFI applications which have multi-lingual support (e.g. `memtest86`).

The [OcBinaryData repository](https://github.com/acidanthera/OcBinaryData) includes:
* [Terminus](https://terminus-font.sourceforge.net/) --- A font with extensive character support suitable for applications such as the above.
* TerminusCore --- A lightly modified version of the Terminus font, making some glyphs (`@KMRSTVWimrsw`) more similar to the free ISO Latin font used in XNU and OpenCore. 

`Terminus` and `TerminusCore` are provided under the SIL Open Font License, Version 1.1. Some additional GPL licensed fonts from the EPTO Fonts library, converted to the required `.hex` format, can be found [here](https://github.com/mikebeaton/epto-fonts).

*Note 1*: On many newer systems the `System` text renderer already provides a full set of international characters, in which case this can be used without requiring the `Builtin` renderer and a custom font.

*Note 2*: This option only affects the `Builtin` text renderer and only takes effect from the point at which the `Builtin` renderer is configured. When console output is visible before this point, it is using the system console font.

<h3 id=uefi-output-consolemode>UEFI -> Output -> ConsoleMode</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty (Maintain current console mode)

**Description**: Sets console output mode as specified with the `WxH` (e.g. `80x24`) formatted string.

Set to `Max` to attempt using the largest available console mode.

*Note*: This field is best left empty on most types of firmware.

<h3 id=uefi-output-directgoprendering>UEFI -> Output -> DirectGopRendering</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Use builtin graphics output protocol renderer for console.

On certain firmware, such as on the `MacPro5,1`, this may provide better performance or fix rendering issues. However, this option is not recommended unless there is an obvious benefit as it may result in issues such as slower scrolling.

This renderer fully supports `AppleEg2Info` protocol and will provide screen rotation for all EFI applications. In order to provide seamless rotation compatibility with `EfiBoot`, builtin `AppleFramebufferInfo` should also be used, i.e. it may need to be overridden on Mac EFI.

<h3 id=uefi-output-forceresolution>UEFI -> Output -> ForceResolution</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Forces `Resolution` to be set in cases where the desired resolution is not available by default, such as on legacy Intel GMA and first generation Intel HD Graphics (Ironlake/Arrandale). Setting `Resolution` to `Max` will try to pull the largest available resolution from the connected display's EDID.

*Note*: This option depends on the [`OC_FORCE_RESOLUTION_PROTOCOL`](https://github.com/acidanthera/OpenCorePkg/blob/master/Include/Acidanthera/Protocol/OcForceResolution.h) protocol being present. This protocol is currently only supported by `OpenDuetPkg`. The `OpenDuetPkg` implementation currently only supports Intel iGPUs.

<h3 id=uefi-output-gopburstmode>UEFI -> Output -> GopBurstMode</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Enable write-combining (WC) caching for GOP memory, if system firmware has not already enabled it.

Some older firmware (e.g. EFI-era Macs) fails to set write-combining caching (aka burst mode) for GOP memory, even though the CPU supports it. Setting this can give a considerable speed-up for GOP operations, especially on systems which require `DirectGopRendering`.

*Note 1*: This quirk takes effect whether or not `DirectGopRendering` is set, and in some cases may give a noticeable speed-up to GOP operations even when `DirectGopRendering` is `false`.

*Note 2*: On most systems from circa 2013 onwards, write-combining caching is already applied by the firmware to GOP memory, in which case `GopBurstMode` is unnecessary. On such systems enabling the quirk should normally be harmless, producing an `OCC:` debug log entry indicating that burst mode is already started.

*Note 3*: Some caution should be taken when enabling this quirk, as it has been observed to cause hangs on a few systems. Since additional guards have been added to try to prevent this, please log a bugtracker issue if such a system is found.

<h3 id=uefi-output-goppassthrough>UEFI -> Output -> GopPassThrough</h3>

**Type**: `plist string`

**Default**: `Disabled`

**Failsafe**: `Disabled`

**Description**: Provide GOP protocol instances on top of UGA protocol instances.

This option provides the GOP protocol via a UGA-based proxy for firmware that do not implement the protocol. The supported values for the option are as follows:
* `Enabled` --- provide GOP for all UGA protocols.
* `Apple` --- provide GOP for `AppleFramebufferInfo`-enabled protocols.
* `Disabled` --- do not provide GOP. 

*Note*: This option requires `ProvideConsoleGop` to be enabled.

<h3 id=uefi-output-ignoretextingraphics>UEFI -> Output -> IgnoreTextInGraphics</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Some types of firmware output text onscreen in both graphics and text mode. This is typically unexpected as random text may appear over graphical images and cause UI corruption. Setting this option to `true` will discard all text output if console control is not in `Text` mode.

*Note*: This option only applies to the `System` renderer.

<h3 id=uefi-output-initialmode>UEFI -> Output -> InitialMode</h3>

**Type**: `plist string`

**Default**: `Auto`

**Failsafe**: `Auto`

**Description**: Selects the internal `ConsoleControl` mode in which `TextRenderer` will operate.

Available values are `Auto`, `Text` and `Graphics`. `Text` and `Graphics` specify the named mode. `Auto` uses the current mode of the system `ConsoleControl` protocol when one exists, defaulting to `Text` mode otherwise.UEFI firmware typically supports `ConsoleControl` with two rendering modes: `Graphics` and `Text`. Some types of firmware do not provide a native `ConsoleControl` and rendering modes. OpenCore and macOS expect text to only be shown in `Text` mode but graphics to be drawn in any mode, and this is how the OpenCore `Builtin` renderer behaves. Since this is not required by the UEFI specification, behaviour of the system `ConsoleControl` protocol, when it exists, may vary.

<h3 id=uefi-output-provideconsolegop>UEFI -> Output -> ProvideConsoleGop</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Ensure GOP (Graphics Output Protocol) on console handle.

macOS bootloader requires GOP or UGA (for 10.4 EfiBoot) to be present on console handle, yet the exact location of the graphics protocol is not covered by the UEFI specification. This option will ensure GOP and UGA, if present, are available on the console handle.

*Note*: This option will also replace incompatible implementations of GOP on the console handle, as may be the case on the `MacPro5,1` when using modern GPUs.

<h3 id=uefi-output-reconnectgraphicsonconnect>UEFI -> Output -> ReconnectGraphicsOnConnect</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Reconnect all graphics drivers during driver connection.

On certain firmware, it may be desireable to use an alternative graphics driver, for example BiosVideo.efi, providing better screen resolution options on legacy machines, or a driver supporting `ForceResolution`. This option attempts to disconnect all currently connected graphics drivers before connecting newly loaded drivers.

*Note*: This option requires `ConnectDrivers` to be enabled.

<h3 id=uefi-output-reconnectonreschange>UEFI -> Output -> ReconnectOnResChange</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Reconnect console controllers after changing screen resolution.

On certain firmware, the controllers that produce the console protocols (simple text out) must be reconnected when the screen resolution is changed via GOP. Otherwise, they will not produce text based on the new resolution.

*Note*: On several boards this logic may result in black screen when launching OpenCore from Shell and thus it is optional. In versions prior to 0.5.2 this option was mandatory and not configurable. Please do not use this unless required.

<h3 id=uefi-output-replacetabwithspace>UEFI -> Output -> ReplaceTabWithSpace</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Some types of firmware do not print tab characters or everything that follows them, causing difficulties in using the UEFI Shell's builtin text editor to edit property lists and other documents. This option makes the console output spaces instead of tabs.

*Note*: This option only applies to `System` renderer.

<h3 id=uefi-output-resolution>UEFI -> Output -> Resolution</h3>

**Type**: `plist string`

**Default**: `Max`

**Failsafe**: Empty (Maintain current screen resolution)

**Description**: Sets console output screen resolution.
* Set to `WxH@Bpp` (e.g. `1920x1080@32`) or `WxH` (e.g. `1920x1080`) formatted string to request custom resolution from GOP if available.
* Set to `Max` to attempt using the largest available screen resolution. 

On HiDPI screens `APPLE_VENDOR_VARIABLE_GUID` `UIScale` NVRAM variable may need to be set to `02` to enable HiDPI scaling in `Builtin` text renderer, FileVault 2 UEFI password interface, and boot screen logo. Refer to the **Recommended Variables** section for details.

*Note*: This will fail when console handle has no GOP protocol. When the firmware does not provide it, it can be added with `ProvideConsoleGop` set to `true`.

<h3 id=uefi-output-sanitiseclearscreen>UEFI -> Output -> SanitiseClearScreen</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Some types of firmware reset screen resolutions to a failsafe value (such as `1024x768`) on the attempts to clear screen contents when large display (e.g. 2K or 4K) is used. This option attempts to apply a workaround.

*Note*: This option only applies to the `System` renderer.On all known affected systems, `ConsoleMode` must be set toan empty string for this option to work.

<h3 id=uefi-output-textrenderer>UEFI -> Output -> TextRenderer</h3>

**Type**: `plist string`

**Default**: `BuiltinGraphics`

**Failsafe**: `BuiltinGraphics`

**Description**: Chooses renderer for text going through standard console output.

Currently two renderers are supported: `Builtin` and `System`. The `System` renderer uses firmware services for text rendering, however with additional options provided to sanitize the output. The `Builtin` renderer bypasses firmware services and performs text rendering on its own. Each renderer supports a different set of options. It is recommended to use the `Builtin` renderer, as it supports HiDPI mode and uses full screen resolution.

Each renderer provides its own `ConsoleControl` protocol (in the case of `SystemGeneric` only, this passes some operations through to the system `ConsoleControl` protocol, if one exists).

Valid values of this option are combinations of the renderer to use and the `ConsoleControl` mode to set on the underlying system `ConsoleControl` protocol before starting. To control the initial mode of the provided `ConsoleControl` protocol once started, use the `InitialMode` option.
* `BuiltinGraphics` --- Switch to `Graphics` mode then use `Builtin` renderer with custom `ConsoleControl`.
* `BuiltinText` --- Switch to `Text` mode then use `Builtin` renderer with custom `ConsoleControl`.
* `SystemGraphics` --- Switch to `Graphics` mode then use `System` renderer with custom `ConsoleControl`.
* `SystemText` --- Switch to `Text` mode then use `System` renderer with custom `ConsoleControl`.
* `SystemGeneric` --- Use `System` renderer with custom a `ConsoleControl` protocol which passes its mode set and get operations through to system `ConsoleControl` when it exists. 

The use of `BuiltinGraphics` is straightforward. For most platforms, it is necessary to enable `ProvideConsoleGop` and set `Resolution` to `Max`. The `BuiltinText` variant is an alternative to `BuiltinGraphics` for some very old and defective laptop firmware, which can only draw in `Text` mode.

The use of `System` protocols is more complicated. Typically, the preferred setting is `SystemGraphics` or `SystemText`. Enabling `ProvideConsoleGop`, setting `Resolution` to `Max`, enabling `ReplaceTabWithSpace` is useful on almost all platforms. `SanitiseClearScreen`, `IgnoreTextInGraphics`, and `ClearScreenOnModeSwitch` are more specific, and their use depends on the firmware.

*Note*: Some Macs, such as the `MacPro5,1`, may have incompatible console output when using modern GPUs, and thus only `BuiltinGraphics` may work for them in such cases. NVIDIA GPUs may require additional [firmware upgrades](https://github.com/acidanthera/bugtracker/issues/1280).

<h3 id=uefi-output-uiscale>UEFI -> Output -> UIScale</h3>

**Type**: `plist integer`, 8 bit

**Default**: `0`

**Failsafe**: `-1`

**Description**: User interface scaling factor.

Corresponds to `4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14:UIScale` variable.
* `1` --- 1x scaling, corresponds to normal displays.
* `2` --- 2x scaling, corresponds to HiDPI displays.
* `-1` --- leaves the current variable unchanged.
* `0` --- automatically chooses scaling based on the current resolution. 

*Note 1*: Automatic scale factor detection works on the basis of total pixel area and may fail on small HiDPI displays, in which case the value may be manually managed using the NVRAM section.

*Note 2*: When switching from manually specified NVRAM variable to this preference an NVRAM reset may be needed.

<h3 id=uefi-output-ugapassthrough>UEFI -> Output -> UgaPassThrough</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Provide UGA protocol instances on top of GOP protocol instances.

Some types of firmware do not implement the legacy UGA protocol but this may be required for screen output by older EFI applications such as EfiBoot from 10.4.

<h2 id=uefi-protocoloverrides>UEFI -> ProtocolOverrides</h2>

**Type**: `plist dict`

**Description**: Force builtin versions of certain protocols described in the **ProtocolOverrides Properties** section below.

*Note*: all protocol instances are installed prior to driver loading.

<h3 id=uefi-protocoloverrides-appleaudio>UEFI -> ProtocolOverrides -> AppleAudio</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Replaces Apple audio protocols with builtin versions.

Apple audio protocols allow OpenCore and the macOS bootloader to play sounds and signals for screen reading or audible error reporting. Supported protocols are beep generation and VoiceOver. The VoiceOver protocol is only provided natively by Gibraltar machines (T2), however versions of macOS which support VoiceOver will see and use the implementation provided by OpenCore, on screens such as FileVault 2 unlock. VoiceOver is not supported before macOS High Sierra (10.13). Older macOS versions use the AppleHDA protocol (which is not currently implemented) instead.

Only one set of audio protocols can be available at a time, so this setting should be enabled in order to enable audio playback in the OpenCore user interface on Mac systems implementing some of these protocols.

*Note*: The backend audio driver needs to be configured in `UEFI Audio` section for these protocols to be able to stream audio.

<h3 id=uefi-protocoloverrides-applebootpolicy>UEFI -> ProtocolOverrides -> AppleBootPolicy</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Replaces the Apple Boot Policy protocol with a builtin version. This may be used to ensure APFS compatibility on VMs and legacy Macs.

*Note*: This option is advisable on certain Macs, such as the `MacPro5,1`, that are APFS compatible but on which the Apple Boot Policy protocol has recovery detection issues.

<h3 id=uefi-protocoloverrides-appledebuglog>UEFI -> ProtocolOverrides -> AppleDebugLog</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Replaces the Apple Debug Log protocol with a builtin version.

<h3 id=uefi-protocoloverrides-appleeg2info>UEFI -> ProtocolOverrides -> AppleEg2Info</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Replaces the Apple EFI Graphics 2 protocol with a builtin version.

*Note 1*: This protocol allows newer `EfiBoot` versions (at least 10.15) to expose screen rotation to macOS. Refer to `ForceDisplayRotationInEFI` variable description on how to set screen rotation angle.

*Note 2*: On systems without native support for `ForceDisplayRotationInEFI`, `DirectGopRendering=true` is also required for this setting to have an effect.

<h3 id=uefi-protocoloverrides-appleframebufferinfo>UEFI -> ProtocolOverrides -> AppleFramebufferInfo</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Replaces the Apple Framebuffer Info protocol with a builtin version. This may be used to override framebuffer information on VMs and legacy Macs to improve compatibility with legacy EfiBoot such as the one in macOS 10.4.

*Note*: The current implementation of this property results in it only being active when GOP is available (it is always equivalent to `false` otherwise).

<h3 id=uefi-protocoloverrides-appleimageconversion>UEFI -> ProtocolOverrides -> AppleImageConversion</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Replaces the Apple Image Conversion protocol with a builtin version.

<h3 id=uefi-protocoloverrides-appleimg4verification>UEFI -> ProtocolOverrides -> AppleImg4Verification</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Replaces the Apple IMG4 Verification protocol with a builtin version. This protocol is used to verify `im4m` manifest files used by Apple Secure Boot.

<h3 id=uefi-protocoloverrides-applekeymap>UEFI -> ProtocolOverrides -> AppleKeyMap</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Replaces Apple Key Map protocols with builtin versions.

<h3 id=uefi-protocoloverrides-applertcram>UEFI -> ProtocolOverrides -> AppleRtcRam</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Replaces the Apple RTC RAM protocol with a builtin version.

*Note*: Builtin version of Apple RTC RAM protocol may filter out I/O attempts to certain RTC memory addresses. The list of addresses can be specified in `4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102:rtc-blacklist` variable as a data array.

<h3 id=uefi-protocoloverrides-applesecureboot>UEFI -> ProtocolOverrides -> AppleSecureBoot</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Replaces the Apple Secure Boot protocol with a builtin version.

<h3 id=uefi-protocoloverrides-applesmcio>UEFI -> ProtocolOverrides -> AppleSmcIo</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Replaces the Apple SMC I/O protocol with a builtin version.

This protocol replaces the legacy `VirtualSmc` UEFI driver, and is compatible with any SMC kernel extension. However, in case the `FakeSMC` kernel extension is used, manual NVRAM key variable addition may be needed.

<h3 id=uefi-protocoloverrides-appleuserinterfacetheme>UEFI -> ProtocolOverrides -> AppleUserInterfaceTheme</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Replaces the Apple User Interface Theme protocol with a builtin version.

<h3 id=uefi-protocoloverrides-datahub>UEFI -> ProtocolOverrides -> DataHub</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Replaces the Data Hub protocol with a builtin version.

*Note*: This will discard all previous entries if the protocol was already installed, so all properties required for the safe operation of the system must be specified in the configuration file.

<h3 id=uefi-protocoloverrides-deviceproperties>UEFI -> ProtocolOverrides -> DeviceProperties</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Replaces the Device Property protocol with a builtin version. This may be used to ensure full compatibility on VMs and legacy Macs.

*Note*: This will discard all previous entries if the protocol was already installed, so all properties required for safe operation of the system must be specified in the configuration file.

<h3 id=uefi-protocoloverrides-firmwarevolume>UEFI -> ProtocolOverrides -> FirmwareVolume</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Wraps Firmware Volume protocols, or installs a new version, to support custom cursor images for FileVault 2. Set to `true` to ensure FileVault 2 compatibility on anything other than on VMs and legacy Macs.

*Note*: Several virtual machines, including VMware, may have corrupted cursor images in HiDPI mode and thus, may also require enabling this setting.

<h3 id=uefi-protocoloverrides-hashservices>UEFI -> ProtocolOverrides -> HashServices</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Replaces Hash Services protocols with builtin versions. Set to `true` to ensure FileVault 2 compatibility on platforms with defective SHA-1 hash implementations. This can be determined by an invalid cursor size when `UIScale` is set to `02`. Platforms earlier than APTIO V (Haswell and older) are typically affected.

<h3 id=uefi-protocoloverrides-osinfo>UEFI -> ProtocolOverrides -> OSInfo</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Replaces the OS Info protocol with a builtin version. This protocol is typically used by the firmware and other applications to receive notifications from the macOS bootloader.

<h3 id=uefi-protocoloverrides-pciio>UEFI -> ProtocolOverrides -> PciIo</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Replaces functions in CpuIo and PciRootBridgeIo with 64-bit MMIO compatible ones to fix `Invalid Parameter` when using 4G Decoding. This affects UEFI drivers such as `AudioDxe` which access 64-bit MMIO devices. Platforms earlier than APTIO V (Haswell and older) are typically affected.

<h3 id=uefi-protocoloverrides-unicodecollation>UEFI -> ProtocolOverrides -> UnicodeCollation</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Replaces unicode collation services with builtin versions. Set to `true` to ensure UEFI Shell compatibility on platforms with defective unicode collation implementations. Legacy Insyde and APTIO platforms on Ivy Bridge, and earlier, are typically affected.

<h2 id=uefi-quirks>UEFI -> Quirks</h2>

**Type**: `plist dict`

**Description**: Apply individual firmware quirks described in the **Quirks Properties** section below.

<h3 id=uefi-quirks-activatehpetsupport>UEFI -> Quirks -> ActivateHpetSupport</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Activates HPET support.

Older boards like ICH6 may not always have HPET setting in the firmware preferences, this option tries to force enable it.

<h3 id=uefi-quirks-disablesecuritypolicy>UEFI -> Quirks -> DisableSecurityPolicy</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Disable platform security policy.

*Note*: This setting disables various security features of the firmware, defeating the purpose of any kind of Secure Boot. Do NOT enable if using UEFI Secure Boot.

<h3 id=uefi-quirks-enablevectoracceleration>UEFI -> Quirks -> EnableVectorAcceleration</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Enable AVX vector acceleration of SHA-512 and SHA-384 hashing algorithms.

*Note*: This option may cause issues on certain laptop firmwares, including Lenovo.

<h3 id=uefi-quirks-enablevmx>UEFI -> Quirks -> EnableVmx</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Enable Intel virtual machine extensions.

*Note*: Required to allow virtualization in Windows on some Mac hardware. VMX is enabled or disabled and locked by BIOS before OpenCore starts on most firmware. Use BIOS to enable virtualization where possible.

<h3 id=uefi-quirks-exitbootservicesdelay>UEFI -> Quirks -> ExitBootServicesDelay</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0`

**Description**: Adds delay in microseconds after `EXIT_BOOT_SERVICES` event.

This is a very rough workaround to circumvent the `Still waiting for root device` message on some APTIO IV firmware (ASUS Z87-Pro) particularly when using FileVault 2. It appears that for some reason, they execute code in parallel to `EXIT_BOOT_SERVICES`, which results in the SATA controller being inaccessible from macOS. A better approach is required and Acidanthera is open to suggestions. Expect 3 to 5 seconds to be adequate when this quirk is needed.

<h3 id=uefi-quirks-forceocwriteflash>UEFI -> Quirks -> ForceOcWriteFlash</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Enables writing to flash memory for all OpenCore-managed NVRAM system variables.

*Note*: This value should be disabled on most types of firmware but is left configurable to account for firmware that may have issues with volatile variable storage overflows or similar. Boot issues across multiple OSes can be observed on e.g. Lenovo Thinkpad T430 and T530 without this quirk. Apple variables related to Secure Boot and hibernation are exempt from this for security reasons. Furthermore, some OpenCore variables are exempt for different reasons, such as the boot log due to an available user option, and the TSC frequency due to timing issues. When toggling this option, a NVRAM reset may be required to ensure full functionality.

<h3 id=uefi-quirks-forgeuefisupport>UEFI -> Quirks -> ForgeUefiSupport</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Implement partial UEFI 2.x support on EFI 1.x firmware.

This setting allows running some software written for UEFI 2.x firmware, such as NVIDIA GOP Option ROMs, on hardware with older EFI 1.x firmware (e.g. `MacPro5,1`).

<h3 id=uefi-quirks-ignoreinvalidflexratio>UEFI -> Quirks -> IgnoreInvalidFlexRatio</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Some types of firmware (such as APTIO IV) may contain invalid values in the `MSR_FLEX_RATIO` (`0x194`) MSR register. These values may cause macOS boot failures on Intel platforms.

*Note*: While the option is not expected to harm unaffected firmware, its use is recommended only when specifically required.

<h3 id=uefi-quirks-releaseusbownership>UEFI -> Quirks -> ReleaseUsbOwnership</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Attempt to detach USB controller ownership from the firmware driver. While most types of firmware manage to do this properly, or at least have an option for this, some do not. As a result, the operating system may freeze upon boot. Not recommended unless specifically required.

<h3 id=uefi-quirks-reloadoptionroms>UEFI -> Quirks -> ReloadOptionRoms</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Query PCI devices and reload their Option ROMs if available.

For example, this option allows reloading NVIDIA GOP Option ROM on older Macs after the firmware version is upgraded via `ForgeUefiSupport`.

<h3 id=uefi-quirks-requestbootvarrouting>UEFI -> Quirks -> RequestBootVarRouting</h3>

**Type**: `plist boolean`

**Default**: `true`

**Failsafe**: `false`

**Description**: Request redirect of all `Boot` prefixed variables from `EFI_GLOBAL_VARIABLE_GUID` to`OC_VENDOR_VARIABLE_GUID`.

This quirk requires `OC_FIRMWARE_RUNTIME` protocol implemented in `OpenRuntime.efi`. The quirk lets default boot entry preservation at times when the firmware deletes incompatible boot entries. In summary, this quirk is required to reliably use the [Startup Disk](https://support.apple.com/HT202796) preference pane in firmware that is not compatible with macOS boot entries by design.

By redirecting `Boot` prefixed variables to a separate GUID namespace with the help of `RequestBootVarRouting` quirk we achieve multiple goals:
* Operating systems are jailed and only controlled by OpenCore boot environment to enhance security.
* Operating systems do not mess with OpenCore boot priority, and guarantee fluent updates and hibernation wakes for cases that require reboots with OpenCore in the middle.
* Potentially incompatible boot entries, such as macOS entries, are not deleted or corrupted in any way.

<h3 id=uefi-quirks-resizegpubars>UEFI -> Quirks -> ResizeGpuBars</h3>

**Type**: `plist integer`

**Default**: `-1`

**Failsafe**: `-1`

**Description**: Configure GPU PCI BAR sizes.

This quirk sets GPU PCI BAR sizes as specified or chooses the largest available below the `ResizeGpuBars` value. The specified value follows PCI Resizable BAR spec. Use `0` for 1 MB, `1` for 2 MB, `2` for 4 MB, and so on up to `19` for 512 GB.

Resizable BAR technology allows to ease PCI device programming by mapping a configurable memory region, BAR, into CPU address space (e.g. VRAM to RAM) as opposed to a fixed memory region. This technology is necessary, because one cannot map the largest memory region by default, for the reasons of backwards compatibility with older hardware not supporting 64-bit BARs. Consequentially devices of the last decade use BARs up to 256 MB by default (4 remaining bits are used by other data) but generally allow resizing them to both smaller and larger powers of two (e.g. from 1 MB up to VRAM size).

Operating systems targeting x86 platforms generally do not control PCI address space, letting UEFI firmware decide on the BAR addresses and sizes. This illicit practice resulted in Resizable BAR technology being unused up until 2020 despite being standardised in 2008 and becoming widely available in the hardware soon after.

Modern UEFI firmware allow the use of Resizable BAR technology but generally restrict the configurable options to failsafe default (`OFF`) and maximum available (`ON`). This quirk allows to fine-tune this value for testing and development purposes.

Consider a GPU with 2 BARs:
* `BAR0` supports sizes from 256 MB to 8 GB. Its value is 4 GB.
* `BAR1` supports sizes from 2 MB to 256 MB. Its value is 256 MB. 

*Example 1*: Setting `ResizeGpuBars` to 1 GB will change `BAR0` to 1 GB and leave `BAR1` unchanged. \*Example 2*: Setting `ResizeGpuBars` to 1 MB will change `BAR0` to 256 MB and `BAR0` to 2 MB. \*Example 3*: Setting `ResizeGpuBars` to 16 GB will change `BAR0` to 8 GB and leave `BAR1` unchanged.

*Note 1*: This quirk shall not be used to workaround macOS limitation to address BARs over 1 GB. `ResizeAppleGpuBars` should be used instead.

*Note 2*: While this quirk can increase GPU PCI BAR sizes, this will not work on most firmware as is, because the quirk does not relocate BARs in memory, and they will likely overlap. In most cases it is best to either update the firmware to the latest version or customise it with a specialised driver like [ReBarUEFI](https://github.com/xCuri0/ReBarUEFI).

<h3 id=uefi-quirks-resizeusepcirbio>UEFI -> Quirks -> ResizeUsePciRbIo</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Use PciRootBridgeIo for `ResizeGpuBars` and `ResizeAppleGpuBars`

The quirk makes `ResizeGpuBars` and `ResizeAppleGpuBars` use `PciRootBridgeIo` instead of PciIo. This is needed on systems with a buggy `PciIo` implementation where trying to configure Resizable BAR results in `Capability I/O Error`. Typically this is required on older systems which have been modified with [ReBarUEFI](https://github.com/xCuri0/ReBarUEFI).

<h3 id=uefi-quirks-tscsynctimeout>UEFI -> Quirks -> TscSyncTimeout</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0`

**Description**: Attempts to perform TSC synchronisation with a specified timeout.

The primary purpose of this quirk is to enable early bootstrap TSC synchronisation on some server and laptop models when running a debug XNU kernel. For the debug kernel the TSC needs to be kept in sync across the cores before any kext could kick in rendering all other solutions problematic. The timeout is specified in microseconds and depends on the amount of cores present on the platform, the recommended starting value is `500000`.

This is an experimental quirk, which should only be used for the aforementioned problem. In all other cases, the quirk may render the operating system unstable and is not recommended. The recommended solution in the other cases is to install a kernel extension such as [VoodooTSCSync](https://github.com/RehabMan/VoodooTSCSync), [TSCAdjustReset](https://github.com/interferenc/TSCAdjustReset), or [CpuTscSync](https://github.com/lvs1974/CpuTscSync) (a more specialised variant of VoodooTSCSync for newer laptops).

*Note*: This quirk cannot replace the kernel extension because it cannot operate in ACPI S3 (sleep wake) mode and because the UEFI firmware only provides very limited multicore support which prevents precise updates of the MSR registers.

<h3 id=uefi-quirks-unblockfsconnect>UEFI -> Quirks -> UnblockFsConnect</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: Some types of firmware block partition handles by opening them in `By Driver` mode, resulting in an inability to install File System protocols.

*Note*: This quirk is useful in cases where unsuccessful drive detection results in an absence of boot entries.

<h2 id=uefi-reservedmemory>UEFI -> ReservedMemory</h2>

**Type**: `plist array`

**Failsafe**: Empty

**Description**: To be filled with `plist dict` values, describing memory areas exclusive to specific firmware and hardware functioning, which should not be used by the operating system. Examples of such memory regions could be the second 256 MB corrupted by the Intel HD 3000 or an area with faulty RAM. Refer to the **ReservedMemory Properties** section below for details.

<h3 id=uefi-reservedmemory-address>UEFI -> ReservedMemory[] -> Address</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0`

**Description**: Start address of the reserved memory region, which should be allocated as reserved effectively marking the memory of this type inaccessible to the operating system.

The addresses written here must be part of the memory map, have a `EfiConventionalMemory` type, and be page-aligned (4 KBs).

*Note*: Some types of firmware may not allocate memory areas used by S3 (sleep) and S4 (hibernation) code unless CSM is enabled causing wake failures. After comparing the memory maps with CSM disabled and enabled, these areas can be found in the lower memory and can be fixed up by doing the reservation. Refer to the `Sample.plist` file for details.

<h3 id=uefi-reservedmemory-comment>UEFI -> ReservedMemory[] -> Comment</h3>

**Type**: `plist string`

**Default**: Empty

**Failsafe**: Empty

**Description**: Arbitrary ASCII string used to provide human readable reference for the entry. Whether this value is used is implementation defined.

<h3 id=uefi-reservedmemory-enabled>UEFI -> ReservedMemory[] -> Enabled</h3>

**Type**: `plist boolean`

**Default**: `false`

**Failsafe**: `false`

**Description**: This region will not be reserved unless set to `true`.

<h3 id=uefi-reservedmemory-size>UEFI -> ReservedMemory[] -> Size</h3>

**Type**: `plist integer`

**Default**: `0`

**Failsafe**: `0`

**Description**: Size of the reserved memory region, must be page-aligned (4 KBs).

<h3 id=uefi-reservedmemory-type>UEFI -> ReservedMemory[] -> Type</h3>

**Type**: `plist string`

**Default**: `Reserved`

**Failsafe**: `Reserved`

**Description**: Memory region type matching the UEFI specification memory descriptor types. Mapping:
* `Reserved` --- `EfiReservedMemoryType`
* `LoaderCode` --- `EfiLoaderCode`
* `LoaderData` --- `EfiLoaderData`
* `BootServiceCode` --- `EfiBootServicesCode`
* `BootServiceData` --- `EfiBootServicesData`
* `RuntimeCode` --- `EfiRuntimeServicesCode`
* `RuntimeData` --- `EfiRuntimeServicesData`
* `Available` --- `EfiConventionalMemory`
* `Persistent` --- `EfiPersistentMemory`
* `UnusableMemory` --- `EfiUnusableMemory`
* `ACPIReclaimMemory` --- `EfiACPIReclaimMemory`
* `ACPIMemoryNVS` --- `EfiACPIMemoryNVS`
* `MemoryMappedIO` --- `EfiMemoryMappedIO`
* `MemoryMappedIOPortSpace` --- `EfiMemoryMappedIOPortSpace`
* `PalCode` --- `EfiPalCode`