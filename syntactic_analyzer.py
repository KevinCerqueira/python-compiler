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
            
            self.Program()
    
    # Vai para o próximo identificador/token
    def nextIdentifier(self):
        self.line_index += 1
        if('$' in self.identifiers_file[self.line_index]):
            self.write_file.write("ANÁLISE SINTÁTICA FINALIZADA")
            sys.exit()
        print(self.line_index, self.identifiers_file[self.line_index])
        self.line_current = self.identifiers_file[self.line_index][self.identifiers_file[self.line_index].find(' ') + 1 : -2]
    
    # Pega o conteudo do indentificador/token
    def contentIdentifier(self):
        # return self.identifiers_file[self.line_index][self.identifiers_file[self.line_index].find('|')+1 : self.identifiers_file[self.line_index].find(' ')]
        return self.identifiers_file[self.line_index][self.identifiers_file[self.line_index].find(' ') : self.identifiers_file[self.line_index].find('\n')]
    
    # Procura por um erro, caso haja vai para a próxima linha
    def hasException(self):
        if("[ERRO]" in self.identifiers_file[self.line_index]):
            self.line_index += 1
    
    def exception(self, exception):
        self.write_file.write("{} ERRO SINTATICO - {} [{}]\n".format(self.line_index, exception, self.line_current))
        self.hasError = True
    
    def Program(self):
        self.hasException()
        
        self.StructDecl()
        self.ConstDecl()
        self.table_global = self.VarDecl()
        # self.table_function = self.FuncDecl()
        # self.start()
        
        if(self.hasError):
            self.write_file.write("ERROS SINTÁTICOS - VERIFIQUE E TENTE NOVAMENTE")
        else:
            if('$' in self.identifiers_file[self.line_index]):
                self.write_file.write("ANÁLISE SINTÁTICA FINALIZADA")
            else:
                self.write_file.write("FIM NÃO ENCONTRADO")
        
        # self.write_file.write('\n')
        # self.write_file.write(self.table_struct)
        # self.write_file.write('\n')
        # self.write_file.write(self.table_const)
        # self.write_file.write('\n')
        # self.write_file.write(self.table_function)
        # self.write_file.write('\n')
        # self.write_file.write(self.table_start)
        # self.write_file.write('\n')
        
        self.write_file.close()
    
    def StructDecl(self): # registro_declaracao
        self.hasException()
        
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
                
    def Decls(self): # declaracao_reg
        self.hasException()
        decl_return = {}
        
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
    
    def Decl(self): # declaracao
        self.hasException()
        decls = {}
        decl_name = ''
        decl_type = ''
        
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
        
    def Type(self): # tipo_primitivo
        self.hasException()
        
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
                while("DEL ;" in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                self.exception("';' DUPLICADOS")
            self.exception("ESPERADO 'int' OU 'real' OU 'boolean' OU 'string'")
            while(not 'IDE' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
        return typeContent
    
    def ConstDecl(self): # constante_declaracao
        self.hasException()
        
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
    
    def Const(self): #declaracao_const
        self.hasException()
        const_inputs = {}
        const_values = []
        
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
    
    def Value(self): # valor_primitivo
        self.hasException()          
        value = ""
        
        if(
            "PRE false" in self.identifiers_file[self.line_index] or
            "PRE true" in self.identifiers_file[self.line_index] or
            "SIM" in self.identifiers_file[self.line_index] or
            "CAD" in self.identifiers_file[self.line_index] or
            "NRO" in self.identifiers_file[self.line_index]
        ):
            value = self.contentIdentifier()
            self.nextIdentifier()
        else:
            self.exception("ESPERADO NUMERO, CADEIA DE CARACTERES, SIMBOLO OU VERDADEIRO OU FALSO")
            while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
        return value
        
    def VarDecl(self): # variaveis_declaracao
        self.hasException()
        return_vardecl = {}
        
        if('PRE var' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            if('DEL {' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                if(not 'DEL }' in self.identifiers_file[self.line_index]):
                    return_vardecl = self.VariablesList()
                if('DEL }' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                else:
                    self.exception("ESPERADO '}' NO FINAL DO BLOCO 'var'")
                    if('PRE function' in self.identifiers_file[self.line_index] or 'PRE start' in self.identifiers_file[self.line_index] or 'PRE procedure' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
                    while(not 'PRE function' in self.identifiers_file[self.line_index] or 'PRE start' in self.identifiers_file[self.line_index] or 'PRE procedure' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
            else:
                self.exception("ESPERADO '{' APOS DECLARAÇAO 'var'")
                while(not 'PRE function' in self.identifiers_file[self.line_index] or 'PRE start' in self.identifiers_file[self.line_index] or 'PRE procedure' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
        else:
            self.exception("DECLARAÇÃO DO BLOCO 'var' É OBRIGATORIA")
            while(not 'PRE function' in self.identifiers_file[self.line_index] or 'PRE start' in self.identifiers_file[self.line_index] or 'PRE procedure' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                
        return return_vardecl
            
    def VariablesList(self): # declaracao_var
        self.hasException()
        var_globals = {}
        var_globals_content = []
        
        if('IDE' in self.identifiers_file[self.line_index]):
            type_block = self.contentIdentifier()
            self.nextIdentifier()
            if('IDE' in self.identifiers_file[self.line_index]):
                identifier_block = self.contentIdentifier()
                self.nextIdentifier()
                if('DEL ;' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                    var_globals[identifier_block] = var_globals_content
                    var_globals_content.append(type_block)
                    var_globals_content.append("TYPE_STRUCT")
                    var_globals_content.append("NO_INIT")
                    if(not 'DEL }' in self.identifiers_file[self.line_index]):
                        var_globals.update(self.VariablesList())
                    else:
                        return var_globals
                else:
                    self.exception("ESPERADO ';'")
                    while(
                        not 'PRE string' in self.identifiers_file[self.line_index] or
                        not 'PRE real' in self.identifiers_file[self.line_index] or
                        not 'PRE int' in self.identifiers_file[self.line_index] or
                        not 'PRE char' in self.identifiers_file[self.line_index] or
                        not 'PRE boolean' in self.identifiers_file[self.line_index] or
                        not 'IDE' in self.identifiers_file[self.line_index]
                    ):
                        self.nextIdentifier()
            else:
                self.exception("ESPERADO IDENTIFICACAO DO TIPO DO BLOCO")
                while(
                    not 'PRE string' in self.identifiers_file[self.line_index] or
                    not 'PRE real' in self.identifiers_file[self.line_index] or
                    not 'PRE int' in self.identifiers_file[self.line_index] or
                    not 'PRE char' in self.identifiers_file[self.line_index] or
                    not 'PRE boolean' in self.identifiers_file[self.line_index] or
                    not 'IDE' in self.identifiers_file[self.line_index]
                ):
                    self.nextIdentifier()
        elif(
            'PRE string' in self.identifiers_file[self.line_index] or
            'PRE real' in self.identifiers_file[self.line_index] or
            'PRE int' in self.identifiers_file[self.line_index] or
            'PRE char' in self.identifiers_file[self.line_index] or
            'PRE boolean' in self.identifiers_file[self.line_index]
        ):
            decl = self.Decl()
            key = list(decl.keys())
            var_globals[key[0]] = var_globals_content
            var_globals_content.append(decl[key[0]])
            
            # content = []
            # content = self.Aux()
            # if(len(content) == 0):
            #     var_globals_content.append("SIMPLE")
            #     var_globals_content.append("NO_INIT")
            # else:
            #     if(content[0] == 0):
            #         var_globals_content.append("SIMPLE")
            #         var_globals_content.append(content[1])
            #     elif(content[0] == 1):
            #         var_globals_content.append("VECTOR")
            #         var_globals_content.append("NO_INIT")
            #         var_globals_content.append(content[1])
            #     elif(content[0] == 1):
            #         var_globals_content.append("MATRIX")
            #         var_globals_content.append("NO_INIT")
            #         var_globals_content.append(content[1])
            #         var_globals_content.append(content[2])
            if('DEL ;' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                if(not 'DEL }' in self.identifiers_file[self.line_index]):
                    var_globals.update(self.VariablesList())
                else:
                    return var_globals
            else:
                self.exception("ESPERADO ';'")
                while(
                    not 'PRE string' in self.identifiers_file[self.line_index] or
                    not 'PRE real' in self.identifiers_file[self.line_index] or
                    not 'PRE int' in self.identifiers_file[self.line_index] or
                    not 'PRE char' in self.identifiers_file[self.line_index] or
                    not 'PRE boolean' in self.identifiers_file[self.line_index] or
                    not 'IDE' in self.identifiers_file[self.line_index]
                ):
                    self.nextIdentifier()
        else:
            if('DEL ;' in self.identifiers_file[self.line_index]):
                while('DEL ;' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                self.exception("';' DUPLICADO")
            self.exception("ESPERADO 'string' ou 'int' ou 'real' ou 'boolean'")
            while(
                    not 'PRE string' in self.identifiers_file[self.line_index] or
                    not 'PRE real' in self.identifiers_file[self.line_index] or
                    not 'PRE int' in self.identifiers_file[self.line_index] or
                    not 'PRE char' in self.identifiers_file[self.line_index] or
                    not 'PRE boolean' in self.identifiers_file[self.line_index] or
                    not 'IDE' in self.identifiers_file[self.line_index]
                ):
                    self.nextIdentifier()
        return var_globals
            
    def Aux(self): # identificador_deriva
        pass
        

# Função main, cria um objeto e inicia o Analisador Sintatico
if __name__ == '__main__':
    analyzer = SyntacticAnalyzer()
    sys.exit()
