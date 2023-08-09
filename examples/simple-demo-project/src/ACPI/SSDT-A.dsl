/*
 * Test SSDT with implicit dependencies on SSDT-B
 */
DefinitionBlock ("", "SSDT", 2, "SSDTA", "TEST", 0x00000000)
{
  External (_SB_, DeviceObj)                      // SB
  External (__SB.PCI0, DeviceObj)                 // SB.PCI0


  Name (\QUX, One)                                // QUX

	If (_OSI ("Darwin"))
	{
		QUX = 0x02

    Scope(\)
    {
      Scope (__SB.PCI0)
      {
        Device (^BAZ) {                           // SB.BAZ
          Name (_HID, EisaId ("BAZ0000"))
        }
        Name (QUUX, Buffer (0x02) { 0x01, 0xFF }) // SB.PCI0.QUUX
      }
    }
	}
}
