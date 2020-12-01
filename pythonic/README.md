# Stack Machine

This is a reference implementation of a stack machine in Python. The goal of
this project is to get a minimal stack machine working, with not much regard
to the performance of this particular implementation. At every step I have
chosen simplicity over speed. I plan to implement the same machine in Rust,
at which point this reference implementation will be useful.

## Assembly Specification

The table below lists all the operations natively supported by the VM. This is
very minimal, with only as many instructions as required to get a
(factorial)[factorial.asm] benchmark working.

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