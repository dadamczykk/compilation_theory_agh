from Mparser import MatrixParser
from lab1.scanner_oo import Scanner
from sly.lex import LexError
from TreePrinter import TreePrinter
from lab4.TypeChecker import TypeChecker
import os



if __name__ == "__main__":
    folder_path = 'tests'
    file_list = os.listdir(folder_path)
    for filename in file_list:
        if filename != "test_2.txt": continue
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                file_contents = file.read()
                print(f'Testing {filename}:')
            try:
                TreePrinter()
                parser = MatrixParser()
                typeChecker = TypeChecker()
                cos = parser.parse(Scanner().tokenize(file_contents))
                # print(cos)
                if cos is not None:
                    cos.printTree(0)
                    typeChecker.visit(cos)

            except LexError as e:
                print(f"Lexer error: {e}")