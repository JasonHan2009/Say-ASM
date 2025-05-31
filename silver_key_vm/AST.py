###
# Abstract Syntax Tree
# Dev JasonHan2009
# IdeaSphere
##

import json
from silver_key_vm.IDERender import Popup
from silver_key_vm.virtualmachine_main import VirtualMachineMain


class AST:

    def __init__(self, type, left, right):
        self.type = type
        self.left = left
        self.right = right
        self.ast_dict = {}
    
    def platform_bits_parse(self):
        if self.type == 'BITS' and str(self.left).isdigit() and self.right == '':
            # Get The PlatForm, Then Pass Value To VM
            self.vm = VirtualMachineMain(self.left)
            # Append Bits Into AST DICT
            if self.vm.flag == False:
                self.ast_dict.update({
                    "TYPE" : "PROGRAM",
                    "PLATFORM" : self.left,
                })
            else:
                Popup(
                    "bottom_right", 
                    "white", 
                    "INTERNAL ERROR", 
                    "You Are Choosing A Unsupported Assembly PlatForm!"
                ).render()
        return self
 
    def instruction_parse(self):
        if self.type == "INSTRUCTION":
            upper_case = self.left.upper()
            match upper_case:
                case "MOV":
                    self.ast_dict.update({
                        "TYPE" : "INSTRUCTION",
                        "INSTRUCTION" : "MOV",
                        "CHILDREN": {
                            "REGISTERS": self.right["children"].left, 
                            "VALUE": self.right["children"].right
                        }
                    })
                case "PUSH":
                    self.ast_dict.update(
                        {
                            "TYPE": "INSTRUCTION",
                            "INSTRUCTION": "PUSH",
                            "CHILDREN": {
                                "VALUE": self.left
                            }
                        }
                    )               
        return self

    def memory_address_parse(self):
        if self.type == "MEMORY_ADDRESS":
            self.ast_dict.update(
                {
                    "TYPE": "MEMORY_ADDRESS",
                    "CHILDREN": {
                        "BEGIN": self.left,
                        "NEXT": self.right
                    }
                }
            )
        return self
    def print_ast(self):
        """Prints the AST structure in JSON format"""
        if not self.ast_dict:
            print("AST is empty")
            return
        
        try:
            print(json.dumps(self.ast_dict, indent=4))
        except TypeError:
            Popup(
                "bottom_right",
                "white",
                "SERIALIZATION ERROR",
                "Non-serializable object detected in AST"
            ).render()
        