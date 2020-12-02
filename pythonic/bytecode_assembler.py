from opcodes import STR_TO_INT
from typing import List, Optional, Tuple


def assemble_bytecode(code: List[Tuple[str, Optional[int]]]) -> bytearray:
    bytecode = bytearray()
    for instruction, arg in code:
        bytecode.extend(STR_TO_INT[instruction].to_bytes(8, "little"))
        if arg is not None:
            bytecode.extend(arg.to_bytes(8, "little"))
    return bytecode
