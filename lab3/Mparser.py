from lab1.scanner_oo import Scanner
from sly import Parser
import AST


def print_error(p, message):
    p = p.error
    print("Syntax error in {0}, at line {1}: LexToken({2}, '{3}')".format(message, p.lineno, p.type, p.value))


class MatrixParser(Parser):
    tokens = Scanner.tokens
    debugfile = 'parser.out'

    # Priorytety operacji
    precedence = (

        ('right', IFX),
        ('right', ELSE),
        ('left', AND, OR, XOR),
        ('right', "=", MULTIPLYASSIGN, DIVIDEASSIGN, MINUSASSIGN, PLUSASSIGN),
        ('left', "+", "-"),
        ('left', "*", "/"),
        ('left', DOTPLUS, DOTMINUS),
        ('left', DOTMULTIPLY, DOTDIVIDE),
        ('nonassoc', LTE, GTE, EQ, NEQ, LT, GT),
        ('left', "\'"),
        ('right', UNEG, UMINUS),

    )

    start = 'program'

    @_('instructions_or_empty')
    def program(self, p):
        return AST.InstrOrEmpty(p[0])

    @_('instructions')
    def instructions_or_empty(self, p):
        return AST.Instructions(p[0])

    @_('')
    def instructions_or_empty(self, p):
        return AST.Instructions()

    @_('instructions instruction',
       'instruction')
    def instructions(self, p):
        # print("p0", p[0])
        # if len(p) > 1: print("p1", p[1])

        return p[0] + [p[1]] if len(p) == 2 else [p[0]]

    @_('if_i',
       'return_i ";"',
       'BREAK ";"',
       'CONTINUE ";"',
       'for_l',
       'while_l',
       'assign ";"',
       'print_i ";"')
    def instruction(self, p):
        return p[0]

    @_('"{" instructions "}"')
    def instruction(self, p):
        return p[1][0]

    @_('IF "(" expr ")" instruction %prec IFX',
       'IF "(" expr ")" instruction ELSE instruction')
    def if_i(self, p):
        return AST.If(p[2], p[4]) if len(p) == 5 else AST.If(p[2], p[4], p[6])

    @_('IF "(" error ")" instruction %prec IFX',
       'IF "(" error ")" instruction ELSE instruction',
       'IF "(" expr ")" error %prec IFX',
       'IF "(" expr ")" error ELSE instruction',
       'IF "(" expr ")" instruction ELSE error')
    def if_i(self, p):
        print_error(p, "if statement")

    @_('WHILE "(" expr ")" instruction')
    def while_l(self, p):
        return AST.While(p[2], p[4])

    @_('WHILE "(" error ")" instruction',
       'WHILE "(" expr ")" error')
    def while_l(self, p):
        print_error(p, "while loop")

    @_('FOR ID "=" expr ":" expr instruction')
    def for_l(self, p):
        return AST.For(AST.Id(p[1]), p[3], p[5], p[6])

    @_('FOR ID "=" error ":" expr instruction',
       'FOR ID "=" expr ":" error instruction',
       'FOR ID "=" expr ":" expr error')
    def for_l(self, p):
        print_error(p, "for loop")

    @_('RETURN',
       'RETURN expr')
    def return_i(self, p):
        return AST.Return(p[1]) if len(p) == 2 else AST.Return()

    @_('RETURN error')
    def return_i(self, p):
        print_error(p, "return statement")

    @_('PRINT printargs')
    def print_i(self, p):
        return AST.Print(p[1])

    @_('PRINT error')
    def print_i(self, p):
        print_error(p, "print function")

    @_('expr "," printargs',
       'expr')
    def printargs(self, p):
        return [p[0]] + p[2] if len(p) == 3 else [p[0]]


    @_('STRING')
    def expr(self, p):
        return AST.String(p[0])

    @_('INTNUM')
    def expr(self, p):
        return AST.IntNum(p[0])

    @_('FLOATNUM')
    def expr(self, p):
        return AST.FloatNum(p[0])

    @_('var')
    def expr(self, p):
        return p[0]
    @_('"(" expr ")"')
    def expr(self, p):
        return p[1]

    @_('matel')
    def var(self, p):
        return p[0]

    @_('ID')
    def var(self, p):
        return AST.Id(p[0])

    @_('ID "[" expr "," expr "]"')
    def matel(self, p):
        return AST.Variable(AST.Id(p[0]), (p[2], p[4]))

    @_('var "=" expr',
       'var PLUSASSIGN expr',
       'var MINUSASSIGN expr',
       'var MULTIPLYASSIGN expr',
       'var DIVIDEASSIGN expr')
    def assign(self, p):
        return AST.AssignOp(p[0], p[1], p[2])

    @_('var "=" error',
       'var PLUSASSIGN error',
       'var MINUSASSIGN error',
       'var MULTIPLYASSIGN error',
       'var DIVIDEASSIGN error')
    def assign(self, p):
        print_error(p, "assigment")


    @_("unary")
    def expr(self, p):
        return p[0]


    @_('"-" expr %prec UMINUS')
    def unary(self, p):
        return AST.Unary("UMINUS", p[1])

    @_('NOT expr %prec UNEG')
    def unary(self, p):
        return AST.Unary("UNEG", p[1])

    @_('expr "\'"')
    def unary(self, p):
        print(p[0])
        return AST.Unary("TRANSPOSE", p[0])

    @_('matrix')
    def expr(self, p):
        return p[0]


    @_('expr "+" expr',
       'expr "-" expr',
       'expr "*" expr',
       'expr "/" expr',

       'expr EQ expr',
       'expr NEQ expr',
       'expr LT expr',
       'expr GT expr',
       'expr LTE expr',
       'expr GTE expr',

       'expr XOR expr',
       'expr AND expr',
       'expr OR expr',

       'expr DOTMULTIPLY expr',
       'expr DOTDIVIDE expr',
       'expr DOTPLUS expr',
       'expr DOTMINUS expr')
    def expr(self, p):
        return AST.BinExpr(p[0], p[1], p[2])



    @_('"[" vectors "]"')
    def matrix(self, p):
        return AST.Matrix(p[1])

    @_('vectors "," vector',
       'vector')
    def vectors(self, p):
        return p[0] + [p[2]] if len(p) == 3 else [p[0]]

    @_('"[" variables "]"')
    def vector(self, p):
        return p[1]

    @_('variables "," variable',
       'variable')
    def variables(self, p):
        return  p[0] + [p[2]] if len(p) == 3 else [p[0]]

    @_('expr')
    def variable(self, p):
        return p[0]

    @_('mat_fun "(" expr ")"')
    def expr(self, p):
        return AST.MatrixFunc(p[0], p[2])

    @_('mat_fun "(" error ")"')
    def expr(self, p):
        print_error(p, "matrix function")

    @_('ZEROS',
       'EYE',
       'ONES')
    def mat_fun(self, p):
        return p[0]

    # def error(self, p):
    #     if p:
    #         print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    #     else:
    #         print("Unexpected end of input")
