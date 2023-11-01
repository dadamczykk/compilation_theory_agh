from lab1.scanner_oo import Scanner
from sly import Parser


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
        ('left', "+", "-"),
        ('left', "*", "/"),
        ('left', DOTPLUS, DOTMINUS),
        ('left', DOTMULTIPLY, DOTDIVIDE),
        ('nonassoc', LTE, GTE, EQ, NEQ, LT, GT),
        # ('left', TRANSPOSE),
        ('right', UNEG, UMINUS),

    )

    start = 'program'

    @_('instructions_or_empty')
    def program(self, p):
        return p

    @_('instructions')
    def instructions_or_empty(self, p):
        return p

    @_('')
    def instructions_or_empty(self, p):
        return p

    @_('instructions instruction',
       'instruction')
    def instructions(self, p):
        return p

    @_('if_i',
       'return_i ";"',
       'BREAK ";"',
       'CONTINUE ";"',
       'for_l',
       'while_l',
       'assign ";"',
       'print_i ";"',
       '"{" instructions "}"')
    def instruction(self, p):
        return p

    @_('IF "(" expr ")" instruction %prec IFX',
       'IF "(" expr ")" instruction ELSE instruction')
    def if_i(self, p):
        return p

    @_('IF "(" error ")" instruction %prec IFX',
       'IF "(" error ")" instruction ELSE instruction',
       'IF "(" expr ")" error %prec IFX',
       'IF "(" expr ")" error ELSE instruction',
       'IF "(" expr ")" instruction ELSE error')
    def if_i(self, p):
        print_error(p, "if statement")
    @_('WHILE "(" expr ")" instruction')
    def while_l(self, p):
        return p

    @_('WHILE "(" error ")" instruction',
       'WHILE "(" expr ")" error')
    def while_l(self, p):
        print_error(p, "while loop")

    @_('FOR ID "=" expr ":" expr instruction',)
    def for_l(self, p):
        return p

    @_('FOR ID "=" error ":" expr instruction',
       'FOR ID "=" expr ":" error instruction',
       'FOR ID "=" expr ":" expr error')
    def for_l(self, p):
        print_error("for loop")

    @_('RETURN',
       'RETURN expr')
    def return_i(self, p):
        return p

    @_('RETURN error')
    def return_i(self, p):
        print_error("return statement")


    @_('PRINT printargs')
    def print_i(self, p):
        return p

    @_('PRINT error')
    def print_i(self, p):
        print_error(p, "print function")

    @_('expr "," printargs',
       'expr')
    def printargs(self, p):
        return p

    @_('var',
       '"(" expr ")"',
       'INTNUM',
       'FLOATNUM',
       'STRING')
    def expr(self, p):
        return p

    @_('ID',
       'matel')
    def var(self, p):
        return p

    @_('ID "[" expr "," expr "]"')
    def matel(self, p):
        return p

    @_('var "=" expr',
       'var PLUSASSIGN expr',
       'var MINUSASSIGN expr',
       'var MULTIPLYASSIGN expr',
       'var DIVIDEASSIGN expr')
    def assign(self, p):
        return p

    @_('var "=" error',
       'var PLUSASSIGN error',
       'var MINUSASSIGN error',
       'var MULTIPLYASSIGN error',
       'var DIVIDEASSIGN error')
    def assign(self, p):
        print_error(p, "assigment")

    @_('"-" expr %prec UMINUS',
       'NOT expr %prec UNEG',
       '''expr "'"''')
    def expr(self, p):
        return p  # -p.expr

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
       'expr DOTMINUS expr',
       )
    def expr(self, p):
        return p
    @_('matrix')
    def expr(self, p):
        return p

    @_('"[" vectors "]"')
    def matrix(self, p):
        return p

    @_('vectors "," vector',
       'vector')
    def vectors(self, p):
        return p

    @_('"[" variables "]"')
    def vector(self, p):
        return p

    @_('variables "," variable',
       'variable')
    def variables(self, p):
        return p

    @_('expr')
    def variable(self, p):
        return p

    @_('mat_fun "(" expr ")"')
    def expr(self, p):
        return p

    @_('mat_fun "(" error ")"')
    def expr(self, p):
        print_error(p, "matrix function")

    @_('ZEROS',
       'EYE',
       'ONES')
    def mat_fun(self, p):
        return p

    # def error(self, p):
    #     if p:
    #         print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    #     else:
    #         print("Unexpected end of input")


