# tests/findaddress.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from virtualmachine_main import Register16Bits, VirtualMachineMain

vm = VirtualMachineMain(16)

vm.IStore(Register16Bits.DS, 0, 0x2000)
# Calculate address for DS:DX (offset in DX)
addr = vm.FindMemoryAddrInSimulationMem(Register16Bits.DS, 19)
print(addr)