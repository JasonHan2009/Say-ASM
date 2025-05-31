# TOKENS
# DEV JASONHAN2009
# IDEASPHERE

class Register16Bits:
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

class Instructions:
    tokens = (
        'NUMBER',
        'COMMA',
        'COLON',
        'MULTIPLY',
        'DOT',
        'IDENTIFIER',
        'BITS',

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
        'BSS',

        'COMMENT',
    )

t_COMMA = r','
t_COLON = r':'
t_DOT = r'\.'
t_ignore = ' \t\r\n'
t_COMMENT = ';.*'

def t_MOV(t):
    r'(?i:MOV)'
    return t

def t_PUSH(t):
    r'(?i:PUSH)'
    return t

def t_AX(t):
    r'(?i:AX)'
    return t

def t_BX(t):
    r'(?i:BX)'
    return t

def t_CX(t):
    r'(?i:CX)'
    return t

def t_DX(t):
    r'(?i:DX)'
    return t

def t_DL(t):
    r'(?i:DL)'
    return t

def t_SP(t):
    r'(?i:SP)'
    return t

def t_BP(t):
    r'(?i:BP)'
    return t

def t_SI(t):
    r'(?i:SI)'
    return t

def t_CS(t):
    r'(?i:CS)'
    return t

def t_DS(t):
    r'(?i:DS)'
    return t


def t_ES(t):
    r'(?i:ES)'
    return t


def t_SS(t):
    r'(?i:SS)'
    return t

def t_AH(t):
    r'(?i:AH)'
    return t


def t_IP(t):
    r'(?i:IP)'
    return t

def t_LEA(t):
    r'(?i:LEA)'
    return t

def t_ADD(t):
    r'(?i:ADD)'
    return t

def t_SUB(t):
    r'(?i:SUB)'
    return t

def t_INC(t):
    r'(?i:INC)'
    return t

def t_DEC(t):
    r'(?i:DEC)'
    return t

def t_MUL(t):
    r'(?i:MUL)'
    return t


def t_DIV(t):
    r'(?i:DIV)'
    return t

def t_IMUL(t):
    r'(?i:IMUL)'
    return t

def t_IDIV(t):
    r'(?i:IDIV)'
    return t

def t_CMP(t):
    r'(?i:CMP)'
    return t

def t_AND(t):
    r'(?i:AND)'
    return t

def t_OR(t):
    r'(?i:OR)'
    return t

def t_XOR(t):
    r'(?i:XOR)'
    return t

def t_NOT(t):
    r'(?i:NOT)'
    return t

def t_SHL(t):
    r'(?i:SHL)'
    return t

def t_SHR(t):
    r'(?i:SHR)'
    return t

def t_ROL(t):
    r'(?i:ROL)'
    return t

def t_ROR(t):
    r'(?i:ROR)'
    return t

def t_TEST(t):
    r'(?i:TEST)'
    return t

def t_JMP(t):
    r'(?i:JMP)'
    return t

def t_JNE(t):
    r'(?i:JNE)'
    return t

def t_JE(t):
    r'(?i:JE)'
    return t

def t_JG(t):
    r'(?i:JG)'
    return t

def t_JL(t):
    r'(?i:JL)'
    return t

def t_CALL(t):
    r'(?i:CALL)'
    return t

def t_RET(t):
    r'(?i:RET)'
    return t

def t_LOOP(t):
    r'(?i:LOOP)'
    return t

def t_MOVSB(t):
    r'(?i:MOVSB)'
    return t

def t_MOVSW(t):
    r'(?i:MOVSW)'
    return t

def t_CMPSB(t):
    r'(?i:CMPSB)'
    return t

def t_CMPSW(t):
    r'(?i:CMPSW)'
    return t

def t_SCASB(t):
    r'(?i:SCASB)'
    return t

def t_SCASW(t):
    r'(?i:SCASW)'
    return t

def t_LODSB(t):
    r'(?i:LODSB)'
    return t

def t_LODSW(t):
    r'(?i:LODSW)'
    return t

def t_STOSB(t):
    r'(?i:STOSB)'
    return t

def t_STOSW(t):
    r'(?i:STOSW)'
    return t

def t_STI(t):
    r'(?i:STI)'
    return t

def t_CLI(t):
    r'(?i:CLI)'
    return t

def t_HLT(t):
    r'(?i:HLT)'
    return t

def t_NOP(t):
    r'(?i:NOP)'
    return t

def t_CLC(t):
    r'(?i:CLC)'
    return t

def t_STC(t):
    r'(?i:STC)'
    return t

def t_INT(t):
    r'(?i:INT)'
    return t

def t_IRET(t):
    r'(?i:IRET)'
    return t

def t_DW(t):
    r'(?i:DW)'
    return t

def t_DD(t):
    r'(?i:DD)'
    return t

def t_DQ(t):
    r'(?i:DQ)'
    return t    

def t_DB(t):
    r'(?i:DB)'
    return t

def t_RESB(t):
    r'(?i:RESB)'
    return t

def t_RESW(t):
    r'(?i:RESW)'
    return t

def t_RESD(t):
    r'(?i:RESD)'
    return t

def t_RESQ(t):
    r'(?i:RESQ)'
    return t

def t_SECTION(t):
    r'(?i:SECTION)'
    return t

def t_DATA(t):
    r'(?i:DATA)'
    return t

def t_CODE(t):
    r'(?i:CODE)'
    return t

def t_BSS(t):
    r'(?i:BSS)'
    return t

def t_BITS(t):
    r'(?i:BITS)'
    return t
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'  
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

def t_error(t):
    print("[SILVERKEY VM]Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_NUMBER(t):
    r'(?i:0x[0-9a-fA-F]+|\d+)'
    try:
        t.value = t.value
    except ValueError:
        print(f"Invalid number format: {t.value}")
        t.error = True
    return t