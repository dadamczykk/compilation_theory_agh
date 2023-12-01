from collections import defaultdict
import AST
from SymbolTable import SymbolTable, VariableSymbol

dict_of_types = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: "")))

dict_of_types["+"]["int"]["int"] = "int"
dict_of_types["+"]["int"]["float"] = "float"
dict_of_types["+"]["float"]["int"] = "float"
dict_of_types["+"]["float"]["float"] = "float"
dict_of_types["+"]["str"]["str"] = "str"
dict_of_types["+"]["vector"]["vector"] = "vector"

dict_of_types["-"]["int"]["int"] = "int"
dict_of_types["-"]["int"]["float"] = "float"
dict_of_types["-"]["float"]["int"] = "float"
dict_of_types["-"]["float"]["float"] = "float"
dict_of_types["-"]["str"]["str"] = "str"
dict_of_types["-"]["vector"]["vector"] = "vector"

dict_of_types["*"]["int"]["int"] = "int"
dict_of_types["*"]["int"]["float"] = "float"
dict_of_types["*"]["float"]["int"] = "float"
dict_of_types["*"]["float"]["float"] = "float"
dict_of_types["*"]["str"]["str"] = "str"
dict_of_types["*"]["vector"]["vector"] = "vector"

dict_of_types["/"]["int"]["int"] = "int"
dict_of_types["/"]["int"]["float"] = "float"
dict_of_types["/"]["float"]["int"] = "float"
dict_of_types["/"]["float"]["float"] = "float"
dict_of_types["/"]["vector"]["vector"] = "vector"


dict_of_types[">"]["int"]["int"] = "bool"
dict_of_types[">"]["int"]["float"] = "bool"
dict_of_types[">"]["float"]["int"] = "bool"
dict_of_types[">"]["float"]["float"] = "bool"

dict_of_types["<"]["int"]["int"] = "bool"
dict_of_types["<"]["int"]["float"] = "bool"
dict_of_types["<"]["float"]["int"] = "bool"
dict_of_types["<"]["float"]["float"] = "bool"

dict_of_types[">="]["int"]["int"] = "bool"
dict_of_types[">="]["int"]["float"] = "bool"
dict_of_types[">="]["float"]["int"] = "bool"
dict_of_types[">="]["float"]["float"] = "bool"

dict_of_types["<="]["int"]["int"] = "bool"
dict_of_types["<="]["int"]["float"] = "bool"
dict_of_types["<="]["float"]["int"] = "bool"
dict_of_types["<="]["float"]["float"] = "bool"

dict_of_types["=="]["int"]["int"] = "bool"
dict_of_types["=="]["int"]["float"] = "bool"
dict_of_types["=="]["float"]["int"] = "bool"
dict_of_types["=="]["float"]["float"] = "bool"

dict_of_types["!="]["int"]["int"] = "bool"
dict_of_types["!="]["int"]["float"] = "bool"
dict_of_types["!="]["float"]["int"] = "bool"
dict_of_types["!="]["float"]["float"] = "bool"

dict_of_types[".+"]["vector"]["vector"] = "vector"
dict_of_types[".-"]["vector"]["vector"] = "vector"
dict_of_types[".*"]["vector"]["vector"] = "vector"
dict_of_types["./"]["vector"]["vector"] = "vector"

dict_of_types["+="]["int"]["int"] = "int"
dict_of_types["+="]["int"]["float"] = "float"
dict_of_types["+="]["float"]["int"] = "float"
dict_of_types["+="]["float"]["float"] = "float"
dict_of_types["+="]["str"]["str"] = "str"
dict_of_types["+="]["vector"]["vector"] = "vector"

dict_of_types["-="]["int"]["int"] = "int"
dict_of_types["-="]["int"]["float"] = "float"
dict_of_types["-="]["float"]["int"] = "float"
dict_of_types["-="]["float"]["float"] = "float"
dict_of_types["-="]["str"]["str"] = "str"
dict_of_types["-="]["vector"]["vector"] = "vector"

dict_of_types["*="]["int"]["int"] = "int"
dict_of_types["*="]["int"]["float"] = "float"
dict_of_types["*="]["float"]["int"] = "float"
dict_of_types["*="]["float"]["float"] = "float"
dict_of_types["*="]["str"]["str"] = "str"
dict_of_types["*="]["vector"]["vector"] = "vector"

dict_of_types["/="]["int"]["int"] = "int"
dict_of_types["/="]["int"]["float"] = "float"
dict_of_types["/="]["float"]["int"] = "float"
dict_of_types["/="]["float"]["float"] = "float"
dict_of_types["/="]["vector"]["vector"] = "vector"



class NodeVisitor(object):
    def __init__(self):
        self.symbol_table = SymbolTable(None, "global")
        self.current_scope = self.symbol_table
        self.loop_indent = 0

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

class TypeChecker(NodeVisitor):

    def visit_InstrOrEmpty(self, node: AST.InstrOrEmpty):
        self.visit(node.instructions)
        # print(self.symbol_table.symbols)

    def visit_Instructions(self, node: AST.Instructions):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_Id(self, node: AST.Id):
        return self.symbol_table.get(node.id)
        pass

    def visit_BinExpr(self, node: AST.BinExpr):
        node.v_type = 'float'
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        if dict_of_types[op][type1][type2] == "":
            print(f"{node.lineno} Type error: {type1} {op} {type2} is not correct")
            return None


        if type1 == "vector" or type2 == "vector":
            was_l_tr = was_r_tr = False
            if isinstance(node.left, AST.Unary):
                if node.left.operation == "TRANSPOSE":
                    was_l_tr = True
                node.left = node.left.expr
            if isinstance(node.right, AST.Unary):
                if node.right.operation == "TRANSPOSE":
                    was_r_tr = True
                node.right = node.right.expr

            if isinstance(node.left, AST.Id):
                left_dims = self.symbol_table.get_v_dims(node.left.id)
                node.v_type = self.symbol_table.get_v_type(node.left.id)
            elif isinstance(node.left, AST.BinExpr):
                left_dims = node.left.dims
                # 5 + (3 - 2 + 1)
            elif isinstance(node.left, AST.Vector):
                left_dims = node.left.dims
            else:
                print("Error in visit_BinExpr")
                print(node.left)
                exit()
            if was_l_tr:
                left_dims = left_dims[::-1]

            if isinstance(node.right, AST.Id):
                right_dims = self.symbol_table.get_v_dims(node.right.id)
                node.v_type = self.symbol_table.get_v_type(node.left.id)
            elif isinstance(node.right, AST.BinExpr):
                right_dims = node.right.dims
                # 5 + (3 - 2 + 1)
            elif isinstance(node.right, AST.Vector):
                right_dims = node.right.dims
            else:
                print("Error in visit_BinExpr")
                print(node.left, node.right)
                exit()
            if was_r_tr:
                right_dims = right_dims[::-1]

            # print(left_dims, right_dims)
            # print(node.left.dims)
            # print()
            # print(node.lineno, left_dims, right_dims)
            if len(right_dims) != len(left_dims):
                print(f"{node.lineno} Nonequal vector dim")
                return None

            for i in range(len(right_dims)):
                if isinstance(left_dims[i], AST.IntNum):
                    ldi = left_dims[i].intnum
                else:
                    ldi = left_dims[i]
                if isinstance(right_dims[i], AST.IntNum):
                    rdi = right_dims[i].intnum
                else:
                    rdi = right_dims[i]

                if ldi != rdi:
                    # print(left_dims[i], right_dims[i])
                    print(f"{node.lineno} Nonequal vector dim")
                    return None
            node.dims = left_dims
        return dict_of_types[op][type1][type2]


    def visit_If(self, node: AST.If):
        self.symbol_table = self.symbol_table.pushScope("if")

        self.visit(node.cond)
        self.visit(node.if_body)
        self.symbol_table = self.symbol_table.popScope()
        if node.else_body is not None:
            self.symbol_table = self.symbol_table.pushScope("else")
            self.visit(node.else_body)
            self.symbol_table = self.symbol_table.popScope()

    def visit_Return(self, node: AST.Return):
        return self.visit(node.expr)

    def visit_Break(self, node: AST.Break):
        if self.loop_indent == 0:
            print(f"{node.lineno} Break shouldn't be here")

    def visit_Continue(self, node: AST.Continue):
        if self.loop_indent == 0:
            print(f"{node.lineno} Continue shouldn't be here")

    def visit_For(self, node:AST.For):
        self.symbol_table = self.symbol_table.pushScope('for')
        self.loop_indent += 1
        t1 = self.visit(node.cond_start)
        t2 = self.visit(node.cond_end)

        if t1 is None or t2 is None or t1 != t2:
            print(f"{node.lineno} something wrong with operand types")
            self.symbol_table.put(node.id, None)

        else:
            if isinstance(node.id, AST.Id):
                self.symbol_table.put(node.id.id, t1)
            else:
                self.symbol_table.put(node.id, t1)

        self.visit(node.body)
        self.symbol_table = self.symbol_table.popScope()
        self.loop_indent -= 1

    def visit_While(self, node: AST.While):
        self.symbol_table = self.symbol_table.pushScope("while")
        self.loop_indent += 1
        self.visit(node.cond)
        self.visit(node.body)
        self.symbol_table = self.symbol_table.popScope()
        self.loop_indent -= 1

    def visit_AssignOp(self, node: AST.AssignOp):
        # print(node)
        # for now idk how to do it
        val_type = self.visit(node.right)
        if val_type is None:
            #PRINT
            return None
        left_id = node.left.id
        if node.op == '=':
            if isinstance(left_id, str):
                self.symbol_table.put(left_id, val_type)
            else:
                self.symbol_table.put(left_id.id, val_type)

            if val_type == 'vector':
                if isinstance(node.right, AST.Unary):
                    self.symbol_table.v_dims[left_id] = node.right.expr.dims[::-1]
                    self.symbol_table.v_type[left_id] = node.right.expr.v_type
                elif isinstance(node.right.dims, AST.IntNum):
                    # print(node.right)
                    self.symbol_table.v_dims[left_id] = node.right.dims.intnum
                    self.symbol_table.v_type[left_id] = node.right.v_type
                else:
                    self.symbol_table.v_dims[left_id] = node.right.dims
                    self.symbol_table.v_type[left_id] = node.right.v_type
        else:
            var_type = self.symbol_table.get(left_id)
            if var_type == 'vector' and val_type == 'vector':
                var_d = self.symbol_table.v_dims[left_id]
                val_d = node.right.dims

                if len(var_d) != len(val_d):
                    print(f"{node.lineno} wrong dimensions")
                    return None

                for i in range(len(var_d)):
                    if var_d[i] != val_d[i]:
                        print(f"{node.lineno} wrong dimensions")
                        return None

            if dict_of_types[node.op][var_type][val_type] != '':
                return dict_of_types[node.op][var_type][val_type]
            else:
                print(f"{node.lineno} operation on given values is not defined")
                return None

        pass

    def visit_Vector(self, node: AST.Vector):

        # print(node)
        if isinstance(node.vector[0], AST.Vector):
            d = node.vector[0].dims
        elif isinstance(node.vector[0], list):
            d = [len(node.vector[0])]
        else:
            d = [1]
# MOŻNA FORALL
        for e in node.vector:
            if isinstance(e, AST.Vector):
                self.visit(e)
                ed = e.dims
            elif isinstance(e, list):
                ed = [len(e)]
            else:
                ed = [1]

            for i in range(len(d)):
                if d[i] != ed[i]:
                    print(f"{node.lineno} Wrong vector size")
                    return None
        return 'vector'
    def visit_Print(self, node: AST.Print):
        for i in node.printargs:
            self.visit(i)

    def visit_String(self, node: AST.String):
        return 'str'

    def visit_IntNum(self, node: AST.IntNum):
        return 'int'

    def visit_FloatNum(self, node: AST.FloatNum):
        return 'float'

    def visit_Variable(self, node: AST.Variable):
        if node.id.id not in self.symbol_table.v_dims:
            print(f"{node.lineno} id not specified earlier")
            return None
        dims = self.symbol_table.v_dims[node.id.id]

        if len(dims) != len(node.index):
            print(f"{node.lineno} Vector sizes not good")
            return None

        # print(node.index)
        # print(dims)
        for i in range(len(node.index)):
            if isinstance(node.index[i], tuple):
                if self.visit(node.index[i][0]) != 'int' or self.visit(node.index[i][1]) != 'int':
                    print(f"{node.lineno} Vector index must be int")
                    return None
                if node.index[i][0].intnum >= dims[i].intnum or node.index[i][1].intnum >= dims[i].intnum:
                    print(f"{node.lineno} Index out of bounds")
                    return None

                if node.index[i][0].intnum >= node.index[i][1].intnum:
                    print(f"{node.lineno} Index wrong soemthing lmfao")
                    return None
            else:
                if self.visit(node.index[i]) != 'int':
                    print(f"{node.lineno} Vector index must be int")
                    return None

                if node.index[i].intnum >= dims[i].intnum:
                    print(f"{node.lineno} Index out of bounds")
                    return None
        return self.symbol_table.v_type[node.id.id]

    def visit_Unary(self, node: AST.Unary):
        # if node.operation == 'TRANSPOSE':
            # if isinstance(node.expr, AST.Id):
            #     self.symbol_table.v_dims[node.expr.id] = self.symbol_table.v_dims[node.expr.id][::-1]

        return self.visit(node.expr)

    def visit_MatrixFunc(self, node: AST.MatrixFunc):
        for el in node.dims:
            if self.visit(el) != 'int':
                print(f"{node.lineno} matrix function takes int")
                return None

        return 'vector'

