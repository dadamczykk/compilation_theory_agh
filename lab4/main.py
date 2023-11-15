from Mparser import MatrixParser
from lab1.scanner_oo import Scanner
from sly.lex import LexError
from TreePrinter import TreePrinter

import os

parser = MatrixParser()

if __name__ == "__main__":
    folder_path = 'tests'
    file_list = os.listdir(folder_path)
    for filename in file_list:
        # if filename != "test_1.txt": continue
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                file_contents = file.read()
                print(f'Testing {filename}:')
            try:
                TreePrinter()
                cos = parser.parse(Scanner().tokenize(file_contents))
                print(cos)
                if cos is not None:
                    cos.printTree(0)

            except LexError as e:
                print(f"Lexer error: {e}")