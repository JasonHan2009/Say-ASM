# tests/processoperand.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from virtualmachine_main import Register16Bits, VirtualMachineMain
vm = VirtualMachineMain(16)

"""
vm.IStore(Register16Bits.AX, 0, 0x4c00)
vm.IStore(Register16Bits.AH, 0, 0x4c)
vm.CallSysService()
"""
"""
vm.IStore(Register16Bits.AL, 0, 1)
vm.IStore(Register16Bits.DX, 0, 0x0001)
vm.IStore(Register16Bits.AH, 0, 0x31)
vm.CallSysService()
"""