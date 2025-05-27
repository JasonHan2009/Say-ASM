# tests/fileoperand.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from virtualmachine_main import Register16Bits, VirtualMachineMain

vm = VirtualMachineMain(16)

"""
# 准备测试文件名 (地址: DS=0x1000, DX=0x2000)
test_filename = "TESTFILE.TXT\x00"  # DOS格式文件名
vm.write_memory((0x1000 << 4) + 0x2000, test_filename.encode('ascii'))  # 添加括号

# 设置寄存器值
vm.IStore(Register16Bits.DS, 0, 0x1000)
vm.IStore(Register16Bits.DX, 0, 0x2000)
vm.IStore(Register16Bits.AL, 0, 1)  # 只读模式
vm.IStore(Register16Bits.AH, 0, 0x3D)

# 执行系统调用
vm.CallSysService()
print(f"File handle: {vm.registers[Register16Bits.AX][0]}")  # 输出分配的文件句柄

# 打开文件
vm.IStore(Register16Bits.DS, 0, 0x1000)
vm.IStore(Register16Bits.DX, 0, 0x2000)
vm.IStore(Register16Bits.AL, 0, 0)
vm.IStore(Register16Bits.AH, 0, 0x3D)
vm.CallSysService()
handle = vm.registers[Register16Bits.AX][0]

# 设置读取参数
vm.IStore(Register16Bits.BX, 0, handle)
vm.IStore(Register16Bits.CX, 0, 12)  # 读取12字节
vm.IStore(Register16Bits.DS, 0, 0x3000)
vm.IStore(Register16Bits.DX, 0, 0x4000)  # 缓冲区地址 0x3000<<4 + 0x4000 = 0x34000
vm.IStore(Register16Bits.AH, 0, 0x3F)

# 执行读取
vm.CallSysService()
bytes_read = vm.registers[Register16Bits.AX][0]
print(f"Read {bytes_read} bytes")  # 应输出12

# 提取内存数据
buffer_data = bytes(vm.memory[0x34000:0x34000+bytes_read]).decode('ascii')
print(buffer_data)  
""" # Read

"""
# 测试文件写入流程

# 准备测试文件名 (地址: DS=0x1000, DX=0x2000)
test_filename = "TESTFILE.TXT\x00"  # DOS格式文件名
vm.write_memory((0x1000 << 4) + 0x2000, test_filename.encode('ascii'))  # 添加括号

# 设置寄存器值
vm.IStore(Register16Bits.DS, 0, 0x1000)
vm.IStore(Register16Bits.DX, 0, 0x2000)
vm.IStore(Register16Bits.AL, 0, 1)  # 只读模式
vm.IStore(Register16Bits.AH, 0, 0x3D)

# 执行系统调用
vm.CallSysService()
print(f"File handle: {vm.registers[Register16Bits.AX][0]}")  # 输出分配的文件句柄

# 打开文件
vm.IStore(Register16Bits.DS, 0, 0x1000)
vm.IStore(Register16Bits.DX, 0, 0x2000)
vm.IStore(Register16Bits.AL, 0, 0)
vm.IStore(Register16Bits.AH, 0, 0x3D)
vm.CallSysService()
handle = vm.registers[Register16Bits.AX][0]
# 准备测试数据
test_data = b"Hello World!"
vm.write_memory((0x3000 << 4) + 0x4000, test_data)  # 写入内存缓冲区

# 打开文件（写模式）
vm.IStore(Register16Bits.DS, 0, 0x1000)
vm.IStore(Register16Bits.DX, 0, 0x2000)
vm.IStore(Register16Bits.AL, 0, 1)  # 写模式
vm.IStore(Register16Bits.AH, 0, 0x3D)
vm.CallSysService()
handle = vm.registers[Register16Bits.AX][0]

# 设置写入参数
vm.IStore(Register16Bits.BX, 0, handle)
vm.IStore(Register16Bits.CX, 0, len(test_data))  # 写入字节数
vm.IStore(Register16Bits.DS, 0, 0x3000)
vm.IStore(Register16Bits.DX, 0, 0x4000)  # 缓冲区地址
vm.IStore(Register16Bits.AH, 0, 0x40)

# 执行写入
vm.CallSysService()
print(f"Wrote {vm.registers[Register16Bits.AX][0]} bytes")

# 关闭文件
vm.IStore(Register16Bits.BX, 0, handle)
vm.IStore(Register16Bits.AH, 0, 0x3E)
vm.CallSysService()
"""