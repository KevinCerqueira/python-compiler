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
	var_local_table = {}
	function_table = {}
	procedure_table = {}
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
			self.write_file.write(self.identifiers_file[self.line_index])
			self.program()
			self.semantic_table['struct'] = self.struct_table
			self.semantic_table['const'] = self.const_table
			self.semantic_table['var_globals'] = self.var_globals_table
			self.semantic_table['function'] = self.function_table
			self.semantic_table['start'] = self.start_table
			
			print(self.semantic_table)
			self.write_file.close()
			read_file.close()
		sys.exit()	
		
	
	# Pega o conteudo do indentificador/token
	def contentIdentifier(self):
		return self.currentIdentifier()[self.currentIdentifier().find(' ') : self.currentIdentifier().find('\n')]

	# Vai para o próximo identificador/token
	def nextIdentifier(self):
		final = False	
		try:
			self.line_index += 1
			self.line_current = self.currentIdentifier()[self.currentIdentifier().find(' ') + 1 : -2]
			self.write_file.write(self.identifiers_file[self.line_index])
			if("ERRO" in self.currentIdentifier()):
				self.line_index += 1
				self.line_current = self.currentIdentifier()[self.currentIdentifier().find(' ') + 1 : -2]
				# self.write_file.write("\nERROS LEXICOS/SINTATICOS - VERIFIQUE E TENTE NOVAMENTE")
				# self.write_file.close()
				# sys.exit()
			# self.write_file.write(self.identifiers_file[self.line_index])
		except:
			self.write_file.close()
			sys.exit()
	
	def currentIdentifier(self):
		final = False	
		try:
			if('$' in self.identifiers_file[self.line_index]):
				final = True
				self.write_file.close()
				sys.exit()
			else:
				return self.identifiers_file[self.line_index]
		except:
			if(not final):
				self.write_file.write("\nERROS SEMANTICOS - VERIFIQUE E TENTE NOVAMENTE")
			self.write_file.close()
			sys.exit()
			
	def exception(self, exception):
		self.write_file.write("{} ERRO SEMANTICO - {} [onde: {}]\n".format(self.line_index, exception, self.line_current))
		self.hasError = True
		
	def struct(self):
		if('IDE' in self.currentIdentifier()):
			identifier_struct = self.contentIdentifier()
			inputs_struct = {}
			
			self.struct_table[identifier_struct] = inputs_struct
			self.nextIdentifier()
			while(not 'DEL }' in self.currentIdentifier()):
				if(
					'PRE string' in self.currentIdentifier() or
					'PRE int' in self.currentIdentifier() or
					'PRE real' in self.currentIdentifier() or
					'PRE boolean' in self.currentIdentifier()
				):
					identifier_type = self.contentIdentifier()
					self.nextIdentifier()
					if('IDE' in self.currentIdentifier()):
						identifier_input = self.contentIdentifier()
						aux = False
						for item in self.struct_table.get(identifier_struct):
							if(item == identifier_input):
								aux = True
						if(not aux):
							inputs_struct[identifier_input] = [identifier_type, 'struct']
						else:
							self.exception("{} JA FOI DECLARADO EM '{}'".format(identifier_input, identifier_struct))
				self.nextIdentifier()
	
	def const(self):
		while(not 'DEL }' in self.currentIdentifier()):
			if(
				'PRE string' in self.currentIdentifier() or
				'PRE int' in self.currentIdentifier() or
				'PRE real' in self.currentIdentifier() or
				'PRE boolean' in self.currentIdentifier()
			):
				identifier_type = self.contentIdentifier()
				self.nextIdentifier()
				if('IDE' in self.currentIdentifier()):
					identifier_input = self.contentIdentifier()
					self.nextIdentifier()
					aux = False
					for item in self.const_table:
						if(item == identifier_input):
							aux = True
					if(not aux):
						if('REL =' in self.currentIdentifier()):
							self.nextIdentifier()
							if(
								('int' in identifier_type and 'NRO' in self.currentIdentifier()) or
								('real' in identifier_type and 'NRO' in self.currentIdentifier()) or
								('string' in identifier_type and 'SIM' in self.currentIdentifier()) or
								('string' in identifier_type and 'CAD' in self.currentIdentifier()) or
								('boolean' in identifier_type and 'true' in self.currentIdentifier()) or
								('boolean' in identifier_type and 'false' in self.currentIdentifier())
							):
								self.const_table[identifier_input] = [identifier_type, 'input_const', 'global']
							else:
								self.exception("ATRIBUICAO NAO CONDIZENTE COM O TIPO DA VARIAVEL '{}'".format(identifier_input))
						else:
							self.exception("{} JA FOI DECLARADO EM 'const' OU NAO FOI ENCONTRADO O ATRIBUIDOR '='".format(identifier_input))
			self.nextIdentifier()
	
	def var(self):
		category = ""
		while(not 'DEL }' in self.currentIdentifier()):
			if(
				'PRE string' in self.currentIdentifier() or
				'PRE int' in self.currentIdentifier() or
				'PRE real' in self.currentIdentifier() or
				'PRE boolean' in self.currentIdentifier() or
				'IDE' in self.currentIdentifier()
			):
				if('DEL' in self.currentIdentifier()):
					category = 'const_var'
				else:
					category = 'global_var'
					
				identifier_type = self.contentIdentifier()
				self.nextIdentifier()
				
				if('IDE' in self.currentIdentifier()):
					identifier_input = self.contentIdentifier()
					self.nextIdentifier()
					aux = False
					for item in self.var_globals_table:
						if(item == identifier_input):
							aux = True
					if(not aux):
						if('DEL [' in self.currentIdentifier()):
							self.nextIdentifier()
							category = 'vector_var'
							if('NRO' in self.currentIdentifier()):
								self.nextIdentifier()
								if('DEL ]' in self.currentIdentifier()):
									self.nextIdentifier()
									if('DEL [' in self.currentIdentifier()):
										self.nextIdentifier()
										category = 'matrix_var'
										if('NRO' in self.currentIdentifier()):
											self.nextIdentifier()
										if('DEL ]' in self.currentIdentifier()):
											self.nextIdentifier()
						
						if('DEL ;' in self.currentIdentifier()):
							self.var_globals_table[identifier_input] = [identifier_type, category, 'global']
						elif('REL =' in self.currentIdentifier()):
							self.nextIdentifier()
							if(
								('int' in identifier_type and 'NRO' in self.currentIdentifier()) or
								('real' in identifier_type and 'NRO' in self.currentIdentifier()) or
								('string' in identifier_type and 'SIM' in self.currentIdentifier()) or
								('string' in identifier_type and 'CAD' in self.currentIdentifier()) or
								('boolean' in identifier_type and 'true' in self.currentIdentifier()) or
								('boolean' in identifier_type and 'false' in self.currentIdentifier())
							):
								self.var_globals_table[identifier_input] = [identifier_type, category, 'global']
							else:
								self.exception("ATRIBUICAO NAO CONDIZENTE COM O TIPO DA VARIAVEL '{}'".format(identifier_input))
					else:
						self.exception("{} JA FOI DECLARADO NAS VARIAVEIS GLOBAIS".format(identifier_input))
			self.nextIdentifier()
			
	def var_global(self):
		category = ""
		while(not 'DEL }' in self.currentIdentifier()):
			if(
				'PRE string' in self.currentIdentifier() or
				'PRE int' in self.currentIdentifier() or
				'PRE real' in self.currentIdentifier() or
				'PRE boolean' in self.currentIdentifier() or
				'IDE' in self.currentIdentifier()
			):
				if('DEL' in self.currentIdentifier()):
					category = 'const_var'
				else:
					category = 'global_var'
					
				identifier_type = self.contentIdentifier()
				self.nextIdentifier()
				
				if('IDE' in self.currentIdentifier()):
					identifier_input = self.contentIdentifier()
					self.nextIdentifier()
					aux = False
					for item in self.var_globals_table:
						if(item == identifier_input):
							aux = True
					if(not aux):
						if('DEL [' in self.currentIdentifier()):
							self.nextIdentifier()
							category = 'vector_var'
							if('NRO' in self.currentIdentifier()):
								self.nextIdentifier()
								if('DEL ]' in self.currentIdentifier()):
									self.nextIdentifier()
									if('DEL [' in self.currentIdentifier()):
										self.nextIdentifier()
										category = 'matrix_var'
										if('NRO' in self.currentIdentifier()):
											self.nextIdentifier()
										if('DEL ]' in self.currentIdentifier()):
											self.nextIdentifier()
						
						if('DEL ;' in self.currentIdentifier()):
							self.var_globals_table[identifier_input] = [identifier_type, category, 'global']
						elif('REL =' in self.currentIdentifier()):
							self.nextIdentifier()
							if(
								('int' in identifier_type and 'NRO' in self.currentIdentifier()) or
								('real' in identifier_type and 'NRO' in self.currentIdentifier()) or
								('string' in identifier_type and 'SIM' in self.currentIdentifier()) or
								('string' in identifier_type and 'CAD' in self.currentIdentifier()) or
								('boolean' in identifier_type and 'true' in self.currentIdentifier()) or
								('boolean' in identifier_type and 'false' in self.currentIdentifier())
							):
								self.var_globals_table[identifier_input] = [identifier_type, category, 'global']
							else:
								self.exception("ATRIBUICAO NAO CONDIZENTE COM O TIPO DA VARIAVEL '{}'".format(identifier_input))
					else:
						self.exception("{} JA FOI DECLARADO NAS VARIAVEIS/CONSTANTES GLOBAIS".format(identifier_input))
			self.nextIdentifier()
	
	def var_local(self):
		category = ""
		while(not 'DEL }' in self.currentIdentifier()):
			if(
				'PRE string' in self.currentIdentifier() or
				'PRE int' in self.currentIdentifier() or
				'PRE real' in self.currentIdentifier() or
				'PRE boolean' in self.currentIdentifier() or
				'IDE' in self.currentIdentifier()
			):
				if('DEL' in self.currentIdentifier()):
					category = 'const_var'
				else:
					category = 'global_var'
					
				identifier_type = self.contentIdentifier()
				self.nextIdentifier()
				
				if('IDE' in self.currentIdentifier()):
					identifier_input = self.contentIdentifier()
					self.nextIdentifier()
					aux = False
					for item in self.var_local_table:
						if(item == identifier_input):
							aux = True
					if(not aux):
						if('DEL [' in self.currentIdentifier()):
							self.nextIdentifier()
							category = 'vector_var'
							if('NRO' in self.currentIdentifier()):
								self.nextIdentifier()
								if('DEL ]' in self.currentIdentifier()):
									self.nextIdentifier()
									if('DEL [' in self.currentIdentifier()):
										self.nextIdentifier()
										category = 'matrix_var'
										if('NRO' in self.currentIdentifier()):
											self.nextIdentifier()
										if('DEL ]' in self.currentIdentifier()):
											self.nextIdentifier()
						
						if('DEL ;' in self.currentIdentifier()):
							self.var_local_table[identifier_input] = [identifier_type, category, 'local']
						elif('REL =' in self.currentIdentifier()):
							self.nextIdentifier()
							if(
								('int' in identifier_type and 'NRO' in self.currentIdentifier()) or
								('real' in identifier_type and 'NRO' in self.currentIdentifier()) or
								('string' in identifier_type and 'SIM' in self.currentIdentifier()) or
								('string' in identifier_type and 'CAD' in self.currentIdentifier()) or
								('boolean' in identifier_type and 'true' in self.currentIdentifier()) or
								('boolean' in identifier_type and 'false' in self.currentIdentifier())
							):
								self.var_local_table[identifier_input] = [identifier_type, category, 'local']
							else:
								self.exception("ATRIBUICAO NAO CONDIZENTE COM O TIPO DA VARIAVEL '{}'".format(identifier_input))
					else:
						self.exception("{} JA FOI DECLARADO NAS VARIAVEIS/CONSTANTES GLOBAIS".format(identifier_input))
			self.nextIdentifier()
			
	def procedure(self):
		self.procedure_table = self.contentIdentifier()
		self.nextIdentifier()
		while('DEL {' in self.currentIdentifier()):
			self.nextIdentifier()
		self.nextIdentifier()
		if('PRE var' in self.currentIdentifier()):
			self.var_local()
	
	def function(self):
		self.nextIdentifier()
		self.function_table = self.contentIdentifier()
		self.nextIdentifier()
		while('DEL {' in self.currentIdentifier()):
			self.nextIdentifier()
		self.nextIdentifier()
		if('PRE var' in self.currentIdentifier()):
			self.var_local()
	
	def start(self):
		self.nextIdentifier()
		
	def program(self):		
		while(not "$" in self.currentIdentifier()):
			
			if('PRE struct' in self.currentIdentifier()):
				self.nextIdentifier()
				self.struct()
			elif('PRE const' in self.currentIdentifier()):
				self.nextIdentifier()
				self.const()
			elif('PRE var' in self.currentIdentifier()):
				self.nextIdentifier()
				self.var_global()
			elif('PRE function' in self.currentIdentifier()):
				self.nextIdentifier()
				self.function()
			elif('PRE procedure' in self.currentIdentifier()):
				self.nextIdentifier()
				self.procedure()
			elif('PRE start' in self.currentIdentifier()):
				self.nextIdentifier()
				self.start()
			else:
				self.nextIdentifier()
		if(self.hasError):
			self.exception("ERROS SEMANTICOS - VERIFIQUE E TENTE NOVAMENTE")
			return False
		else:
			self.write_file("CADEIA RECONHECIDA COM SUCESSO")
			return True

# SemanticAnalyzer()