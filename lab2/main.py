from Mparser import MatrixParser
from lab1.scanner_oo import Scanner
from sly.lex import LexError

parser = MatrixParser()

if __name__ == "__main__":
    with open("text.txt", "r") as infile:
        source_code = infile.read()
        infile.close()

    try:
        parser.parse(Scanner().tokenize(source_code))
    except LexError as e:
        print(f"Lexer error: {e}")