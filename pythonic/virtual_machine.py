from collections import namedtuple
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union


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
            # eval(f"self.x{idx - 2} = {val}")
            self.__dict__[f"x{idx - 2}"] = val


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
            number = to_int(
                code[registerFile.ip][1], "`push` instruction requires an integer argument.")
            stack.append(number)
            registerFile.ip += 1

        elif instruction == "load":
            addr = to_int(code[registerFile.ip][1],
                          "`load` instruction requires an address to load from.")
            if 0 <= addr < 10:  # load from register file
                stack.append(registerFile[addr])
            elif addr > 10:
                raise NotImplementedError("Need to implement RAM.")
            else:
                raise ValueError(f"Invalid address {addr}")

            registerFile.ip += 1

        elif instruction == "store":
            addr = to_int(code[registerFile.ip][1],
                          "`store` instruction requires an address to store to.")
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

        elif instruction == "mul":
            # sub the top two ints on the stack (and pop them), push the result
            stack.append(stack.pop() * stack.pop())
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
            addr = to_int(code[registerFile.ip][1],
                          "`beq` instruction requires an address to branch to.")
            if cmp_result == 0:
                registerFile.ip = addr
            else:
                registerFile.ip += 1

        elif instruction == "bgt":
            # if the result of the previous comparison was 1 then branch
            cmp_result = stack.pop()
            addr = to_int(code[registerFile.ip][1],
                          "`bgt` instruction requires an address to branch to.")
            if cmp_result == 1:
                registerFile.ip = addr
            else:
                registerFile.ip += 1

        elif instruction == "print":
            # just print the top of the stack
            print(stack[-1])
            registerFile.ip += 1

        elif instruction == "input":
            # read an integer from stdin and push it to the top of the stack
            stack.append(int(input(">>> ")))
            registerFile.ip += 1

        elif instruction == "noop":
            # don't do anything (apparently this is useful?)
            registerFile.ip += 1

        else:
            raise ValueError(f"Unknown instruction {code[registerFile.ip]}")

    return stack


def to_int(maybeAddr: Optional[int], msg: str) -> int:
    if maybeAddr is None:
        raise ValueError(msg)
    else:
        return maybeAddr
