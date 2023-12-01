# from __future__ import print_function
import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.InstrOrEmpty)
    def printTree(self, indent=0):
        self.instructions.printTree(indent)

    # @addToClass(AST.Instructions)
    # def printTree(self,i):


    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            # print(instruction)
            # print(self.instructions)
            # print(instruction)
            # print(instruction, type(instruction))
            instruction.printTree(indent)

    @addToClass(AST.If)
    def printTree(self, indent):
        self.print_indent(indent)
        print("IF")
        self.cond.printTree(indent+1)
        self.print_indent(indent)
        print("THEN")
        # for x in self.if_body:
        #     x.printTree(indent+1)
        self.if_body.printTree(indent+1)
        if self.else_body is not None:
            self.print_indent(indent)
            print("ELSE")
            # for x in self.else_body:
            #     x.printTree(indent+1)
            self.else_body.printTree(indent+1)


    @addToClass(AST.Return)
    def printTree(self, indent):
        self.print_indent(indent)
        print("RETURN")
        if self.expr is not None:
            self.expr.printTree(indent+1)

    @addToClass(AST.Break)
    def printTree(self, i):
        self.print_indent(i)
        print("BREAK")

    @addToClass(AST.Continue)
    def printTree(self, i):
        self.print_indent(i)
        print("CONTINUE")

    @addToClass(AST.For)
    def printTree(self, i):
        self.print_indent(i)
        print("FOR")
        self.id.printTree(i+1)
        self.print_indent(i+1)
        print("RANGE")
        self.cond_start.printTree(i+2)
        self.cond_end.printTree(i+2)
        self.body.printTree(i+1)

    @addToClass(AST.While)
    def printTree(self, i):
        self.print_indent(i)
        print("WHILE")
        self.cond.printTree(i+1)
        self.body.printTree(i+1)


    @addToClass(AST.AssignOp)
    def printTree(self, i):
        self.print_indent(i)
        print(self.op)
        self.left.printTree(i+1)
        self.right.printTree(i+1)

    @addToClass(AST.Print)
    def printTree(self, i):
        self.print_indent(i)
        print("PRINT")
        for printarg in self.printargs:
            # self.print_indent(1+i)
            # print(printarg)
            printarg.printTree(i+1)



    @addToClass(AST.String)
    def printTree(self, i):
        self.print_indent(i)
        print("STRING")
        self.print_indent(i+1)
        print(self.string)

    @addToClass(AST.IntNum)
    def printTree(self, i ):
        # self.print_indent(i)
        # print("INTNUM")
        # self.print_indent(i+1)s
        self.print_indent(i)
        print(self.intnum)


    @addToClass(AST.FloatNum)
    def printTree(self, i ):
        self.print_indent(i)
        print("FLOATNUM")
        self.print_indent(i+1)
        print(self.floatnum)


    @addToClass(AST.Variable)
    def printTree(self, i):

        if self.index is not None:
            self.print_indent(i)
            print("REF")
            self.id.printTree(i+1)


            for e in self.index:
                # self.print_indent(i+2)
                if isinstance(e, tuple):
                    self.print_indent(i + 1)
                    print(":")
                    e[0].printTree(i+1)


                    e[1].printTree(i+1)
                else:
                    e.printTree(i+1)


    @addToClass(AST.Id)
    def printTree(self, i):
        self.print_indent(i)
        print(self.id)

    @addToClass(AST.BinExpr)
    def printTree(self, i):
        self.print_indent(i)
        print(self.op)
        self.left.printTree(i+1)
        self.right.printTree(i+1)


    @addToClass(AST.Uminus)
    def printTree(self, i):
        self.print_indent(i)
        print("-")
        self.val.printTree(i+1)

    @addToClass(AST.Uneg)
    def printTree(self, i):
        self.print_indent(i)
        print("NOT")
        self.val.printTree(i + 1)

    @addToClass(AST.Transpose)
    def printTree(self, i):
        self.print_indent(i)
        print("TRANSPOSE")
        self.val.printTree(i + 1)

    @addToClass(AST.Unary)
    def printTree(self, i):
        self.print_indent(i)
        print(self.operation)
        self.expr.printTree(i+1)


    @addToClass(AST.Matrix)
    def printTree(self, i):
        self.print_indent(i)
        print("VECTOR")
        for row in self.matrix:
            row.printTree(i + 1)


    @addToClass(AST.Vector)
    def printTree(self, i):
        self.print_indent(i)
        print("VECTOR")
        for expr in self.vector:
            expr.printTree(i + 1)


    @addToClass(AST.MatrixFunc)
    def printTree(self, i):
        self.print_indent(i)
        print(self.func)
        # print(self.expr)
        for el in self.dims:
            el.printTree(i+1)
        # self.expr.printTree(i+1)
