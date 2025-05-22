import ply.lex as lex

class REGISTERS_16BITS:
    tokens = (
        'AX',
        'BX',
        'CX',
        'DX',
        'DL',

        'SP',
        'BP',
        'SI',
        'CS',
        'DS',
        'SS',
        'ES',
        'AH',

        'IP'
    )

class GENERALLY_ASM_INSTRUCTION:
    tokens = (
        'NUMBER',
        'COMMA',
        'COLON',
        'DOT',
        'IDENTIFIER',

        'MOV',
        'PUSH',
        'POP',
        'LEA',
        'ADD',
        'SUB',
        'INC',
        'DEC',
        'MUL',
        'DIV',
        'IMUL',
        'IDIV',
        'CMP',
        'AND',
        'OR',
        'XOR',
        'NOT',
        'SHL',
        'SHR',
        'ROL',
        'ROR',
        'TEST',

        'JMP',
        'JNE',
        'JE',
        'JG',
        'JL',
        'CALL',
        'RET',
        'LOOP',

        'MOVSB',
        'MOVSW',
        'CMPSB',
        'CMPSW',
        'SCASB',
        'SCASW',
        'LODSB',
        'LODSW',
        'STOSB',
        'STOSW',

        'STI',
        'CLI',
        'HLT',
        'NOP',
        'CLC',
        'STC',
        'INT',
        'IRET',

        'DW',
        'DD',
        'DQ',
        'DB',

        'RESB',
        'RESW',
        'RESD',
        'RESQ',

        'SECTION',
        'DATA',
        'CODE',
        'BSS'


        
    )

t_MOV = r'(?i:MOV)'
t_PUSH = r'(?i:PUSH)'
t_POP = r'(?i:POP)'
t_LEA = r'(?i:LEA)'
t_ADD = r'(?i:ADD)'
t_SUB = r'(?i:SUB)'
t_INC = r'(?i:INC)'
t_DEC = r'(?i:DEC)'
t_MUL = r'(?i:MUL)'
t_DIV = r'(?i:DIV)'
t_IMUL = r'(?i:IMUL)'
t_IDIV = r'(?i:IDIV)'
t_CMP = r'(?i:CMP)'
t_AND = r'(?i:AND)'
t_OR = r'(?i:OR)'
t_XOR = r'(?i:XOR)'
t_NOT = r'(?i:NOT)'
t_SHL = r'(?i:SHL)'
t_SHR = r'(?i:SHR)'
t_ROL = r'(?i:ROL)'
t_ROR = r'(?i:ROR)'
t_TEST = r'(?i:TEST)'

t_JMP = r'(?i:JMP)'
t_JNE = r'(?i:JNE)'
t_JE = r'(?i:JE)'
t_JG = r'(?i:JG)'
t_JL = r'(?i:JL)'
t_CALL = r'(?i:CALL)'
t_RET = r'(?i:RET)'
t_LOOP = r'(?i:LOOP)'

t_MOVSB = r'(?i:MOVSB)'
t_MOVSW = r'(?i:MOVSW)'
t_CMPSB = r'(?i:CMPSB)'
t_CMPSW = r'(?i:CMPSW)'
t_SCASB = r'(?i:SCASB)'
t_SCASW = r'(?i:SCASW)'
t_LODSB = r'(?i:LODSB)'
t_LODSW = r'(?i:LODSW)'
t_STOSB = r'(?i:STOSB)'
t_STOSW = r'(?i:STOSW)'

t_STI = r'(?i:STI)'
t_CLI = r'(?i:CLI)'
t_HLT = r'(?i:HLT)'
t_NOP = r'(?i:NOP)'
t_CLC = r'(?i:CLC)'
t_STC = r'(?i:STC)'
t_INT = r'(?i:INT)'
t_IRET = r'(?i:IRET)'

t_DW = r'(?i:DW)'
t_DD = r'(?i:DD)'
t_DQ = r'(?i:DQ)'
t_DB = r'(?i:DB)'

t_RESB = r'(?i:RESB)'
t_RESW = r'(?i:RESW)'
t_RESD = r'(?i:RESD)'
t_RESQ = r'(?i:RESQ)'

t_SECTION = r'(?i:SECTION)'
t_DATA = r'(?i:DATA)'
t_CODE = r'(?i:CODE)'
t_BSS = r'(?i:BSS)'

t_COMMA = r','
t_COLON = r':'
t_DOT = r'\.'
t_ignore = ' \t' 
t_AX = r'(?i:AX)'
t_BX = r'(?i:BX)'
t_CX = r'(?i:CX)'
t_DX = r'(?i:DX)'
t_SP = r'(?i:SP)'
t_BP = r'(?i:BP)'
t_SI = r'(?i:SI)'
t_DL = r'(?i:DL)'
t_CS = r'(?i:CS)'
t_DS = r'(?i:DS)'
t_SS = r'(?i:SS)'
t_ES = r'(?i:ES)'
t_IP = r'(?i:IP)'
t_AH = r'(?i:AH)'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'  # Standard identifier pattern
    return t

def t_error(t):
    print("[SILVERKEY VM]Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

"""
tokens = GENERALLY_ASM_INSTRUCTION.tokens
tokens = SIXTEEN_BITS_TOKENS.tokens
lexer = lex.lex()
lexer.input('1,2:3.4S')
for token in lexer:
    print(token)
"""