import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from virtualmachine_main import Register16Bits, VirtualMachineMain
vm = VirtualMachineMain(16)

# Test Interrupt Vector Handling (AH=25h/35h)
def test_interrupt_vectors():
    # Set interrupt 0x21 handler to 1000:2000
    vm.registers[Register16Bits.AH][0] = 0x25
    vm.registers[Register16Bits.AL][0] = 0x21  # INT number
    vm.registers[Register16Bits.DS][0] = 0x1000 # Segment
    vm.registers[Register16Bits.DX][0] = 0x2000 # Offset
    vm.CallSysService()
    print(f"Set INT21h vector to {vm.interrupt_vectors[0x21]}")

    # Get interrupt 0x21 vector
    vm.registers[Register16Bits.AH][0] = 0x35
    vm.registers[Register16Bits.AL][0] = 0x21
    vm.CallSysService()
    print(f"Got INT21h vector: ES:BX = "
          f"{vm.registers[Register16Bits.ES][0]:04X}:"
          f"{vm.registers[Register16Bits.BX][0]:04X}")

# Test System Date/Time Services
def test_system_datetime():
    # Get system date (AH=2Ah)
    vm.registers[Register16Bits.AH][0] = 0x2A
    vm.CallSysService()
    print(f"System Date: {vm.registers[Register16Bits.CX][0]}-"
          f"{vm.registers[Register16Bits.DH][0]:02d}-"
          f"{vm.registers[Register16Bits.DL][0]:02d}")

    # Get system time (AH=2Ch)
    vm.registers[Register16Bits.AH][0] = 0x2C
    vm.CallSysService()
    print(f"System Time: {vm.registers[Register16Bits.CH][0]:02d}:"
          f"{vm.registers[Register16Bits.CL][0]:02d}:"
          f"{vm.registers[Register16Bits.DH][0]:02d}.{vm.registers[Register16Bits.DL][0]:02d}")

# Run tests
if __name__ == "__main__":
    test_interrupt_vectors()
    test_system_datetime()