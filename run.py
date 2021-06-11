from syntactic_analyzer import SyntacticAnalyzer
from lexical_analyzer import LexicalAnalyzer
from semantic_analyzer import SemanticAnalyzer
import sys

if __name__ == '__main__':
	print("Iniciando analisador lexico...\n")
	lexical = LexicalAnalyzer()
	lexical.start()
	print("Análisador lexico finalizou.\n")
	print("Iniciando analisador sintatico...\n")
	syntatic = SyntacticAnalyzer()
	print("Analisador sintatico finalizou....\n")
	print("Iniciando analisador semantico...\n")
	semantic = SemanticAnalyzer()
	print("Analisador semantico finalizou....\n")
	sys.exit()

