import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys

sys.setrecursionlimit(10000)


def mat_add(a, b):
    # print(a, b)
    for i in range(len(a)):
        if isinstance(a[0], list):
            for j in range(len(a[0])):
                a[i][j] += b[i][j]
        else:
            a[i] += b[i]
    return a


def mat_sub(a, b):
    for i in range(len(a)):
        if isinstance(a[0], list):
            for j in range(len(a[0])):
                a[i][j] -= b[i][j]
        else:
            a[i] -= b[i]
    return a

def mat_mul(a, b):
    for i in range(len(a)):
        if isinstance(a[0], list):
            for j in range(len(a[0])):
                a[i][j] *= b[i][j]
        else:
            a[i] *= b[i]
    return a

def mat_div(a, b):
    for i in range(len(a)):
        if isinstance(a[0], list):
            for j in range(len(a[0])):
                a[i][j] /= b[i][j]
        else:
            a[i] /= b[i]
    return a

def transpose(a):
    return [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]


operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '<': lambda x, y: x < y,
    '>': lambda x, y: x > y,
    '<=': lambda x, y: x <= y,
    '>=': lambda x, y: x >= y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
    '.+': lambda x, y: mat_add(x, y),
    '.-': lambda x, y: mat_sub(x, y),
    '.*': lambda x, y: mat_mul(x, y),
    './': lambda x, y: mat_div(x, y)
}


class Interpreter(object):
    @on('node')
    def visit(self, node):
        pass

    @when(AST.InstrOrEmpty)
    def visit(self, node: AST.Instructions):
        self.memory = MemoryStack()
        self.memory.push('global')
        node.instructions.accept(self)

    @when(AST.Instructions)
    def visit(self, node: AST.Instructions):
        for instruction in node.instructions:
            instruction.accept(self)

    @when(AST.BinExpr)
    def visit(self, node: AST.BinExpr):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)

        # print("r1, r2", r1, r2)
        # print(operations[node.op](r1, r2))

        # print(r1, node.op, r2, 'memory:', self.memory.stack[-1].memory)
        return operations[node.op](r1, r2)

    @when(AST.Unary)
    def visit(self, node: AST.Unary):
        r1 = node.expr.accept(self)
        if node.operation == "TRANSPOSE":
            return transpose(r1)
        else:
            return -r1

    @when(AST.Id)
    def visit(self, node: AST.Id):

        return self.memory.get(node.id)

    @when(AST.IntNum)
    def visit(self, node: AST.IntNum):
        return int(node.intnum)

    @when(AST.FloatNum)
    def visit(self, node: AST.FloatNum):
        return float(node.floatnum)

    @when(AST.String)
    def visit(self, node: AST.String):
        return str(node.string)

    @when(AST.If)
    def visit(self, node: AST.If):
        condition = node.cond.accept(self)
        if condition:
            self.memory.push('if')
            if isinstance(node.if_body, AST.Instructions):
                node.if_body.accept(self)
            else:
                for instruction in node.if_body:
                    instruction.accept(self)
            self.memory.pop()
        else:
            if node.else_body is not None:
                self.memory.push('else')
                node.else_body.accept(self)
                self.memory.pop()

    @when(AST.While)
    def visit(self, node: AST.While):
        self.memory.push("while")
        while node.cond.accept(self):
            try:
                if isinstance(node.body, list):
                    for instruction in node.body:
                        instruction.accept(self)
                else:
                    node.body.accept(self)
            except ContinueException:
                continue
            except BreakException:
                break
        self.memory.pop()

    @when(AST.For)
    def visit(self, node: AST.For):
        iterator = node.id
        start = node.cond_start.accept(self)
        end = node.cond_end.accept(self)
        self.memory.push("for")
        self.memory.set(iterator.id, start)
        while self.memory.get(iterator.id) <= end:
            try:
                if isinstance(node.body, list):
                    for instruction in node.body:
                        instruction.accept(self)
                else:
                    node.body.accept(self)
            except ContinueException:
                continue
            except BreakException:
                break
            finally:
                self.memory.set(iterator.id, self.memory.get(iterator.id) + 1)
        self.memory.pop()

    @when(AST.Return)
    def visit(self, node: AST.Return):
        raise ReturnValueException(node.expr.accept(self))

    @when(AST.Break)
    def visit(self, node: AST.Break):
        raise BreakException()

    @when(AST.Continue)
    def visit(self, node: AST.Continue):
        raise ContinueException

    @when(AST.Print)
    def visit(self, node: AST.Print):
        # print(node)
        # print(self.memory.get("C"))
        to_print = [element.accept(self) for element in node.printargs]
        print(*to_print, sep=' ')

    @when(AST.AssignOp)
    def visit(self, node: AST.AssignOp):
        if not isinstance(node.left, AST.Variable):
            if node.op == '=':
                # print("ah", node.op, node.left, node.right)
                # print("before", self.memory.get(node.left.id))
                self.memory.set(node.left.id, node.right.accept(self))
                # print("after", self.memory.get(node.left.id))
                # print(self.memory.get(node.left.id))
            else:
                # print("before else", self.memory.get(node.left.id))
                # print("to", node.op, node.left.id, node.right, self.memory.get(node.right.id), self.memory.get(node.left.id))
                self.memory.set(node.left.id, operations[node.op[0]](self.memory.get(node.left.id), node.right.accept(self)))
                # print("after else", self.memory.get(node.left.id))
        else:
            # print(node.left, node.right)
            matrix = self.memory.get(node.left.id.id)
            if isinstance(node.left.index[0], tuple):
                x = [i for i in range(node.left.index[0][0].accept(self), node.left.index[0][1].accept(self))]
            else:
                x = [node.left.index[0].accept(self)]
            if isinstance(node.left.index[1], tuple):
                y = [i for i in range(node.left.index[1][0].accept(self), node.left.index[1][1].accept(self))]
            else:
                y = [node.left.index[1].accept(self)]
            # y = node.left.index[1].accept(self)
            # print(x, y, matrix)
            if node.op == '=':
                for i in x:
                    for j in y:
                        # print(matrix, i, j)
                        matrix[j][i] = node.right.accept(self)
            else:
                for i in x:
                    for j in y:
                        matrix[j][i] = operations[node.op[0]](matrix[j][i], node.right.accept(self))

            self.memory.set(node.left.id.id, matrix)
        # print(f'after {node.var_id.name} assignment:', self.memory.stack[-1].memory)

    @when(AST.Vector)
    def visit(self, node: AST.Vector):
        return [element.accept(self) for element in node.vector]

    @when(AST.Variable)
    def visit(self, node: AST.Variable):
        matrix = self.memory.get(node.id.id)

        # Tylko dla macierzy 2x2
        x = node.index[0].accept(self)
        y = node.index[1].accept(self)

        return matrix[x][y]

    @when(AST.MatrixFunc)
    def visit(self, node: AST.MatrixFunc):
        func = node.func
        args = [dim.accept(self) for dim in node.dims]
        # print("args", args)
        if func == 'zeros':
            if len(args) == 2:
                return [[0 for _ in range(args[0])] for _ in range(args[1])]
            else:
                return [0 for _ in range(args[0])]
        elif func == 'ones':
            if len(args) == 2:
                return [[1 for _ in range(args[0])] for _ in range(args[1])]
            else:
                return [1 for _ in range(args[0])]
        elif func == 'eye':
            if len(args) == 2:
                return [[1 if i == j else 0 for i in range(args[0])] for j in range(args[0])]
            else:
                return [1 for _ in range(args[0])]

    # @when(AST.MatrixFunction)
    # def visit(self, node: AST.MatrixFunction):
    #     return node.function