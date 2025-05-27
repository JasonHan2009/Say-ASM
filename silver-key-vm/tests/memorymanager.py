# tests/memorymanager.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from virtualmachine_main import Register16Bits, VirtualMachineMain
"""

# 测试内存管理
vm = VirtualMachineMain(16)

# 请求分配1个段落(16字节)
vm.IStore(Register16Bits.BX, 0, 0x0001)
vm.IStore(Register16Bits.AH, 0, 0x48)
vm.CallSysService()
print(f"Allocated segment: 0x{vm.registers[Register16Bits.AX][0]:04X}")  # 应输出0x1000

# 请求分配过大内存
vm.IStore(Register16Bits.BX, 0, 0x1001)  # 请求4KB+1段落
vm.CallSysService()
print(f"Error code: 0x{vm.registers[Register16Bits.AX][0]:04X}")  # 应输出0x0008

# 测试内存释放
vm.IStore(Register16Bits.AH, 0, 0x49)
print(f"Memory released: 0x{vm.registers[Register16Bits.AX][0]:04X}")  # 应输出0x0000
"""

