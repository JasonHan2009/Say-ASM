# tests/movinstruction.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from virtualmachine_main import Register16Bits, VirtualMachineMain

vm = VirtualMachineMain(16)
vm.IStore(Register16Bits.AX, 0, 0x1234)
print(vm.registers[Register16Bits.AX][0])

# Test Invalid Range
vm.IStore(Register16Bits.AX, 0, 0xFFFFFF)
print(vm.registers[Register16Bits.AX][0])

vm.IStore(Register16Bits.AX, 0xFF, 0xFFFFFF)
print(vm.registers[Register16Bits.AX][0xFF])