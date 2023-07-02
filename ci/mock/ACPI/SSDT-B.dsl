/*
 * Test SSDT with implicit dependents
 */
DefinitionBlock ("", "SSDT", 2, "SSDTB", "TEST", 0x00000000)
{
	External (_SB_, DeviceObj)                      // SB
  External (__SB.PCI0._FIZ, DeviceObj)            // SB.PCI0.FIZ
  External (SB.BAZ, DeviceObj)                    // SB.BAZ
  

	If (_OSI ("Darwin"))
	{
    Scope(\)
    {
      Scope (SB.PCI0.FIZ)
      {
        Device (^^BAR) {                          // SB.BAR
          // ...
        }
      }
      Name(FUUB, One)                             // FUUB
      Device (\_SB.FOO)                           // SB.FOO
      {
        Name (XUUQ, Buffer (0x02) { 0x01, 0xFF }) // SB.FOO.XUUQ
      }
      Name(BUUF, Zero)                            // BUUF
      Name(BUUX, Zero)                            // BUUX
    }
	}
}