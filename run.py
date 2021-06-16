from lexical_analyzer import LexicalAnalyzer
from syntactic_analyzer import SyntacticAnalyzer
import sys

# if __name__ == '__main__':
print("Iniciando analisador lexico...\n")
lexical = LexicalAnalyzer()
lexical.start()
print("Iniciando analisador sintatico...\n")
SyntacticAnalyzer()


