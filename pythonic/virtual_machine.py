from collections import namedtuple
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union


@dataclass(frozen=True)
class Halt:
    pass


@dataclass(frozen=True)
class Noop:
    pass


@dataclass(frozen=True)
class Push:
    num: int


@dataclass(frozen=True)
class Add:
    pass


@dataclass(frozen=True)
class Sub:
    pass


@dataclass(frozen=True)
class Cmp:
    pass


@dataclass(frozen=True)
class Jmp:
    pass


@dataclass(frozen=True)
class Beq:
    pass


@dataclass(frozen=True)
class Bgt:
    pass


@dataclass(frozen=True)
class Load:
    addr: int


@dataclass(frozen=True)
class Store:
    addr: int


@dataclass
class RegisterFile:
    ip: int = 0
    sp: int = 0
    x0: int = 0
    x1: int = 0
    x2: int = 0
    x3: int = 0
    x4: int = 0
    x5: int = 0
    x6: int = 0
    x7: int = 0

    def __getitem__(self, idx: int) -> int:
        if idx == 0:
            return self.ip
        elif idx == 1:
            return self.sp
        else:
            return eval(f"self.x{idx - 2}")

    def __setitem__(self, idx: int, val: int) -> None:
        if idx == 0:
            self.ip = val
        elif idx == 1:
            self.sp = val
        else:
            eval(f"self.x{idx - 2} = {val}")


def execute(code: List[Tuple[str, Optional[int]]]) -> List[int]:
    stack: List[int] = []
    registerFile = RegisterFile()

    while True:
        instruction = code[registerFile.ip][0]
        if instruction == "halt":
            # halt program execution
            break

        elif instruction == "jmp":
            # jump to the address at the top of the stack
            registerFile.ip = stack.pop()

        elif instruction == "push":
            # push an integer to the stack
            maybeNumber = code[registerFile.ip][1]
            if maybeNumber is None:
                raise TypeError(
                    "`push` instruction requires an integer argument.")
            else:  # we have a number for sure
                stack.append(maybeNumber)
            registerFile.ip += 1

        elif instruction == "load":
            maybeNumber = code[registerFile.ip][1]
            if maybeNumber is None:
                raise TypeError(
                    "`load` instruction requires an address to load from.")
            else:  # we have an address for sure
                addr = maybeNumber
                if 0 <= addr < 10:  # load from register file
                    stack.append(registerFile[addr])
                elif addr > 10:
                    raise NotImplementedError("Need to implement RAM.")
                else:
                    raise ValueError(f"Invalid address {addr}")

            registerFile.ip += 1

        elif instruction == "store":
            maybeNumber = code[registerFile.ip][1]
            if maybeNumber is None:
                raise TypeError(
                    "`store` instruction requires an address to store to.")
            else:  # we have an address for sure
                addr = maybeNumber
                if 0 <= addr < 10:  # store to register file
                    registerFile[addr] = stack.pop()
                elif addr > 10:
                    raise NotImplementedError("Need to implement RAM.")
                else:
                    raise ValueError(f"Invalid address {addr}")

            registerFile.ip += 1

        elif instruction == "add":
            # add the top two ints on the stack (and pop them), push the result
            stack.append(stack.pop() + stack.pop())
            registerFile.ip += 1

        elif instruction == "sub":
            # sub the top two ints on the stack (and pop them), push the result
            stack.append(stack.pop() - stack.pop())
            registerFile.ip += 1

        elif instruction == "cmp":
            # pop the top and second, push sign(top - second)
            def comparator(a, b):
                if a == b:
                    return 0
                elif a > b:
                    return 1
                else:
                    return -1
            stack.append(comparator(stack.pop(), stack.pop()))
            registerFile.ip += 1

        elif instruction == "beq":
            # if the result of the previous comparison was 0 then branch
            cmp_result = stack.pop()
            if cmp_result == 0:
                registerFile.ip = stack.pop()
            else:
                registerFile.ip += 1

        elif instruction == "bgt":
            # if the result of the previous comparison was 1 then branch
            cmp_result = stack.pop()
            if cmp_result == 1:
                registerFile.ip = stack.pop()
            else:
                registerFile.ip += 1

        elif instruction == "noop":
            # don't do anything (apparently this is useful?)
            registerFile.ip += 1

        else:
            raise ValueError(f"Unknown instruction {code[registerFile.ip]}")

    return stack
