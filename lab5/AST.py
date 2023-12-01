from dataclasses import dataclass
from typing import Any


class Node(object):
    def print_indent(self, indent):
        print(indent * "|\t", end="")


@dataclass
class InstrOrEmpty(Node):
    instructions: Any = None
    lineno: Any = 0


@dataclass
class Instructions(Node):
    instructions: Any = None
    lineno: Any = 0


@dataclass
class If(Node):
    cond: Any
    if_body: Any
    else_body: Any = None


@dataclass
class Return(Node):
    expr: Any = None
    lineno: Any = 0


@dataclass
class Break(Node):
    lineno: Any = 0
    pass


@dataclass
class Continue(Node):
    lineno: Any = 0
    pass


@dataclass
class For(Node):
    id: Any
    cond_start: Any
    cond_end: Any
    body: Any
    lineno: Any = 0


@dataclass
class While(Node):
    cond: Any
    body: Any
    lineno: Any = 0


@dataclass
class AssignOp(Node):
    left: Any
    op: Any
    right: Any
    lineno: Any = 0


@dataclass
class Print(Node):
    printargs: Any
    lineno: Any = 0


@dataclass
class String(Node):
    string: str
    lineno: Any = 0


@dataclass
class IntNum(Node):
    intnum: int
    lineno: Any = 0


@dataclass
class FloatNum(Node):
    floatnum: float
    lineno: Any = 0


@dataclass
class Variable(Node):
    id: Any
    index: Any = None
    lineno: Any = 0


@dataclass
class Id(Node):
    id: Any
    lineno: Any = 0


@dataclass
class BinExpr(Node):
    left: Any
    op: Any
    right: Any
    lineno: Any = 0
    dims: Any = None
    v_type: Any = None


@dataclass
class Uminus(Node):
    val: Any
    lineno: Any = 0


@dataclass
class Uneg(Node):
    val: Any
    lineno: Any = 0


@dataclass
class Transpose(Node):
    val: Any
    lineno: Any = 0


@dataclass
class Matrix(Node):
    matrix: Any
    lineno: Any = 0


@dataclass
class MatrixFunc(Node):
    func: Any
    dims: Any
    lineno: Any = 0
    v_type:Any = 'int'


class Vector(Node):
    def __init__(self, vector, lineno):
        self.vector = vector
        self.lineno = lineno
        self.dims = [len(vector)]
        self.v_type = None

        # print(vector)
        # print(type(vector[0]))

        if isinstance(vector[0], Vector):
            self.dims += vector[0].dims
        elif isinstance(vector[0], list):
            self.dims += [len(vector[0])]

        cd = vector
        while isinstance(cd, list) or isinstance(cd, Vector):
            if isinstance(cd, list):
                cd = cd[0]
            else:
                cd = cd.vector[0]

        if isinstance(cd, IntNum):
            self.v_type = 'int'
        if isinstance(cd, FloatNum):
            self.v_type = 'float'
        if isinstance(cd, String):
            self.v_type = 'str'



    def __repr__(self):
        return f"[{self.vector}], {self.dims}, {self.v_type}, {self.lineno}"


@dataclass
class Unary(Node):
    operation: str
    expr: Any
    lineno: Any = 0
    dims: Any = None


class Error(Node):
    def __init__(self):
        pass
