from lab1.scanner_oo import Scanner
from sly import Parser
from sly.lex import LexError


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
        ('right',  FOR, WHILE),

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
        return p  #-p.expr



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


# Inicjalizacja parsera
parser = MatrixParser()

# Przykładowy kod do analizy
source_code = """# control flow instruction

N = 10;
M = 20;

if(N==10)
    print "N==10";
else if(N!=10)
    print "N!=10";


if(N>5) {
    print "N>5";
}
else if(N>=0) {
    print "N>=0";
}

if(N<10) {
    print "N<10";
}
else if(N<=15)
    print "N<=15";

k = 10;
while(k>0)
    k = k - 1;

while(k>0) {
    if(k<5)
        i = 1;
    else if(k<10)
        i = 2;   
    else
        i = 3;
    
    k = k - 1;
}


for i = 1:N
  for j = i:M
    print i, j;
 

for i = 1:N {
    if(i<=N/16)
        print i;
    else if(i<=N/8)
        break;
    else if(i<=N/4)
        continue;
    else if(i<=N/2)
        return 0;
}


{
  N = 100;
  M = 200;  
  
  
  # assignment operators
# binary operators
# transposition

C = -A;     # assignemnt with unary expression
C = B' ;    # assignemnt with matrix transpose
C = A+B ;   # assignemnt with binary addition
C = A-B ;   # assignemnt with binary substraction
C = A*B ;   # assignemnt with binary multiplication
C = A/B ;   # assignemnt with binary division
C = A.+B ;  # add element-wise A to B
C = A.-B ;  # substract B from A 
C = A.*B ;  # multiply element-wise A with B
C = A./B ;  # divide element-wise A by B

C += B ;  # add B to C 
C -= B ;  # substract B from C 
C *= A ;  # multiply A with C
C /= A ;  # divide A by C


# special functions, initializations

A = zeros(5);  # create 5x5 matrix filled with zeros
B = ones(7);   # create 7x7 matrix filled with ones
I = eye(10);   # create 10x10 matrix filled with ones on diagonal and zeros elsewhere

# initialize 3x3 matrix with specific values
E1 = [ [1, 2, 3],
       [4, 5, 6],
       [7, 8, 9] ]] ;

A[1,3] = 0 ;

x = 2;
y = 2.5;
}"""

# Analiza kodu źródłowego
try:
    parser.parse(Scanner().tokenize(source_code))
except LexError as e:
    print(f"Lexer error: {e}")
