import ply.lex as lex
import ply.yacc as yacc
from silver_key_vm.IDERender import RenderModule
from silver_key_vm.asm_tokens import *
from silver_key_vm.AST import AST

# 获取所有token
tokens = Register16Bits.tokens + Instructions.tokens + ('NEWLINE',)

# 语法规则
"""
DONT CHANGE THIS PART
"""
def p_program(p):
    """
    program : statement
            | program statement
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

# STATEMENT JP
def p_statement(p):
    """
    statement : expression NEWLINE
             | expression
    """
    p[0] = p[1]

# EXPR MAIN JP
def p_expression(p):
    """
    expression : bits
               | mov
    """
    p[0] = p[1]

# END

# THIS PART CAN CHANGE



# Get The Assembly PlatForm
def p_bits_check(p):
    """
    bits : BITS NUMBER
    """
    ast = AST('BITS', p[2], '')
    ast.platform_bits_parse() 
    p[0] = ast 

# Registers FOR 16 BITS
def p_registers16(p):
    """
    registers16 : AX 
                | BX 
                | CX 
                | DX 
                | DL 
                | SP 
                | BP 
                | SI 
                | CS 
                | DS 
                | SS 
                | ES 
                | AH 
                | IP 
    """
    p[0] = p[1]

########## INSTRUCTIONS ############
def p_mov_instruction(p):
    """
    mov : MOV registers16 COMMA NUMBER
        | MOV registers16 COMMA registers16
    """
    ast = AST("INSTRUCTION", "MOV", {
        "children" : AST("REGISTERS", p[2], p[4])
    })
    ast.instruction_parse()
    p[0] = ast

def p_push_instruction(p):
    """
    push : PUSH registers16
         | PUSH NUMBER
    """
    ast = AST("INSTRUCTION", "PUSH")
########## ERROR DUMP ##########
def p_error(p):
    if p:
        error_msg = f"[Syntax Error] At {lexer.lineno}Lines: Illeagal Char '{p.value}'"
    else:
        error_msg = "[Syntax Error] Error AT EOF"
    RenderModule("ERROR", "red", error_msg).render()

# 初始化解析器
lexer = lex.lex()
parser = yacc.yacc()

# 测试用例
if __name__ == "__main__":
    test_input = """
    MOV CX, 0X3ad
    """
    result = parser.parse(test_input)
    for node in result:
        node.print_ast()