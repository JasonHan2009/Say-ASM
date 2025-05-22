from enum import Enum
import platform
import sys
import ctypes

VM_MEM_SIZE: int = 1024
VM_REGISTER_SIZE: int = 65535

class Register16Bits(Enum):
    AX = "AX"
    BX = "BX"
    AH = "AH"
    CX = "CX"
    DX = "DX"
    SP = "SP"
    BP = "BP"
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
            case _:
                raise NotImplementedError("Unsupported Asm Platform!")

    def IStore(self, reg: Register16Bits, index: int, value: int):
        """Store value into register[index]"""
        if self.platform == 16:
            if index < 0 or index >= VM_REGISTER_SIZE:
                raise IndexError(f"Register index {index} out of range")
            if not (0 <= value <= 0xFFFF):
                raise ValueError(f"Value {value} exceeds 16-bit range")
                
            self.registers[reg][index] = value
    
    def IPush(self, reg: Register16Bits, index: int, value: int):
        """Push value into stack[index]"""
        if self.platform == 16:
            if index < 0 or index >= VM_MEM_SIZE:
                raise IndexError(f"Stack index {index} out of range")
            if not (0 <= value <= 0xFFFF):
                raise ValueError(f"Value {value} exceeds 16-bit range")
            
            self.stack_16[index] = value
    
    def IPop(self, reg: Register16Bits, index: int):
        """Pop value from stack[index]"""
        if self.platform == 16:
            if index < 0 or index >= VM_MEM_SIZE:
                raise IndexError(f"Stack index {index} out of range")
            
            return self.stack_16[index]

    def CallSysService(self):
        if self.platform == 16:
            AHVAL = self.registers[Register16Bits.AH][0]
            if sys.platform == "win32":
                match AHVAL:
                    # Get System PlatForm
                   case 1:
                        pass # TODO!