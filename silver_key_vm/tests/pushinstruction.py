# tests/movinstruction.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from virtualmachine_main import Register16Bits, VirtualMachineMain

vm = VirtualMachineMain(16)
vm.IPush(Register16Bits.AX, 0, 1)

# TEST POP
print(vm.IPop(Register16Bits.AX, 0))