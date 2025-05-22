# tests/sysservicetest.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from virtualmachine_main import Register16Bits, VirtualMachineMain

vm = VirtualMachineMain(16)
vm.IStore(Register16Bits.AH, 0, 1)
vm.CallSysService()