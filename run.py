from syntactic_analyzer import SyntacticAnalyzer
from lexical_analyzer import LexicalAnalyzer
import sys

if __name__ == '__main__':
	print("Iniciando analisador lexico...\n")
	lexical = LexicalAnalyzer()
	print("Análisador lexico finalizou.\n")
	lexical.start()
	print("Iniciando analisador sintatico...\n")
	syntatic = SyntacticAnalyzer()
	print("Analisador sintatico finalizou....\n")
	sys.exit()

