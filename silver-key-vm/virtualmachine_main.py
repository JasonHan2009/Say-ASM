from enum import Enum
from SAYYASMCONST import *
from keystone import *
import ctypes
import mmap

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
    CS = "CS"
    DS = "DS"
    SS = "SS"
    ES = "ES"
    IP = "IP"

class VirtualMachineMain:
    def __init__(self, platform):
        match platform:
            case 16:
                self.registers = {reg: [0] * VM_REGISTER_SIZE for reg in Register16Bits}
                self.stack_16 = [0] * VM_MEM_SIZE
                self.platform = platform
                self.memory = bytearray(1024 * 1024)  # 1MB Physics Memory
            case _:
                raise NotImplementedError("Unsupported Asm Platform!")

    def write_memory(self, address: int, data: bytes):
        """Write Binary Into Simulation Memory"""
        for offset, byte in enumerate(data):
            if address + offset >= len(self.memory):
                raise IndexError(f"Memory address 0x{address + offset:X} out of range")
            self.memory[address + offset] = byte

    def IStore(self, reg: Register16Bits, index: int, value: int):
        """
        Store value into register[index]
        """
        if self.platform == 16:
            if index < 0 or index >= VM_REGISTER_SIZE:
                raise IndexError(f"Register index {index} out of range")
            if not (0 <= value <= 0xFFFF):
                raise ValueError(f"Value {value} exceeds 16-bit range")
                
            self.registers[reg][index] = value
    
    def IPush(self, reg: Register16Bits, index: int, value: int):
        """
        Push value into stack[index]
        """
        if self.platform == 16:
            if index < 0 or index >= VM_MEM_SIZE:
                raise IndexError(f"Stack index {index} out of range")
            if not (0 <= value <= 0xFFFF):
                raise ValueError(f"Value {value} exceeds 16-bit range")
            
            self.stack_16[index] = value
    
    def IPop(self, reg: Register16Bits, index: int):
        """
        Pop value from stack[index]
        """
        if self.platform == 16:
            if index < 0 or index >= VM_MEM_SIZE:
                raise IndexError(f"Stack index {index} out of range")
            
            return self.stack_16[index]
    
    def IReset(self, reg : Register16Bits, index: int):
        """
        Reset value to stack[index]
        """
        if self.platform == 16:
            if index < 0 or index >= VM_MEM_SIZE:
                raise IndexError(f"Stack index {index} out of range")
            
            self.stack_16[index] = 0

    def CallSysService(self):
        """
        Call the system service
        Its not simulate in array, its directly write into mem
        """
        if self.platform == 16: 
            AHVAL = self.registers[Register16Bits.AH][0]
            match AHVAL:
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
                        raise IOError(
                                        "[SILVERKEY VM][DEEP WARN]It May Caused Segement Fault Or Other Questions In Real Env, Please Check Your Code" +
                                        "May Its AL Register Caused"
                                      )
                case 0x02:
                    DLVAL = self.registers[Register16Bits.DL][0]
                    if 0 <= DLVAL <= 0xFF:
                        print(chr(DLVAL), end='', flush=True) 
                    else:
                        raise ValueError(f"[SILVERKEY VM][EXCEPTION]Invalid ASCII value in DL: 0x{DLVAL:X}")

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
                                raise IndexError("String exceeds memory bounds")

                        # 转换并输出字符串
                        decoded_str = bytes(output).decode('ascii', errors='replace')
                        print(decoded_str, end='')
                        
                    except IndexError as e:
                        raise IOError(f"[SILVERKEY VM] Memory access error: {str(e)}")