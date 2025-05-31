from enum import Enum
from silver_key_vm.SAYYASMCONST import *
from silver_key_vm.IDERender import Popup, RenderModule
import sys

##########
# VirtualMachine
# Dev JasonHan2009
# IDEASPHERE
############
class Register16Bits(Enum):
    AX = "AX"
    BX = "BX"
    AH = "AH"
    CX = "CX"
    DX = "DX"
    SP = "SP"
    BP = "BP"
    AL = "AL"
    SI = "SI"
    DL = "DL"
    CF = "CF"
    CS = "CS"
    DS = "DS"
    DH = 'DH'
    SS = "SS"
    CL = 'CL'
    CH = 'CH'
    ES = "ES"
    IP = "IP"

class VirtualMachineMain:
    def __init__(self, platform):
        self.flag = False

        match platform:
            case 16:
                self.flag = False
                self.registers = {reg: [0] * VM_REGISTER_SIZE for reg in Register16Bits}
                self.stack_16 = [0] * VM_MEM_SIZE
                self.platform = platform
                self.memory = bytearray(1024 * 1024)  # 1MB Physics Memory
                current_os = platform
                self.interrupt_vectors = {}
                # 初始化文件句柄表
                self.file_handles = {
                    0: sys.stdin,
                    1: sys.stdout,
                    2: sys.stderr,
                    3: self._get_console_input(current_os),
                    4: self._get_console_output(current_os)
                }

                self.memory_blocks = {
                    'free': [(0x1000, 0xEFFF)],  # 初始可用内存块 (段地址0x1000-0xFFFF)
                    'used': [],
                    'resident': [] 
                }
                self.memory_base = 0x1000 << 4  # 可用内存起始地址(0x10000)
                self.memory_size = 0xF0000       # 可用内存大小(960KB)

                if sys.platform == 'windows':
                    self.file_handles.update({
                        3: open('CON', 'r'),
                        4: open('CON', 'w')
                    })
                else:  # Linux/macOS使用标准IO
                    self.file_handles.update({
                        3: sys.stdin,   # 复用标准输入
                        4: sys.stdout   # 复用标准输出
                    })
                
                self.next_handle = 5
            case _:
                self.flag = True
                
    def write_memory(self, address: int, data: bytes):
        """Write Binary Into Simulation Memory"""
        for offset, byte in enumerate(data):
            if address + offset >= len(self.memory):
                RenderModule(
                    "POTENTIAL",
                    "white",
                    f"You Are Trying To Write Into Memory 0x{address + offset:X} Out Of Range"    
                ).render()
            self.memory[address + offset] = byte

    def IStore(self, reg: Register16Bits, index: int, value: int):
        """
        Store value into register[index]
        """
        if self.platform == 16:
            if index < 0 or index >= VM_REGISTER_SIZE:
                RenderModule(
                    "POTENTIAL",
                    "white",
                    f"Register index {index} out of range"
                ).render()
            if not (0 <= value <= 0xFFFF):
                RenderModule(
                    "POTENTIAL",
                    "white",
                    f"Value {value} exceeds 16-bit range"
                ).render()                
            self.registers[reg][index] = value
    
    def IPush(self, reg: Register16Bits, index: int, value: int):
        """
        Push value into stack[index]
        """
        if self.platform == 16:
            if index < 0 or index >= VM_MEM_SIZE:
                RenderModule(
                    "POTENTIAL",
                    "white",
                    f"Stack index {index} out of range"
                ).render()
            if not (0 <= value <= 0xFFFF):
                RenderModule(
                    "POTENTIAL",
                    "white",
                    f"Value {value} exceeds 16-bit range"
                ).render()
            self.stack_16[index] = value
    
    def IPop(self, reg: Register16Bits, index: int):
        """
        Pop value from stack[index]
        """
        if self.platform == 16:
            if index < 0 or index >= VM_MEM_SIZE:
                RenderModule(
                    "POTENTIAL",
                    "white",
                    f"Stack index {index} out of range"
                ).render()
            return self.stack_16[index]
    
    def IReset(self, reg : Register16Bits, index: int):
        """
        Reset value to stack[index]
        """
        if self.platform == 16:
            if index < 0 or index >= VM_MEM_SIZE:
                RenderModule(
                    "POTENTIAL",
                    "white",
                    f"Stack index {index} out of range"
                ).render()
            
            self.stack_16[index] = 0

    def CallSysService(self):
        """
        Call the system service
        Its not simulate in array, its directly write into mem
        """
        if self.platform == 16: 
            AHVAL = self.registers[Register16Bits.AH][0]
            match AHVAL:

                # IO(Console)
                case 0x01:  # KeyBoard Input(With Echo)
                    char : str = input("")[0]
                    # Get Single Character And Print Its ASCII Value
                    # First, Store Into AL Reg Then Print And Next Reset To 0
                    self.IPush(Register16Bits.AL, 0, ord(char))
                    # If AL Register Has Value, OutPut it To Console
                    if self.IPop(Register16Bits.AL, 0) != 0:
                        print(self.IPop(Register16Bits.AL, 0))
                    else:
                        self.IReset(Register16Bits.AL, 0)
                        RenderModule(
                            "POTENTIAL",
                            "white",
                            "It May Caused Segement Fault Or Other Questions In Real Env, Please Check Your Code"
                        ).render()
                        
                case 0x02:
                    DLVAL = self.registers[Register16Bits.DL][0]
                    if 0 <= DLVAL <= 0xFF:
                        print(chr(DLVAL), end='', flush=True) 
                    else:
                        RenderModule(
                            "EXCEPTION",
                            "white",
                            f"Invalid ASCII value in DL: 0x{DLVAL:X}"
                        ).render()
                          
                case 0x08: # KeyBoard Input Without Echo
                    char : str = input("")[0]
                    # Get Single Character With Out Echo
                    if self.IPop(Register16Bits.AL, 0) != 0:
                        self.IPush(Register16Bits.AL, 0, ord(char))
                    else:
                        # Find The Next Dict Postion, Then Stored It
                        i = 0
                        next_object = self.IPop(Register16Bits.AL, i+1)
                        if next_object == 0:
                            self.IPush(Register16Bits.AL, i+1, ord(char))
                case 0x09:
                    try:
                        # 计算线性地址 = DS << 4 + DX
                        ds = self.registers[Register16Bits.DS][0]
                        dx = self.registers[Register16Bits.DX][0]
                        linear_addr = (ds << 4) + dx

                        # 读取$结尾的字符串
                        output = []
                        while True:
                            char = self.memory[linear_addr]
                            linear_addr += 1
                            if char == 0x24:  # 遇到$符号
                                break
                            output.append(char)
                            if linear_addr >= len(self.memory):
                                RenderModule(
                                    "POTENTIAL",
                                    "white",
                                    f"String exceeds memory bounds"
                                ).render()
                          
                        # 转换并输出字符串
                        decoded_str = bytes(output).decode('ascii', errors='replace')
                        print(decoded_str, end='')
                        
                    except IndexError as e:
                        RenderModule(
                            "POTENTIAL",
                            "white",
                            f"Memory access error: {str(e)}"
                        ).render()
                
                # File Operand
                # Dev Jason
                case 0x3D:  # 打开文件
                    try:
                        # 获取访问模式 (AL寄存器)
                        access_code = self.registers[Register16Bits.AL][0]
                        
                        # 计算文件名地址 DS:DX -> 线性地址
                        ds = self.registers[Register16Bits.DS][0]
                        dx = self.registers[Register16Bits.DX][0]
                        filename_addr = (ds << 4) + dx
                        
                        # 读取以NULL结尾的DOS文件名
                        filename_bytes = []
                        while True:
                            char = self.memory[filename_addr]
                            filename_addr += 1
                            if char == 0x00:  # NULL终止符
                                break
                            filename_bytes.append(char)
                            if filename_addr >= len(self.memory):
                                RenderModule(
                                    "POTENTIAL",
                                    "white",
                                    f"Filename exceeds memory bounds"
                                ).render()
                                
                        # 转换DOS 8.3格式文件名
                        dos_name = bytes(filename_bytes).decode('ascii', errors='replace')
                        modern_name = self._convert_dos_filename(dos_name)
                        
                        # 映射访问模式
                        mode_mapping = {
                            0: 'rb',  # 只读
                            1: 'wb',  # 只写
                            2: 'r+b'  # 读/写
                        }
                        if access_code not in mode_mapping:
                            RenderModule(
                                "POTENTIAL",
                                "white",
                                f"Invalid access code: {access_code}"
                            ).render()              
                        # 打开文件并分配句柄
                        try:
                            file_obj = open(modern_name, mode_mapping[access_code])
                            handle = self.next_handle
                            self.file_handles[handle] = file_obj
                            self.next_handle += 1
                            
                            # 成功返回句柄到AX
                            self.registers[Register16Bits.AX][0] = handle
                            
                        except IOError as e:
                            # 失败设置错误码 (DOS错误码2=文件未找到)
                            self.registers[Register16Bits.AX][0] = 0x0002
                            RenderModule(
                                "SUGGESTION",
                                "white",
                                f"May File Its Not On Your PC: {str(e)}"
                            ).render()

                    except IndexError as e:
                        RenderModule(
                            "POTENTIAL",
                            "white",
                            f"Memory access error: {str(e)}"
                        ).render()
                case 0x3e:  # 关闭文件
                    try:
                        handle = self.registers[Register16Bits.BX][0]
                        
                        # 检查预定义句柄(0-4)是否允许关闭
                        if handle < 5:
                            RenderModule(
                                "SUGGESTION",
                                "white",
                                "Cannot close standard handles"
                            ).render()
                        if handle in self.file_handles:
                            # 执行关闭操作
                            self.file_handles[handle].close()
                            del self.file_handles[handle]
                            
                            # 成功状态：CF=0 (通过AX最高位表示)
                            self.registers[Register16Bits.AX][0] = 0x0000
                        else:
                            # 失败状态：CF=1 + 错误码06h (无效句柄)
                            self.registers[Register16Bits.AX][0] = 0x0006 | 0x8000  # 最高位1表示错误
                            RenderModule(
                                "EXCEPTION",
                                "white",
                                f"Invalid file handle: {handle}"
                            ).render()

                    except PermissionError as pe:
                        # DOS不允许关闭标准设备
                        self.registers[Register16Bits.AX][0] = 0x0001 | 0x8000  # 错误码01h
                        RenderModule(
                                "EXCEPTION",
                                "white",
                                f"Invalid file handle: {str(pe)}"
                        ).render()
                    except Exception as e:  
                        self.registers[Register16Bits.AX][0] = 0x0006 | 0x8000  # 错误码06h
                        RenderModule(
                                "EXCEPTION",
                                "white",
                                f"May File Its Not On Your PC {str(e)}"
                        ).render()
                case 0x3F:  # 读取文件
                    try:
                        # 获取参数
                        handle = self.registers[Register16Bits.BX][0]
                        bytes_to_read = self.registers[Register16Bits.CX][0]
                        buffer_addr = (self.registers[Register16Bits.DS][0] << 4) + self.registers[Register16Bits.DX][0]

                        # 参数验证
                        if bytes_to_read > 65535:
                            RenderModule(
                                "EXCEPTION",
                                "white",
                                "CX value exceeds 16-bit range"
                            ).render()
                        if buffer_addr + bytes_to_read > len(self.memory):
                            RenderModule(
                                "EXCEPTION",
                                "white",
                                "Buffer address exceeds memory range"
                            ).render()
                        # 检查文件句柄有效性
                        if handle not in self.file_handles:
                            self.registers[Register16Bits.AX][0] = 0x0006 | 0x8000  # 无效句柄
                            RenderModule(
                                "EXCEPTION",
                                "white",
                                f"Invalid file handle: {handle}"
                            ).render()

                        # 执行读取操作
                        file_obj = self.file_handles[handle]
                        data = file_obj.read(bytes_to_read)

                        
                        # 写入内存缓冲区
                        for i, byte in enumerate(data):
                            self.memory[buffer_addr + i] = byte
                            
                        # 设置返回结果
                        self.registers[Register16Bits.AX][0] = len(data)  # 实际读取字节数
                        
                        # 清除错误标志
                        if len(data) == bytes_to_read:
                            self.registers[Register16Bits.CF][0] = 0  # 成功完成
                        else:
                            self.registers[Register16Bits.CF][0] = 1  # 部分读取

                    except ValueError as ve:
                        self.registers[Register16Bits.AX][0] = 0x0001 | 0x8000  # 无效参数
                        RenderModule(
                                "EXCEPTION",
                                "white",
                                f"Invalid argument: {str(ve)}"
                        ).render()
                    except IndexError as ie:
                        self.registers[Register16Bits.AX][0] = 0x0005 | 0x8000  # 内存越界
                        RenderModule(
                                "EXCEPTION",
                                "white",
                                f"Memory access error: {str(ie)}"
                        ).render()
                    except Exception as e:
                        self.registers[Register16Bits.AX][0] = 0x0006 | 0x8000  # 通用错误
                        RenderModule(
                                "EXCEPTION",
                                "white",
                                f"[SILVERKEY VM][DEEP WARN] File read error: {str(e)}"
                        ).render()
                case 0x40: # Write File Service In Dos
                    try:
                        # Get Args
                        handle = self.registers[Register16Bits.BX][0]
                        bytes_to_write = self.registers[Register16Bits.CX][0]
                        buffer_addr = (self.registers[Register16Bits.DS][0] << 4) + self.registers[Register16Bits.DX][0]
                          # 参数验证
                        if bytes_to_write > 65535:
                            RenderModule(
                                "EXCEPTION",
                                "white",
                                "CX value exceeds 16-bit range"
                            ).render()
                        if buffer_addr + bytes_to_write > len(self.memory):
                            RenderModule(
                                "EXCEPTION",
                                "white",
                                "Buffer address exceeds memory range"
                            ).render()
                            
                        # 检查文件句柄有效性
                        if handle not in self.file_handles:
                            self.registers[Register16Bits.AX][0] = 0x0006 | 0x8000 # 无效句柄
                            RenderModule(
                                "EXCEPTION",
                                "white",
                                f"Invalid file handle: {handle}"
                            ).render()
                            

                        # 从内存读取要写入的数据
                        data_to_write = bytes(self.memory[buffer_addr : buffer_addr + bytes_to_write])
                        
                        # 执行写入操作
                        file_obj = self.file_handles[handle]
                        written_bytes = file_obj.write(data_to_write)
                        
                        # 设置返回结果
                        self.registers[Register16Bits.AX][0] = written_bytes
                        
                        # 设置状态标志
                        self.registers[Register16Bits.CF][0] = 0 if written_bytes == bytes_to_write else 1

                    except ValueError as ve:
                        self.registers[Register16Bits.AX][0] = 0x0001 | 0x8000
                        RenderModule(
                                "EXCEPTION",
                                "white",
                                f"Invalid argument: {str(ve)}"
                        ).render()
                    except IOError as ie:
                        self.registers[Register16Bits.AX][0] = 0x0005 | 0x8000
                        RenderModule(
                                "EXCEPTION",
                                "white",
                                f"Write failed: {str(ie)}"
                        ).render()
                    except Exception as e:
                        self.registers[Register16Bits.AX][0] = 0x0006 | 0x8000
                        RenderModule(
                                "EXCEPTION",
                                "white",
                                f"File write error: {str(e)}"
                        ).render()
                    
                 # MemoryManager
                case 0x48:  # 分配内存
                    free_blocks = [
                        (start, end) for (start, end) in self.memory_blocks['free'] 
                        if not self._is_reserved_block(start, end)
                    ]

                    def _is_reserved_block(self, start_seg, end_seg):
                        block_start = start_seg << 4
                        block_end = (end_seg + 1) << 4 - 1
                        for (res_start, res_end) in self.memory_blocks['resident']:
                            if not (block_end < res_start or block_start > res_end):
                                return True
                        return False
                    try:
                        # 获取请求的段落数 (1 paragraph = 16 bytes)
                        paragraphs = self.registers[Register16Bits.BX][0]
                        bytes_needed = paragraphs << 4

                        # 参数验证
                        if paragraphs == 0 or paragraphs > 0x1000:  # 最大4KB段落
                            RenderModule(
                                "EXCEPTION",
                                "white",
                                "Invalid paragraph count"
                            ).render()

                        # 寻找足够大的空闲块
                        allocated_segment = None
                        for i, (start_seg, end_seg) in enumerate(self.memory_blocks['free']):
                            block_size = (end_seg - start_seg + 1) << 4
                            if block_size >= bytes_needed:
                                # 分配内存
                                allocated_segment = start_seg
                                
                                # 更新空闲列表
                                remaining = (end_seg - start_seg) - (paragraphs - 1)
                                if remaining > 0:
                                    self.memory_blocks['free'][i] = (
                                        start_seg + paragraphs, 
                                        end_seg
                                    )
                                else:
                                    del self.memory_blocks['free'][i]
                                
                                # 记录已分配块
                                self.memory_blocks['used'].append(
                                    (allocated_segment, allocated_segment + paragraphs - 1)
                                )
                                break

                        if allocated_segment is None:
                            # 内存不足
                            self.registers[Register16Bits.CF][0] = 1
                            self.registers[Register16Bits.AX][0] = 0x0008  # DOS错误码08h
                            RenderModule(
                                "EXCEPTION",
                                "white",
                                f"Insufficient memory"
                            ).render()

                        # 设置返回参数
                        self.registers[Register16Bits.CF][0] = 0
                        self.registers[Register16Bits.AX][0] = allocated_segment

                    except ValueError as ve:
                        self.registers[Register16Bits.CF][0] = 1
                        self.registers[Register16Bits.AX][0] = 0x0007  # 内存控制块损坏
                        RenderModule(
                                "EXCEPTION",
                                "white",
                                f"Mem Block Broken!"
                        ).render()
                    except MemoryError as me:
                        self.registers[Register16Bits.CF][0] = 1
                        self.registers[Register16Bits.AX][0] = 0x0008  # 内存不足
                        RenderModule(
                                "EXCEPTION",
                                "white",
                                f"It May Cause Memory Not Enough"
                        ).render()
                case 0x49: # Release Memory
                    try:    
                        # 获取要释放的内存段落
                        segment = self.registers[Register16Bits.BX][0]
                        
                        # 参数验证
                        if segment == 0 or segment > 0xFFFF:
                            RenderModule(
                                    "EXCEPTION",
                                    "white",
                                    f"Invalid segment value"
                            ).render()
                        
                        # 寻找要释放的内存段落
                        for i,(start_seg, end_seg) in enumerate(self.memory_blocks['used']):
                            if start_seg <= segment <= end_seg:
                                # 释放内存
                                self.memory_blocks['used'].pop(i)
                                
                                # 添加到空闲列表
                                self.memory_blocks['free'].append((start_seg, end_seg))
                                break
                            else:
                                RenderModule(
                                        "EXCEPTION",
                                        "white",
                                        f"Segment not found"
                                ).render()
                    except ValueError as ve:
                        self.registers[Register16Bits.CF][0] = 1
                        self.registers[Register16Bits.AX][0] = 0x0007  # 内存控制块损坏
                        RenderModule(
                                "EXCEPTION",
                                "white",
                                f"Mem Block Broken!"
                        ).render()

                # Process Manager
                case 0x4c: # Exit Program
                    # Get The Exit Code 
                    exit_code = self.registers[Register16Bits.AX][0]  
                    # Check the value valid
                    if exit_code > 0x4c00:
                        RenderModule(
                            "EXCEPTION",
                            "white",
                            f"Invalid Exit Code"
                        ).render()
                    
                    if exit_code == 0x4c00:
                        self.registers[Register16Bits.AH][0] = 0x4c
                        self.registers[Register16Bits.AL][0] = 0x00
                    elif exit_code == 0x4c01:
                        self.registers[Register16Bits.AH][0] = 0x4c
                        self.registers[Register16Bits.AL][0] = 0x01
                case 0x31: # TSR (Terminate and Stay Resident)
                    try:
                        # 获取参数 (AL=返回码, DX=驻留内存段落数)
                        return_code = self.registers[Register16Bits.AL][0]
                        paragraphs = self.registers[Register16Bits.DX][0]

                        # 参数验证
                        if paragraphs == 0 or paragraphs > 0xFFF:  # 最大支持0xFFF段落(约64KB)
                            RenderModule(
                                "EXCEPTION",
                                "white",
                                f"Invalid paragraph count: {paragraphs}"
                        ).render()

                        # 计算驻留内存大小 (paragraphs * 16 bytes)
                        resident_size = paragraphs << 4  # 转换为字节数

                        # 获取当前程序内存范围 (假设从CS:0000到当前内存尾)
                        cs = self.registers[Register16Bits.CS][0]
                        start_addr = cs << 4
                        end_addr = start_addr + resident_size - 1

                        # 验证内存范围
                        if end_addr >= len(self.memory):
                            RenderModule(
                                "EXCEPTION",
                                "white",
                                f"Resident size exceeds memory limit"
                            ).render()

                        # 标记为驻留内存 (防止被后续分配)
                        self.memory_blocks['resident'] = self.memory_blocks.get('resident', [])
                        self.memory_blocks['resident'].append( (start_addr, end_addr) )

                        # 设置返回参数 (CF=0表示成功)
                        self.registers[Register16Bits.CF][0] = 0
                        
                        # 终止程序执行 (需要上层添加程序状态控制)
                        self.program_terminated = True
                        self.exit_code = return_code

                    except (ValueError, IndexError) as e:
                        self.registers[Register16Bits.CF][0] = 1  # 失败标志
                        self.registers[Register16Bits.AX][0] = 0x0007  # 错误码: 内存控制块损坏
                        RenderModule(
                            "EXCEPTION",
                            "white",
                            f"TSR failed: {str(e)}"
                        ).render()
                case 0x25:  # Set Interrupt Vector (AH=25h)
                    try:
                        # AL = interrupt number
                        # DS:DX = address of interrupt handler
                        int_num = self.registers[Register16Bits.AL][0]
                        ds = self.registers[Register16Bits.DS][0]
                        dx = self.registers[Register16Bits.DX][0]
                        
                        # Store in interrupt vector table (segment:offset format)
                        self.interrupt_vectors[int_num] = (ds, dx)
                        
                        # Clear carry flag for success
                        self.registers[Register16Bits.CF][0] = 0
                        
                    except Exception as e:
                        self.registers[Register16Bits.CF][0] = 1
                        RenderModule(
                            "EXCEPTION",
                            "white",
                            f"Int Vector Set Failed: {str(e)}"
                        ).render()

                case 0x35:  # Get Interrupt Vector (AH=35h)
                    try:
                        # AL = interrupt number
                        # Return in ES:BX
                        int_num = self.registers[Register16Bits.AL][0]
                        
                        if int_num not in self.interrupt_vectors:
                            RenderModule(
                                "EXCEPTION",
                                "white",
                                f"Int Vector Not Found: {int_num}"
                            ).render()
                        seg, offset = self.interrupt_vectors[int_num]
                        self.registers[Register16Bits.ES][0] = seg
                        self.registers[Register16Bits.BX][0] = offset
                        self.registers[Register16Bits.CF][0] = 0
                        
                    except Exception as e:
                        self.registers[Register16Bits.CF][0] = 1
                        self.registers[Register16Bits.AX][0] = 0x0001  # Error code
                        RenderModule(
                            "EXCEPTION",
                            "white",
                            f"Int Vector Get Failed: {str(e)}"
                        ).render()

                case 0x2A:  # Get System Date (AH=2Ah)
                    from datetime import datetime
                    try:
                        now = datetime.now()
                        # CX = year (1980-2099)
                        self.registers[Register16Bits.CX][0] = now.year
                        # DH = month (1-12)
                        self.registers[Register16Bits.DH][0] = now.month
                        # DL = day (1-31)
                        self.registers[Register16Bits.DL][0] = now.day
                        # AL = day of week (0=Sunday)
                        self.registers[Register16Bits.AL][0] = now.weekday() + 1 % 7
                        
                        self.registers[Register16Bits.CF][0] = 0
                        
                    except Exception as e:
                        self.registers[Register16Bits.CF][0] = 1
                        RenderModule(
                            "EXCEPTION",
                            "white",
                            f"Date Get Failed: {str(e)}"
                        ).render()

                case 0x2C:  # Get System Time (AH=2Ch)
                    from datetime import datetime
                    try:
                        now = datetime.now()
                        # CH = hour (0-23)
                        self.registers[Register16Bits.CH][0] = now.hour
                        # CL = minute (0-59)
                        self.registers[Register16Bits.CL][0] = now.minute
                        # DH = second (0-59)
                        self.registers[Register16Bits.DH][0] = now.second
                        # DL = 1/100 seconds (0-99)
                        self.registers[Register16Bits.DL][0] = now.microsecond // 10000
                        
                        self.registers[Register16Bits.CF][0] = 0
                        
                    except Exception as e:
                        self.registers[Register16Bits.CF][0] = 1
                        RenderModule(
                            "EXCEPTION",
                            "white",
                            f"Time Get Failed: {str(e)}"
                        ).render()
                case _:
                    RenderModule(
                        "EXCEPTION",
                        "white",
                        f"Invalid AH Register Value: {self.registers[Register16Bits.AH][0]}"
                    ).render()
                            
    def FindMemoryAddrInSimulationMem(self,segment_reg_val: Register16Bits, offset: int):
        """
        Simulate memory addressing modes
        """
        # Real-mode address calculation: (segment << 4) + offset
        if not isinstance(segment_reg_val, Register16Bits):
            raise TypeError("Invalid segment register type")
            
        # Get segment value from registers (using index 0 as per IStore implementation)
        segment = self.registers[segment_reg_val][0]
        linear_addr = (segment << 4) + offset
            
        # Validate address range for 1MB memory (0x00000-0xFFFFF)
        if linear_addr < 0 or linear_addr >= len(self.memory):
            raise IndexError(f"[SILVERKEY VM][VM-SELF EXCEPTION]Calculated address 0x{linear_addr:X} out of 1MB memory range")
        return linear_addr
        

    def _get_console_input(self, os_type: str):
        """获取跨平台控制台输入流"""
        try:
            return open('CON', 'r') if os_type == 'Windows' else sys.stdin
        except FileNotFoundError:
            return sys.stdin  # 安全回退

    def _get_console_output(self, os_type: str):
        """获取跨平台控制台输出流"""
        try:
            return open('CON', 'w') if os_type == 'Windows' else sys.stdout
        except FileNotFoundError:
            return sys.stdout  # 安全回退
        
    def _convert_dos_filename(self, dos_name: str) -> str:
        """转换DOS 8.3文件名到现代格式"""
        # 处理通配符 (* 和 ?)
        if '*' in dos_name or '?' in dos_name:
            raise NotImplementedError("[SILVERKEY VM][DEEPWARN]Wildcard file names not supported")
        
        # 分割文件名和扩展名
        if '.' in dos_name:
            name_part, ext_part = dos_name.split('.', 1)
            name_part = name_part.ljust(8)[:8]  # 主名补足8字符
            ext_part = ext_part.ljust(3)[:3]    # 扩展名补足3字符
        else:
            name_part = dos_name.ljust(8)[:8]
            ext_part = ''
            
        # 生成现代文件名
        return f"{name_part.strip()}.{ext_part.strip()}".rstrip('.')
    
    