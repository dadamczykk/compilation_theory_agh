#object oriented version

import sys
import scanner_oo  # scanner_oo.py is a file you create, (it is not an external library)


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example_full.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = scanner_oo.Scanner()
    # lexer.build()

    
    # Give the lexer some input
    # lexer.input(text)

    # Tokenize
    for tok in lexer.tokenize(text):
        print(f'({tok.lineno}): {tok.type}({tok.value})')
