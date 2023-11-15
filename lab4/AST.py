from dataclasses import dataclass
from typing import Any


class Node(object):
    def print_indent(self, indent):
        print(indent * "|\t", end="")


@dataclass
class InstrOrEmpty(Node):
    instructions: Any = None


@dataclass
class Instructions(Node):
    instructions: Any = None


@dataclass
class If(Node):
    cond: Any
    if_body: Any
    else_body: Any = None


@dataclass
class Return(Node):
    expr: Any = None


@dataclass
class Break(Node):
    pass


@dataclass
class Continue(Node):
    pass


@dataclass
class For(Node):
    id: Any
    cond_start: Any
    cond_end: Any
    body: Any


@dataclass
class While(Node):
    cond: Any
    body: Any


@dataclass
class AssignOp(Node):
    left: Any
    op: Any
    right: Any


@dataclass
class Print(Node):
    printargs: Any


@dataclass
class String(Node):
    string: str


@dataclass
class IntNum(Node):
    intnum: int


@dataclass
class FloatNum(Node):
    floatnum: float


@dataclass
class Variable(Node):
    id: Any
    index: Any = None


@dataclass
class Id(Node):
    id: Any


@dataclass
class BinExpr(Node):
    left: Any
    op: Any
    right: Any


@dataclass
class Uminus(Node):
    val: Any


@dataclass
class Uneg(Node):
    val: Any


@dataclass
class Transpose(Node):
    val: Any


@dataclass
class Matrix(Node):
    matrix: Any


@dataclass
class MatrixFunc(Node):
    func: Any
    expr: Any

@dataclass
class Vector(Node):
    vector: Any


@dataclass
class Unary(Node):
    operation: str
    expr: Any

class Error(Node):
    def __init__(self):
        pass
