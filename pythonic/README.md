# Stack Machine

This is a reference implementation of a stack machine in Python. The goal of
this project is to get a minimal stack machine working, with not much regard
to the performance of this particular implementation. At every step I have
chosen simplicity over speed. I plan to implement the same machine in Rust,
at which point this reference implementation will be useful.

- [Stack Machine](#stack-machine)
  - [To-dos](#to-dos)
  - [Known Issues](#known-issues)
  - [Running](#running)
  - [Assembly Instructions](#assembly-instructions)
  - [Registers](#registers)
  - [Memory](#memory)

## To-dos

- [x] Use a `bytearray` for memory
  - [x] Implement read/write
  - [x] Handle overflows (roll over while storing)
- [x] Use part of main memory as stack
  - [x] Test
- [x] Use part of main memory as code section
  - [x] Test
- [ ] Linker
- [ ] Memory-mapped I/O
- [ ] Allow data section in assembly
- [x] Write a bytecode assembler
- [x] Write a bytecode interpreter
- [ ] Read ascii as bytes from stdin

## Known Issues

- [ ] Labels currently cannot be substrings of each other. Use `re.replace` and match on whole word instead of `str.replace`.
- [ ] I/O is a kludge. MMIO must solve it.
## Running

You must follow the [Assembly Specification](#assembly-specification) to
write an assembly file that can then be interpreted by the virtual machine.
Note that this "assembly" format is really more like human-readable machine
code so there is no data or text section. For the sake of my sanity I have
implemented a rudimentary assembler that resolves labels within the same
assembly file.

Assuming your assembly code is in a file called `foo.asm`, then you can do the
following to execute the code in using the assembly interpreter
(please use the appropriate Python 3 executable on your system):
```bash
python run_assembly_interpreter.py foo.asm
```
This directly interprets the assembly text instead of interpreting bytecode.
If you want to do the latter, first assemble `foo.asm` to bytecode, then
run the bytecode:
```bash
python assemble_bytecode.py -i foo.asm -o foo.o
python run_vm.py foo.o
```

## Assembly Instructions

The table below lists all the operations natively supported by the VM. This is
very minimal, with only as many instructions as required to get a
[factorial](factorial.asm) benchmark working. I decided to make it
little-endian since that makes it somewhat easier to read memory for me.
The opcodes are all 1-byte long. The least significant byte is in the opcode
column below, the other bytes are ignored but should be set to `0`.

| Assembly Instruction | Opcode        | Description                                                                                                                   |
| -------------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `halt`               | `0x00`        | Halt program execution.                                                                                                       |
| `noop`               | `0x01`        | Just increment the instruction pointer. Not sure if it's useful.                                                              |
| `push arg`           | `0x02`        | Push `arg` to (the top of) the stack.                                                                                         |
| `load offset`        | `0x03`        | Push the value at address `addr + offset` to the stack, where `addr` is obtained by popping the stack.                        |
| `store offset`       | `0x04`        | Pop the stack and store it at `addr + offset` to the stack, where `addr` is obtained by popping the stack.                    |
| `add`/`sub`/`mul`    | `0x05`-`0x07` | Pop two values, perform the operation, push the result.                                                                       |
| `cmp`                | `0x20`        | Pop the top two values `t1` and `t2`. Push `sign(t1 - t2)`.                                                                   |
| `jmp`                | `0x21`        | Jump to the address at the top of the stack.                                                                                  |
| `beq addr`           | `0x22`        | Pop once, if the popped value is `0` then set the instruction pointer to `addr`, otherwise increment the instruction pointer. |
| `bgt addr`           | `0x23`        | Pop once, if the popped value is `1` then set the instruction pointer to `addr`, otherwise increment the instruction pointer. |
| `print`              | `0xf0`        | Print the top of the stack **without popping**.                                                                               |
| `input`              | `0xf1`        | Read an `int` from `stdin`, push it to the stack.                                                                             |


## Registers

There are no dedicated registers, but memory aliasing provides 11 registers.
The instruction pointer is at address `0`, the stack pointer at `1`, the
frame pointer at `2`, and the next eight 64-bit words are the general-purpose
registers `x1` through `x8`. I did not include a separate register bank since
that only creates additional complexity when loading and storing values without
adding any speed, since these are not hardware registers. However, using these
addresses as aliased registers will probably ensure that those memory addresses
stay in the processor's L1 cache, allowing fast access that way. Note that this
means there must be at least eleven 64-bit words in memory.

## Memory

As described in the [previous](#registers) section, the lowest eleven words of
memory (`0x00` through `0x0a`) are used as registers. Then the next five words
are used as padding. Reads/writes should never happen to addresses `0x0b`
through `0x0f`.

The code section starts at `0x10` and extends arbitrarily upwards (but it does
not grow at runtime). The end of the code section is not well-defined. The VM
will keep incrementing the instruction pointer until it hits a jump/branch/halt
instruction.

The stack starts at the highest address value and grows downwards. The stack
pointer holds the address of the top of the stack, which is one less than the
lowest address that belongs to the stack. `sp` points at the word that will be
written to during the next push, and one less than the word which will be
removed during the next pop.

The heap is unstructured, and there is nothing stopping the programmer from
rewriting the code or stack by taking appropriate pointers. One may implement
a memory allocator which prevents such shenanigans using appropriate
implementations of `malloc` and `free`.
