from sly import Lexer



class Scanner(Lexer):
    tokens = {
    ID,
    INTNUM, FLOATNUM, STRING,
    PLUS, MINUS, MULTIPLY,  DIVIDE, DOTPLUS, DOTMINUS, DOTMULTIPLY, DOTDIVIDE,  ASSIGN, PLUSASSIGN, MINUSASSIGN, MULTIPLYASSIGN,  DIVIDEASSIGN, LT, GT, LTE, GTE, EQ, NEQ, LPAREN,  RPAREN, LBRACKET, RBRACKET, LBRACE, RBRACE, COLON,  TRANSPOSE, COMA, SEMICOLON, IF, ELSE, FOR, WHILE,  BREAK, CONTINUE, RETURN, EYE, ZEROS, ONES, PRINT
    }
    
    
    ignore = ' \t'
    ignore_comment = r'\#.*'
    # ignore_newline = r'\n+'
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)
    
    ID= r'[A-Za-z_][A-Za-z0-9_]*'
    INTNUM= r'[1-9]\d*'
    FLOATNUM= r'\d+\.\d+'
    STRING= r'\"[^\"]*\"'
    
    PLUS= r'\+'
    MINUS= r'-'
    MULTIPLY= r'\*'
    DIVIDE= r'/'
    DOTPLUS= r'\.\+'
    DOTMINUS= r'\.-'
    DOTMULTIPLY= r'\.\*'
    DOTDIVIDE= r'\./'
    ASSIGN= r'='
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
    LPAREN= r'\('
    RPAREN= r'\)'
    LBRACKET= r'\['
    RBRACKET= r'\]'
    LBRACE= r'\{'
    RBRACE= r'\}'
    COLON= r':'
    TRANSPOSE= r'\''
    COMA= r','
    SEMICOLON= r';'
    IF= r'if'
    ELSE= r'else'
    FOR= r'for'
    WHILE= r'while'
    BREAK= r'break'
    CONTINUE= r'continue'
    RETURN= r'return'
    EYE= r'eye'
    # ZEROS= r'zeros'
    ID['zeros'] = ZEROS
    ONES= r'ones'
    PRINT= r'print'
