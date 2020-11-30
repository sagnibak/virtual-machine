from dataclasses import dataclass


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
class Print:
    pass


@dataclass(frozen=True)
class Beq:
    addr: int


@dataclass(frozen=True)
class Bgt:
    addr: int


@dataclass(frozen=True)
class Load:
    addr: int


@dataclass(frozen=True)
class Store:
    addr: int


@dataclass(frozen=True)
class Input:
    pass


@dataclass(frozen=True)
class Mul:
    pass
