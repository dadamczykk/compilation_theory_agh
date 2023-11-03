from sly import Lexer

class Scanner(Lexer):
    tokens = {
        DOTPLUS, DOTMINUS, DOTMULTIPLY, DOTDIVIDE,
        PLUSASSIGN, MINUSASSIGN, MULTIPLYASSIGN, DIVIDEASSIGN,
        # PLUS, MINUS, MULTIPLY, DIVIDE, ASSIGN,
        LT, GT, LTE, GTE, EQ, NEQ,
        IF, ELSE, FOR, WHILE,
        AND, OR, XOR, NOT,
        BREAK, CONTINUE, RETURN,
        EYE, ZEROS, ONES,
        PRINT,
        ID,
        INTNUM,
        FLOATNUM,
        STRING
    }

    literals = {
                '+', '-', '*', '/',
                '=',
                '(', ')', '[', ']', '{', '}',
                ':',
                '\'',
                ';', ','}

    ignore = ' \t'
    ignore_comment = r'\#.*'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)



    FLOATNUM = r'((\d+\.(\d*)?|\.\d+)([eE][-+]?\d+)?|(\d+[eE][-+]?\d+))'
    INTNUM = r'(\d+)'
    STRING = r'\"[^\"]*\"'

    def FLOATNUM(self, t):
        t.value = float(t.value)
        return t

    def INTNUM(self, t):
        t.value = int(t.value)
        return t

    def STRING(self, t):
        t.value = str(t.value)[1:-1]

        return t


    DOTPLUS = r'\.\+'
    DOTMINUS = r'\.-'
    DOTMULTIPLY = r'\.\*'
    DOTDIVIDE = r'\./'

    PLUSASSIGN = r'\+='
    MINUSASSIGN = r'-='
    MULTIPLYASSIGN = r'\*='
    DIVIDEASSIGN = r'/='

    # PLUS = r'\+'
    # MINUS = r'-'
    # MULTIPLY = r'\*'
    # DIVIDE = r'/'
    # ASSIGN = r'='

    LTE = r'<='
    GTE = r'>='
    EQ = r'=='
    NEQ = r'!='
    LT = r'<'
    GT = r'>'


    ID = r'[A-Za-z_][A-Za-z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['for'] = FOR
    ID['while'] = WHILE
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID['return'] = RETURN
    ID['eye'] = EYE
    ID['zeros'] = ZEROS
    ID['ones'] = ONES
    ID['print'] = PRINT
    ID['and'] = AND
    ID['or'] = OR
    ID['xor'] = XOR
    ID['not'] = NOT

    def error(self, t):
        print(f"({t.lineno}) illegal character '{t.value[0]}'")
        self.index += 1
