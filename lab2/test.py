from Mparser import MatrixParser
from lab1.scanner_oo import Scanner
from sly.lex import LexError
import os

parser = MatrixParser()

if __name__ == "__main__":
    folder_path = 'tests'
    file_list = os.listdir(folder_path)
    for filename in file_list:
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                file_contents = file.read()
                print(f'Testing {filename}:')
            try:
                parser.parse(Scanner().tokenize(file_contents))
            except LexError as e:
                print(f"Lexer error: {e}")