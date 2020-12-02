HALT = 0x00
NOOP = 0x01
PUSH = 0x02
LOAD = 0x03
STORE = 0x04
ADD = 0x05
SUB = 0x06
MUL = 0x07
CMP = 0x20
JMP = 0x21
BEQ = 0x22
BGT = 0x23
PRINT = 0xF0
INPUT = 0xF1

STR_HALT = "halt"
STR_NOOP = "noop"
STR_PUSH = "push"
STR_LOAD = "load"
STR_STORE = "store"
STR_ADD = "add"
STR_SUB = "sub"
STR_MUL = "mul"
STR_CMP = "cmp"
STR_JMP = "jmp"
STR_BEQ = "beq"
STR_BGT = "bgt"
STR_PRINT = "print"
STR_INPUT = "input"

STR_TO_INT = {
    STR_HALT: HALT,
    STR_NOOP: NOOP,
    STR_PUSH: PUSH,
    STR_LOAD: LOAD,
    STR_STORE: STORE,
    STR_ADD: ADD,
    STR_SUB: SUB,
    STR_MUL: MUL,
    STR_CMP: CMP,
    STR_JMP: JMP,
    STR_BEQ: BEQ,
    STR_BGT: BGT,
    STR_PRINT: PRINT,
    STR_INPUT: INPUT,
}

