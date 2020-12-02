from collections import namedtuple
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

INT_MOD = 2**64


def execute(
    code: List[Tuple[str, Optional[int]]], stack: List[int], mem: bytearray
) -> List[int]:
    def getIp() -> int:
        # return int.from_bytes(mem[0:8], "little")
        return read_mem(0)

    def setIp(newIp: int) -> None:
        # mem[0:8] = newIp.to_bytes(8, "little")
        write_mem(0, newIp)

    def incIp() -> None:
        setIp(getIp() + 1)

    def read_mem(addr: int) -> int:
        """Read a 64-bit word starting at `addr`."""
        return int.from_bytes(mem[8*addr: 8*addr + 8], "little")

    def write_mem(addr: int, val: int) -> None:
        """Write a 64-bit word `val` starting at `addr`."""
        mem[8*addr: 8*addr + 8] = (val % INT_MOD).to_bytes(8, "little")

    def to_int(maybeAddr: Optional[int], msg: str) -> int:
        if maybeAddr is None:
            raise ValueError(msg)
        else:
            return maybeAddr

    while True:
        instruction = code[getIp()][0]
        if instruction == "halt":
            # halt program execution
            break

        elif instruction == "jmp":
            # jump to the address at the top of the stack
            setIp(stack.pop())

        elif instruction == "push":
            # push an integer to the stack
            number = to_int(
                code[getIp()][1], "`push` instruction requires an integer argument."
            )
            stack.append(number)
            incIp()

        elif instruction == "load":
            # addr = to_int(
            #     code[getIp()][1], "`load` instruction requires an address to load from."
            # )
            # if addr >= 0:
            #     stack.append(read_mem(addr))
            # else:
            #     raise ValueError(f"Invalid address {addr}")

            addr = stack.pop()
            offset = to_int(
                code[getIp()][1], "`load` instruction requires an address to load from."
            )
            stack.append(read_mem(addr + offset))

            incIp()

        elif instruction == "store":
            # addr = to_int(
            #     code[getIp()][1], "`store` instruction requires an address to store to."
            # )
            # if addr >= 0:
            #     write_mem(addr, stack.pop())
            # else:
            #     raise ValueError(f"Invalid address {addr}")

            addr = stack.pop()
            offset = to_int(
                code[getIp()][1], "`store` instruction requires an address to store to."
            )
            write_mem(addr + offset, stack.pop())

            incIp()

        elif instruction == "add":
            # add the top two ints on the stack (and pop them), push the result
            stack.append(stack.pop() + stack.pop())
            incIp()

        elif instruction == "sub":
            # sub the top two ints on the stack (and pop them), push the result
            stack.append(stack.pop() - stack.pop())
            incIp()

        elif instruction == "mul":
            # sub the top two ints on the stack (and pop them), push the result
            stack.append(stack.pop() * stack.pop())
            incIp()

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
            incIp()

        elif instruction == "beq":
            # if the result of the previous comparison was 0 then branch
            cmp_result = stack.pop()
            addr = to_int(
                code[getIp()][1], "`beq` instruction requires an address to branch to."
            )
            if cmp_result == 0:
                setIp(addr)
            else:
                incIp()

        elif instruction == "bgt":
            # if the result of the previous comparison was 1 then branch
            cmp_result = stack.pop()
            addr = to_int(
                code[getIp()][1], "`bgt` instruction requires an address to branch to."
            )
            if cmp_result == 1:
                setIp(addr)
            else:
                incIp()

        elif instruction == "print":
            # just print the top of the stack
            print(stack[-1])
            incIp()

        elif instruction == "input":
            # read an integer from stdin and push it to the top of the stack
            stack.append(int(input(">>> ")))
            incIp()

        elif instruction == "noop":
            # don't do anything (apparently this is useful?)
            incIp()

        else:
            raise ValueError(f"Unknown instruction {code[getIp()]}")

    return stack
