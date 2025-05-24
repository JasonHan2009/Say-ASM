# tests/sysservicetest.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from virtualmachine_main import Register16Bits, VirtualMachineMain

# Test Service 1

"""
vm = VirtualMachineMain(16)
vm.IStore(Register16Bits.AH, 0, 1)
vm.CallSysService()
"""
# Test Service 2

"""
vm = VirtualMachineMain(16)
vm.IStore(Register16Bits.AL, 0, ord("HelloWorld"[0]))
vm.IStore(Register16Bits.AH, 0, 2)
vm.CallSysService()
"""

# Test Service 8

"""
vm = VirtualMachineMain(16)
vm.IStore(Register16Bits.AH, 0, 8)

vm.CallSysService()
"""

# Test Service 9
"""
vm = VirtualMachineMain(16)

test_str = "Hello Qwen!$"  

vm.write_memory(0x11234, test_str.encode('ascii'))

# 设置寄存器值
vm.IStore(Register16Bits.DS, 0, 0x1000) 
vm.IStore(Register16Bits.DX, 0, 0x1234)
vm.IStore(Register16Bits.AH, 0, 0x09)    

vm.CallSysService()  
"""