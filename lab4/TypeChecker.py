from collections import defaultdict
import AST

super_huge_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: "")))

super_huge_dict["+"]["int"]["int"] = "int"
super_huge_dict["+"]["int"]["float"] = "float"
super_huge_dict["+"]["float"]["int"] = "float"
super_huge_dict["+"]["float"]["float"] = "float"
super_huge_dict["+"][""]

class NodeVisitor(object):

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

    def visit_BinExpr(self, node):
        # alternative usage,
        # requires definition of accept method in class Node
        type1 = self.visit(node.left)  # type1 = node.left.accept(self)
        type2 = self.visit(node.right)  # type2 = node.right.accept(self)
        op = node.op
        # ...
        #

    def visit_Variable(self, node):
        pass


