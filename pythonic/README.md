# Stack Machine

This is a reference implementation of a stack machine in Python. The goal of
this project is to get a minimal stack machine working, with not much regard
to the performance of this particular implementation. At every step I have
chosen simplicity over speed. I plan to implement the same machine in Rust,
at which point this reference implementation will be useful.

- [Stack Machine](#stack-machine)
  - [To-dos](#to-dos)
  - [Running](#running)
  - [Assembly Instructions](#assembly-instructions)
  - [Registers](#registers)

## To-dos

- [ ] Use a `bytearray` for memory
  - [ ] Implement read/write
  - [ ] Handle overflows
- [ ] Allow data section in assembly
- [ ] Write a bytecode assembler
- [ ] Write a bytecode interpreter
## Running

You must follow the [Assembly Specification](#assembly-specification) to
write an assembly file that can then be interpreted by the virtual machine.
Note that this "assembly" format is really more like human-readable machine
code so there is no data or text section. For the sake of my sanity I have
implemented a rudimentary assembler that resolves labels within the same
assembly file.

Assuming your assembly code is in a file called `foo.asm`, then you can do the
following to execute the code in the VM (please use the appropriate Python 3
executable on your system):
```bash
python run_vm.py foo.asm
```

## Assembly Instructions

The table below lists all the operations natively supported by the VM. This is
very minimal, with only as many instructions as required to get a
[factorial](factorial.asm) benchmark working.

| Assembly Instruction | Description                                                                                                                   |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `halt`               | Halt program execution.                                                                                                       |
| `jmp`                | Jump to the address at the top of the stack.                                                                                  |
| `push arg`           | Push `arg` to (the top of) the stack.                                                                                         |
| `load addr`          | Push the value at address `addr` to the stack.                                                                                |
| `store addr`         | Pop (the top of) the stack and store it at `addr`.                                                                            |
| `add`/`sub`/`mul`    | Pop two values, perform the operation, push the result.                                                                       |
| `cmp`                | Pop the top two values `t1` and `t2`. Push `sign(t1 - t2)`.                                                                   |
| `beq addr`           | Pop once, if the popped value is `0` then set the instruction pointer to `addr`, otherwise increment the instruction pointer. |
| `bgt addr`           | Pop once, if the popped value is `1` then set the instruction pointer to `addr`, otherwise increment the instruction pointer. |
| `print`              | Print the top of the stack **without popping**.                                                                               |
| `input`              | Read an `int` from `stdin`, push it to the stack.                                                                             |
| `noop`               | Just increment the instruction pointer. Not sure if it's useful.                                                              |


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
