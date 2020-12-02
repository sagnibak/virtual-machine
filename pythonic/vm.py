from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Optional
from opcodes import *

INT_MOD = 2 ** 64


@dataclass
class VM:
    mem: bytearray
    isHalted: bool = False

    def readMem(self, addr: int) -> int:
        """Read a 64-bit word starting at `addr`."""
        return int.from_bytes(self.mem[8 * addr : 8 * addr + 8], "little")

    def writeMem(self, addr: int, val: int) -> None:
        """Write a 64-bit word `val` starting at `addr`."""
        self.mem[8 * addr : 8 * addr + 8] = (val % INT_MOD).to_bytes(8, "little")

    # methods for working with the instruction pointer
    def getIp(self) -> int:
        return self.readMem(0)

    def setIp(self, newIp: int) -> None:
        self.writeMem(0, newIp)

    def incIp(self) -> None:
        self.setIp(self.getIp() + 1)

    # methods for working with the stack
    def pushStack(self, val: int) -> None:
        sp = self.readMem(1)  # read stack pointer
        self.writeMem(sp, val)  # push to stack
        self.writeMem(1, sp - 1)  # stack grows downwards

    def popStack(self) -> int:
        sp = self.readMem(1)
        self.writeMem(1, sp + 1)
        return self.readMem(sp + 1)

    # methods for operating the VM
    def run(self) -> VM:
        while not self.isHalted:
            self.step()
        return self

    def reset(self) -> VM:
        # set the instruction pointer to the first instruction
        self.setIp(0x10)
        # set the stack pointer to the last address
        self.writeMem(1, (len(self.mem) // 8) - 1)
        # mark the CPU as ready for operation
        self.isHalted = False
        # allow operation chaining
        return self

    def step(self) -> None:
        """Executes one instruction."""
        if self.isHalted:
            raise RuntimeError("Trying to step a halted CPU.")

        # fetch the next instruction
        instruction = self.readMem(self.getIp())
        # print(
        #     f"Executing instruction {instruction:02x}, next: {self.readMem(self.getIp() + 1):02x}, ip: {self.getIp():02x}"
        # )
        # print(f"Registers: {self.mem[:88]}")

        # decode and execute
        if instruction == HALT:
            self.isHalted = True

        elif instruction == NOOP:
            self.incIp()

        elif instruction == PUSH:
            self.incIp()
            self.pushStack(self.readMem(self.getIp()))
            self.incIp()

        elif instruction == LOAD:
            addr = self.popStack()
            self.incIp()
            offset = self.readMem(self.getIp())
            self.pushStack(self.readMem(addr + offset))
            self.incIp()

        elif instruction == STORE:
            addr = self.popStack()
            self.incIp()
            offset = self.readMem(self.getIp())
            self.writeMem(addr + offset, self.popStack())
            self.incIp()

        elif instruction == ADD:
            self.pushStack(self.popStack() + self.popStack())
            self.incIp()

        elif instruction == SUB:
            self.pushStack(self.popStack() - self.popStack())
            self.incIp()

        elif instruction == MUL:
            self.pushStack(self.popStack() * self.popStack())
            self.incIp()

        elif instruction == CMP:

            def comparator(a, b):
                if a == b:
                    return 0
                elif a > b:
                    return 1
                else:
                    return -1

            self.pushStack(comparator(self.popStack(), self.popStack()))
            self.incIp()

        elif instruction == JMP:
            self.setIp(self.popStack())

        elif instruction == BEQ:
            cmpResult = self.popStack()
            self.incIp()
            addr = self.readMem(self.getIp())
            if cmpResult == 0:
                self.setIp(addr)
            else:
                self.incIp()

        elif instruction == BGT:
            cmpResult = self.popStack()
            self.incIp()
            addr = self.readMem(self.getIp())
            if cmpResult == 1:
                self.setIp(addr)
            else:
                self.incIp()

        elif instruction == PRINT:
            top = self.popStack()
            print(top)
            self.pushStack(top)
            self.incIp()

        elif instruction == INPUT:
            # self.pushStack(
            #     int.from_bytes(
            #         bytes(input(">>> ").ljust(8, "\0")[:8], "ascii"), "little"
            #     )
            # )
            self.pushStack(int(input(">>> ")))
            self.incIp()

        else:
            raise ValueError(f"Unknown instruction {instruction}")
