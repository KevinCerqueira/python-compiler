# Authors: 
# Esdras Abreu (@EsdrasAbreu)
# Kevin Cerqueira (@KevinCerqueira)
# EXA 869 - MI - Processadores de Linguagem de Programacao
# ==============================================================================
# Implementação do Análisador Semântico de um compilador

import sys
import string
import os

class SemanticAnalyzer():
	
	# Diretório dos arquivos de saída.
	dir_input = '\\output_syntactic\\'
	# Diretório dos arquivos de saída.
	dir_output = '\\output_semantic\\'
	
	#Leitura e escrita do arquivo de entradaX.txt e de saídaX.txt
	def openFiles(self, file_input):
		try:
			read_file = open(os.getcwd() + self.dir_input + file_input, 'r')
			write_file = open(os.getcwd() + self.dir_output + str(file_input).replace('saida_sintatica', 'saida_semantica'), 'w')
			return [read_file, write_file]
		except:
			write_file = open(os.getcwd() + self.dir_input + str(file_input).replace('saida_sintatica', 'saida_semantica'), 'w')
			write_file.write("[ERRO] Não foi possível ler o arquivo de entrada '{}'.".format(self.dir_input + file_input))
			sys.exit()
	
	# Verifica se as pastas e arquivos de entrada e saída existem, caso os 
	# arquivos de sáida exitam, é retornado todos aqueles que estão na pasta,
	# caso não existam, retorna um aviso.
	def openPrograms(self):
		if(not (os.path.isdir(os.getcwd() + self.dir_input))):
			print("[ERRO] Não foi possível encontrar o diretório de entrada '{}'.".format(self.dir_input))
			sys.exit()

		if(not (os.path.isdir(os.getcwd() + self.dir_output))):
			os.mkdir(os.getcwd() + self.dir_output)

		files_programs = []
		for iterator in os.listdir(os.getcwd() + self.dir_input):
			if(iterator.count('.txt')):
				files_programs.append(iterator)

		if(len(files_programs) < 1):
			print('[WARNING] Não há arquivos para ler!')
			sys.exit()
		return files_programs
		
	identifiers_file = []
	# Índice do arquivo atual
	line_index = 0
	# Linha por completo do arquivo atual
	line_current = ""
	
	# Tabelas semânticas
	semantic_table = {}
	# Tabelas struct
	struct_table = {}
	# Tabelas const
	const_table = {}
	var_globals_table = {}
	function_table = {}
	star_table = {}
	
	
	def __init__(self):
		# Arquivos do programa
		files_programs = self.openPrograms()

		# Laço de repetição que percorre todos os arquivos encontrados na 
		# pasta de saida do analisador lexico (output_lexical/saidaX.txt).
		for file_program in files_programs:
			# Verifica se há algum erro sintático
			self.hasError = False

			read_file = self.openFiles(file_program)[0]
			self.write_file = self.openFiles(file_program)[1]
			self.identifiers_file = read_file.readlines()

			self.line_index = 0
			self.line_current = ""

			self.semantic_table['struct'] = self.struct_table
			self.semantic_table['const'] = self.const_table
			self.semantic_table['var_globals'] = self.var_globals_table
			self.semantic_table['function'] = self.function_table
			self.semantic_table['start'] = self.start_table
	
	# Pega o conteudo do indentificador/token
	def contentIdentifier(self):
		return self.identifiers_file[self.line_index][self.identifiers_file[self.line_index].find(' ') : self.identifiers_file[self.line_index].find('\n')]

	# Vai para o próximo identificador/token
	def nextIdentifier(self):
		final = False	
		try:
			if('$' in self.identifiers_file[self.line_index]):
				final = True
			self.line_index += 1
			if(not '$' in self.identifiers_file[self.line_index]):
				self.line_current = self.identifiers_file[self.line_index][self.identifiers_file[self.line_index].find(' ') + 1 : -2]
			else:
				final = True
			self.hasException()
			if(not "ERRO" in self.identifiers_file[self.line_index]):
				self.write_file.write(self.identifiers_file[self.line_index])
		except:
			if(not final):
				self.write_file.write("\nERROS SEMANTICOS - VERIFIQUE E TENTE NOVAMENTE")
			self.write_file.close()
			sys.exit()
			
	def exception(self, exception):
		self.write_file.write("{} ERRO SEMANTICO - {} [onde: {}]\n".format(self.line_index, exception, self.line_current))
		self.hasError = True
		
	def struct_table(self):
		if('IDE' in self.identifiers_file[self.line_index]):
			identifier_struct = self.contentIdentifier()
			inputs_struct = {}
			self.nextIdentifier()
			while(not 'DEL }' in self.identifiers_file[self.line_index]):
				if(
					'PRE string' in self.identifiers_file[self.line_index] or
					'PRE int' in self.identifiers_file[self.line_index] or
					'PRE real' in self.identifiers_file[self.line_index] or
					'PRE boolean' in self.identifiers_file[self.line_index]
				):
					identifier_type = self.contentIdentifier()
					self.nextIdentifier()
					if('IDE' in self.identifiers_file[self.line_index]):
						identifier_input = self.contentIdentifier()
						
						if(not self.struct_table.get(identifier_type).has_key(identifier_input)):
							inputs_struct[identifier_input] = [identifier_type, 'input_struct']
						else:
							self.exception("{} JA FOI DECLARADO EM '{}'".format(identifier_input, identifier_struct))
				self.nextIdentifier()
	
	def const_table(self):
		while(not 'DEL }' in self.identifiers_file[self.line_index]):
			if(
				'PRE string' in self.identifiers_file[self.line_index] or
				'PRE int' in self.identifiers_file[self.line_index] or
				'PRE real' in self.identifiers_file[self.line_index] or
				'PRE boolean' in self.identifiers_file[self.line_index]
			):
				identifier_type = self.contentIdentifier()
				self.nextIdentifier()
				if('IDE' in self.identifiers_file[self.line_index]):
					identifier_input = self.contentIdentifier()
					self.nextIdentifier()
					if(not self.const_table.has_key(identifier_input)):
						if('REL =' in self.identifiers_file[self.line_index]):
							self.nextIdentifier()
							if(
								identifier_type == 'PRE int' and 'NRO' in self.identifiers_file[self.line_index] or
								identifier_type == 'PRE real' and 'NRO' in self.identifiers_file[self.line_index] or
								identifier_type == 'PRE string' and 'SIM' in self.identifiers_file[self.line_index] or
								identifier_type == 'PRE string' and 'CAD' in self.identifiers_file[self.line_index] or
								identifier_type == 'PRE boolean' and 'PRE true' in self.identifiers_file[self.line_index] or
								identifier_type == 'PRE boolean' and 'PRE false' in self.identifiers_file[self.line_index]
							):
								self.const_table[identifier_input] = [identifier_type, 'input_const', 'global']
							else:
								self.exception("ATRIBUIÇÃO NÃO CONDIZENTE COM O TIPO DA VARIAVEL '{}'".format(identifier_input))
						else:
							self.exception("{} JA FOI DECLARADO EM 'const'".format(identifier_input))
			self.nextIdentifier()
	
	