from sly import Lexer
# TO DO
# zrobić to ładniej (o ile się da)
# poprawić regexa do liczb float
# zrobić może jakieś testy czy to w ogóle działa tak jak ma działać


class Scanner(Lexer):
    tokens = {
    DOTPLUS, DOTMINUS, DOTMULTIPLY, DOTDIVIDE,
    PLUSASSIGN, MINUSASSIGN, MULTIPLYASSIGN,  DIVIDEASSIGN,
    LT, GT, LTE, GTE, EQ, NEQ,
    IF, ELSE, FOR, WHILE,
    BREAK, CONTINUE, RETURN,
    EYE, ZEROS, ONES,
    PRINT,
    ID,
    INTNUM,
    FLOATNUM,
    STRING
    }
    
    literals = {'+', '-', '*', '/',
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
    
    INTNUM= r'[1-9]\d*'
    FLOATNUM= r'\d*\.\d*'
    STRING= r'\"[^\"]*\"'
    
    DOTPLUS= r'\.\+'
    DOTMINUS= r'\.-'
    DOTMULTIPLY= r'\.\*'
    DOTDIVIDE= r'\./'
    
    PLUSASSIGN= r'\+='
    MINUSASSIGN= r'-='
    MULTIPLYASSIGN= r'\*='
    DIVIDEASSIGN= r'/='
    
    LT= r'<'
    GT= r'>'
    LTE= r'<='
    GTE= r'>='
    EQ= r'=='
    NEQ= r'!='
    
    ID= r'[A-Za-z_][A-Za-z0-9_]*'
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
    
    def error(self, t):
        print(f"({t.lineno}) illegal character '{t.value[0]}'")
        self.index += 1
