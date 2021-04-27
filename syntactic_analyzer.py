# Authors: 
# Esdras Abreu (@EsdrasAbreu)
# Kevin Cerqueira (@KevinCerqueira)
# EXA 869 - MI - Processadores de Linguagem de Programacao
# ==============================================================================
# Implementação do Análisador Léxico de um compilador

# Bibliotecas para entrada e saida de arquivos
import sys
import string
import os
# from itertools import chain

class SyntacticAnalyzer():
	
	# Diretório dos arquivos de saída.
    dir_input = '\\output_lexical\\'
	# Diretório dos arquivos de saída.
    dir_output = '\\output_syntactic\\'
	
	#Leitura e escrita do arquivo de entradaX.txt e de saídaX.txt
    def openFiles(self, file_input):
        try:
            read_file = open(os.getcwd() + self.dir_input + file_input, 'r')
            write_file = open(os.getcwd() + self.dir_output + str(file_input).replace('saida', 'saida_sintatica'), 'w')
            return [read_file, write_file]
        except:
            write_file = open(os.getcwd() + self.dir_input + str(file_input).replace('saida', 'saida_sintatica'), 'w')
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
	
    # Identificadores resultantes da analise lexica
    identifiers_file = []
    # Índice do arquivo atual
    line_index = 0
    # Linha por completo do arquivo atual
    line_current = ""
    
    
    # Tabelas da análise sintatica
    table_struct = {}
    table_const = {}
    table_global = {}
    table_function = {}
    table_start = {}
    
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
            
            self.start()
    
    # Vai para o próximo identificador/token
    def nextIdentifier(self):
        self.line_index += 1
        self.line_current = self.identifiers_file[self.line_index][self.identifiers_file[self.line_index].find(' ') + 1 : -1]
    
    # Pega o conteudo do indentificador/token
    def contentIdentifier(self):
        return self.identifiers_file[self.line_index][self.identifiers_file[self.line_index].find('|')+1 : self.identifiers_file[self.line_index].find(' ')]
    
    # Procura por um erro, caso haja vai para a próxima linha
    def nextIndex(self):
        if("[ERRO]" in self.identifiers_file[self.line_index]):
            self.line_index += 1
    
    def exception(self, exception):
        self.write_file.write("{} ERRO SINTÁTICO - {} [{}]".format(self.line_current, exception, self.identifiers_file[self.line_index]))
        self.hasError = True
    
    def Program(self):
        self.nextIndex()
        
        self.StructDecl()
        self.ConstDecl()
        self.table_global = self.VarDecl()
        self.table_function = self.FuncDecl()
        self.start()
        
        if(self.hasError):
            self.write_file.write("ERROS SINTÁTICOS - VERIFIQUE E TENTE NOVAMENTE")
        else:
            if('$' in self.identifiers_file[self.line_index]):
                self.write_file.write("ANÁLISE SINTÁTICA FINALIZADA")
            else:
                self.write_file.write("FIM NÃO ENCONTRADO")
        
        self.write_file.write('\n')
        self.write_file.write(self.table_struct)
        self.write_file.write('\n')
        self.write_file.write(self.table_const)
        self.write_file.write('\n')
        self.write_file.write(self.table_function)
        self.write_file.write('\n')
        self.write_file.write(self.table_start)
        self.write_file.write('\n')
        
        self.write_file.close()
    
    def StructDecl(self):
        self.nextIndex()
        
        if('PRE struct' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            if('IDE' in self.identifiers_file[self.line_index]):
                struct_name = self.contentIdentifier()
                self.nextIdentifier()
                if('DEL {' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                    struct_inputs = self.Decls()
                    if('DEL }' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
                        self.table_struct[struct_name] = struct_inputs
                        self.StructDecl()
                    else:
                        self.exception("ESPERADO '}'")
                        while(not 'PRE const' in self.identifiers_file[self.line_index] or not 'PRE struct' in self.identifiers_file[self.line_index]):
                            self.nextIdentifier()
                else:
                    self.exception("ESPERADO '{'")
                    while(not 'PRE const' in self.identifiers_file[self.line_index] or not 'PRE struct' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
            else:
                self.exception("ESPERADO UM IDENTIFICADOR")
                while(not 'PRE const' in self.identifiers_file[self.line_index] or not 'PRE struct' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                return
                
    def Decls(self):
        decl_return = {}
        self.nextIndex()
        
        if('DEL }' in self.identifiers_file[self.line_index]):
            return decl_return
            
        decl_return = self.Decl()
        
        if('DEL ;' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            decl_return.update(self.Decls())
            return decl_return
        else:
            self.exception("ESPERADO ';'")
            while(not 'DEL }' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
    
    def Decl(self):
        decls = {}
        decl_name = ''
        decl_type = ''
        self.nextIndex()
        
        decl_type = self.Type()
        
        if('IDE' in self.identifiers_file[self.line_index]):
            decl_name = self.contentIdentifier()
            self.nextIdentifier()
        else:
            if('DEL ;' in self.identifiers_file[self.line_index]):
                while('DEL ;' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                self.exception("';' DUPLICADO")
            else:
                self.exception("ESPERADO UM IDENTIFICADOR")
            while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                
        decls[decl_name] = decl_type
        return decls
        
    def Type(self):
        self.nextIndex()
        
        typeContent = ""
        if(
            "PRE int" in self.identifiers_file[self.line_index] or
            "PRE real" in self.identifiers_file[self.line_index] or
            "PRE boolean" in self.identifiers_file[self.line_index] or
            "PRE string" in self.identifiers_file[self.line_index]
        ):
            typeContent = self.contentIdentifier()
            self.nextIdentifier()
        else:
            if("DEL ;" in self.identifiers_file[self.line_index]):
                while("DEL ;" in self.identifiers_file[self.identifiers_file]):
                    self.nextIdentifier()
                self.exception("';' DUPLICADOS")
            self.exception("ESPERADO 'int' OU 'real' OU 'boolean' OU 'string'")
            while(not 'IDE' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
        return typeContent
    
    def ConstDecl(self):
        self.nextIndex()
        
        if('PRE const' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            if('DEL {' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                if(not 'DEL }' in self.identifiers_file[self.line_index]):
                    self.table_const = self.Decls()
                if('DEL }' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                else:
                    self.exception("ESPERADO '}'")
                    if('PRE var' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
                    while(not 'PRE var' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
            else:
                self.exception("ESPERADO '{'")
                while(not 'PRE var' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
        else:
            self.exception("ESPERADO 'const'")
            while(not 'PRE var' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
    
    def Const(self):
        const_inputs = {}
        const_values = []
        self.nextIndex()
        
        if('DEL }' in self.identifiers_file[self.line_index]):
            return const_inputs
        decls = self.Decl()
        key = list(decls.keys())
        const_inputs[key[0]] = const_values
        const_values.append(decls[key[0]])
        
        if('REL =' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            
            const_value = self.Value()
            const_values.append(const_value)
            
            if('DEL ;' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                const_inputs.update(self.Const())
                return const_inputs
            else:
                self.exception("ESPERADO ';'")
                while(not 'DEL }' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
        else:
            self.exception("ESPERADO '='")
            while(not 'DEL }' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                                     
# Função main, cria um objeto e inicia o Analisador Sintatico
if __name__ == '__main__':
    analyzer = SyntacticAnalyzer()
    sys.exit()
