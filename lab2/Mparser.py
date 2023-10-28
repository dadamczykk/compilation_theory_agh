from lab1.scanner_oo import Scanner
from sly import Parser


class MatrixParser(Parser):
    tokens = Scanner.tokens
    debugfile = 'parser.out'

    # Priorytety operacji
    precedence = (
        # ('right', "(", ")"),
        ('right', IFX),
        ('right', ELSE),
        # ('right', "{", "}", "[", "]"),
        #
        ('right', FOR, WHILE),

        ('left', "+", "-"),
        ('left', "*", "/"),
        ('left', DOTPLUS, DOTMINUS),
        ('left', DOTMULTIPLY, DOTDIVIDE),

        ('left', "=", PLUSASSIGN, MINUSASSIGN, MULTIPLYASSIGN, DIVIDEASSIGN),
        ('left', AND, OR, XOR),
        ('nonassoc', LTE, GTE, EQ, NEQ, LT, GT),

        ('left', TRANSPOSE),
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

    @_('WHILE "(" expr ")" instruction',
       )
    def while_l(self, p):
        return p

    @_('FOR ID "=" expr ":" expr instruction')
    def for_l(self, p):
        return p

    @_('RETURN',
       'RETURN expr')
    def return_i(self, p):
        return p

    @_('PRINT printargs')
    def print_i(self, p):
        return p

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

    @_('"-" expr %prec UMINUS',
       'NOT expr %prec UNEG',
       '''expr "'" %prec TRANSPOSE''')
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

    @_('ZEROS',
       'EYE',
       'ONES')
    def mat_fun(self, p):
        return p

    def error(self, p):
        if p:
            print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
        else:
            print("Unexpected end of input")
