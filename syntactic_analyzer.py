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
        # if('$' in self.identifiers_file[self.line_index]):
        #     self.write_file.write("ANALISE SINTATICA FINALIZADA")
        #     self.Program()
        print('next ',self.line_index, self.identifiers_file[self.line_index])
        # if(self.line_index == 295):
        #     print(self.identifiers_file[self.line_index+1000][self.identifiers_file[self.line_index].find(' ') + 1 : -2])
        # self.write_file.write(self.identifiers_file[self.line_index])
        self.line_index += 1
        self.line_current = self.identifiers_file[self.line_index][self.identifiers_file[self.line_index].find(' ') + 1 : -2]
        self.hasException()
    # Vai para o próximo identificador/token
    def previousIdentifier(self):
        # if('$' in self.identifiers_file[self.line_index]):
        #     self.write_file.write("ANALISE SINTATICA FINALIZADA")
        #     self.Program()
        print('next ',self.line_index, self.identifiers_file[self.line_index])
        # if(self.line_index == 220):
        #     print(self.identifiers_file[self.line_index+1000][self.identifiers_file[self.line_index].find(' ') + 1 : -2])
        # self.write_file.write(self.identifiers_file[self.line_index])
        self.line_index -= 1
        self.line_current = self.identifiers_file[self.line_index][self.identifiers_file[self.line_index].find(' ') + 1 : -2]
        self.hasException()
        
    # Pega o conteudo do indentificador/token
    def contentIdentifier(self):
        # return self.identifiers_file[self.line_index][self.identifiers_file[self.line_index].find('|')+1 : self.identifiers_file[self.line_index].find(' ')]
        return self.identifiers_file[self.line_index][self.identifiers_file[self.line_index].find(' ') : self.identifiers_file[self.line_index].find('\n')]
    
    # Procura por um erro, caso haja vai para a próxima linha
    def hasException(self):
        if("[ERRO]" in self.identifiers_file[self.line_index]):
            # self.write_file.write(self.identifiers_file[self.line_index])
            self.line_index += 1
    
    # Procura por um erro, caso haja vai para a próxima linha
    def isEndFile(self):
        if('$' in self.identifiers_file[self.line_index]):
            return True
        return False
    
    def exception(self, exception):
        self.write_file.write("{} ERRO SINTATICO - {} [palavra problematica: {}]\n".format(self.line_index, exception, self.line_current))
        self.hasError = True
    
    def Program(self):
        self.hasException()
        
        self.StructDecl()
        self.ConstDecl()
        self.table_global = self.VarDecl()
        self.table_function = self.FunctionDeclaration()
        self.Start()
        
        if(self.hasError):
            self.write_file.write("ERROS SINTÁTICOS - VERIFIQUE E TENTE NOVAMENTE")
        else:
            if('$' in self.identifiers_file[self.line_index]):
                self.write_file.write("ANALISE SINTATICA FINALIZADA")
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
        elif(
            "PRE local" in self.identifiers_file[self.line_index] or
            "PRE global" in self.identifiers_file[self.line_index]
        ):
            typeContent = self.contentIdentifier()
            self.nextIdentifier()
            if('DEL .' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
            else:
                self.exception("ESPERADO '.'")
                while(not 'IDE' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
        elif("PRE struct" in self.identifiers_file[self.line_index]):
            typeContent = self.contentIdentifier()
            self.nextIdentifier()
            if("IDE" in self.identifiers_file[self.line_index]):
                typeContent += ' '+self.contentIdentifier()
                self.nextIdentifier()
            else:
                if("DEL ;" in self.identifiers_file[self.line_index]):
                    while("DEL ;" in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
                    self.exception("';' DUPLICADOS")
                self.exception("ESPERADO 'int' OU 'real' OU 'boolean' OU 'string' OU 'struct'")
                while(not 'IDE' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
        else:
            if("DEL ;" in self.identifiers_file[self.line_index]):
                while("DEL ;" in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                self.exception("';' DUPLICADOS")
            self.exception("ESPERADO 'int' OU 'real' OU 'boolean' OU 'string' OU 'struct' OU 'local.' OU 'global.'")
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
                        # not 'DEL }' in self.identifiers_file[self.line_index] or
                        not 'IDE' in self.identifiers_file[self.line_index]
                    ):
                        # if('DEL }' in self.identifiers_file[self.line_index]):
                        #     break
                        self.nextIdentifier()
            elif('REL =' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                if(
                    'PRE true' in self.identifiers_file[self.line_index] or 
                    'PRE false' in self.identifiers_file[self.line_index] or
                    'CAD' in self.identifiers_file[self.line_index] or
                    'SIM' in self.identifiers_file[self.line_index] or
                    'NRO' in self.identifiers_file[self.line_index]
                ):
                    self.nextIdentifier()
                    if('DEL ;' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
                        if(
                            'IDE' in self.identifiers_file[self.line_index]
                        ):
                            var_globals.update(self.VariablesList())
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
                    self.exception("ESPERADO UM VALOR APOS '='")
                    while(
                        not 'DEL ;' in self.identifiers_file[self.line_index] or
                        not 'PRE string' in self.identifiers_file[self.line_index] or
                        not 'PRE real' in self.identifiers_file[self.line_index] or
                        not 'PRE int' in self.identifiers_file[self.line_index] or
                        not 'PRE char' in self.identifiers_file[self.line_index] or
                        not 'PRE boolean' in self.identifiers_file[self.line_index] or
                        not 'IDE' in self.identifiers_file[self.line_index]
                    ):
                        self.nextIdentifier()
            elif(
                'ART + ' in self.identifiers_file[self.line_index] or
                'ART - ' in self.identifiers_file[self.line_index] or
                'ART /' in self.identifiers_file[self.line_index] or
                'ART *' in self.identifiers_file[self.line_index]
                ):
                print("TRO AQIOOOOOOOOOOOOOOOOOOOOO", self.contentIdentifier())
                self.nextIdentifier()
                if('REL =' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                    if(
                        'PRE true' in self.identifiers_file[self.line_index] or 
                        'PRE false' in self.identifiers_file[self.line_index] or
                        'CAD' in self.identifiers_file[self.line_index] or
                        'SIM' in self.identifiers_file[self.line_index] or
                        'NRO' in self.identifiers_file[self.line_index]
                    ):
                        self.nextIdentifier()
                        if('DEL ;' in self.identifiers_file[self.line_index]):
                            self.nextIdentifier()
                            if(
                                'IDE' in self.identifiers_file[self.line_index]
                            ):
                                var_globals.update(self.VariablesList())
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
                        self.exception("ESPERADO UM VALOR APOS '='")
                        while(
                            not 'DEL ;' in self.identifiers_file[self.line_index] or
                            not 'PRE string' in self.identifiers_file[self.line_index] or
                            not 'PRE real' in self.identifiers_file[self.line_index] or
                            not 'PRE int' in self.identifiers_file[self.line_index] or
                            not 'PRE char' in self.identifiers_file[self.line_index] or
                            not 'PRE boolean' in self.identifiers_file[self.line_index] or
                            not 'IDE' in self.identifiers_file[self.line_index]
                        ):
                            self.nextIdentifier()
                else:
                    self.exception("ESPERADO IDENTIFICACAO DO TIPO DO BLOCO OU ATRIBUICAO DE VALOR")
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
            'PRE local' in self.identifiers_file[self.line_index] or
            'PRE global' in self.identifiers_file[self.line_index] or
            'PRE boolean' in self.identifiers_file[self.line_index]
        ):
            decl = self.Decl()
            key = list(decl.keys())
            var_globals[key[0]] = var_globals_content
            var_globals_content.append(decl[key[0]])
            
            if('DEL ;' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                if(not 'DEL }' in self.identifiers_file[self.line_index]):
                    var_globals.update(self.VariablesList())
                else:
                    return var_globals
            elif('REL =' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                if(
                    'PRE true' in self.identifiers_file[self.line_index] or 
                    'PRE false' in self.identifiers_file[self.line_index] or
                    'CAD' in self.identifiers_file[self.line_index] or
                    'SIM' in self.identifiers_file[self.line_index] or
                    'NRO' in self.identifiers_file[self.line_index]
                ):
                    self.nextIdentifier()
                    if('DEL ;' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
                        if(not 'DEL }' in self.identifiers_file[self.line_index]):
                            var_globals.update(self.VariablesList())
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
            elif(
                'ART + ' in self.identifiers_file[self.line_index] or
                'ART - ' in self.identifiers_file[self.line_index] or
                'ART /' in self.identifiers_file[self.line_index] or
                'ART *' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
                if('REL =' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                    if(
                        'PRE true' in self.identifiers_file[self.line_index] or 
                        'PRE false' in self.identifiers_file[self.line_index] or
                        'CAD' in self.identifiers_file[self.line_index] or
                        'SIM' in self.identifiers_file[self.line_index] or
                        'NRO' in self.identifiers_file[self.line_index]
                    ):
                        self.nextIdentifier()
                        if('DEL ;' in self.identifiers_file[self.line_index]):
                            self.nextIdentifier()
                            if(not 'DEL }' in self.identifiers_file[self.line_index]):
                                var_globals.update(self.VariablesList())
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
                        self.exception("ESPERADO UM VALOR APOS '='")
                        while(
                            not 'DEL ;' in self.identifiers_file[self.line_index] or
                            not 'PRE string' in self.identifiers_file[self.line_index] or
                            not 'PRE real' in self.identifiers_file[self.line_index] or
                            not 'PRE int' in self.identifiers_file[self.line_index] or
                            not 'PRE char' in self.identifiers_file[self.line_index] or
                            not 'PRE boolean' in self.identifiers_file[self.line_index] or
                            not 'IDE' in self.identifiers_file[self.line_index]
                        ):
                            self.nextIdentifier()
                else:
                    self.exception("ESPERADO IDENTIFICACAO DO TIPO DO BLOCO OU ATRIBUICAO DE VALOR")
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
        elif("PRE struct" in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            if("IDE" in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                # var_globals.update(self.VariablesList())
                # decl = self.Decl()
                # key = list(decl.keys())
                # var_globals[key[0]] = var_globals_content
                # var_globals_content.append(decl[key[0]])
                
                if('DEL ;' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                    if(not 'DEL }' in self.identifiers_file[self.line_index]):
                        var_globals.update(self.VariablesList())
                    else:
                        return var_globals
                elif('IDE' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                    if('DEL [' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
                        if('IDE' in self.identifiers_file[self.line_index]):
                            self.nextIdentifier()
                            if('DEL ]' in self.identifiers_file[self.line_index]):
                                self.nextIdentifier()
                                if('DEL ;' in self.identifiers_file[self.line_index]):
                                    self.nextIdentifier()
                                    return var_globals
                                else:
                                    self.exception("ESPERADO ';'")
                                    while(
                                        not 'PRE string' in self.identifiers_file[self.line_index] or
                                        not 'PRE real' in self.identifiers_file[self.line_index] or
                                        not 'PRE int' in self.identifiers_file[self.line_index] or
                                        not 'PRE char' in self.identifiers_file[self.line_index] or
                                        not 'PRE boolean' in self.identifiers_file[self.line_index] or
                                        not 'PRE struct' in self.identifiers_file[self.line_index] or
                                        not 'IDE' in self.identifiers_file[self.line_index]
                                    ):
                                        self.nextIdentifier()
                            else:
                                self.exception("ESPERADO ';'")
                                while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                                    self.nextIdentifier()
                        else:
                            self.exception("ESPERADO NUMERO OU VARIAVEL NA MATRIX/VETOR")
                            while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                                self.nextIdentifier()
                    elif('DEL ;' in self.identifiers_file[self.line_index]):
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
                            not 'PRE struct' in self.identifiers_file[self.line_index] or
                            not 'IDE' in self.identifiers_file[self.line_index]
                        ):
                            self.nextIdentifier()
                else:
                    self.exception("ESPERADO ';' OU IDENTIFICADOR")
                    while(
                        not 'PRE string' in self.identifiers_file[self.line_index] or
                        not 'PRE real' in self.identifiers_file[self.line_index] or
                        not 'PRE int' in self.identifiers_file[self.line_index] or
                        not 'PRE char' in self.identifiers_file[self.line_index] or
                        not 'PRE boolean' in self.identifiers_file[self.line_index] or
                        not 'PRE struct' in self.identifiers_file[self.line_index] or
                        not 'IDE' in self.identifiers_file[self.line_index]
                    ):
                        self.nextIdentifier()
            else:
                self.exception("ESPERADO TIPO DA STRUCT")
                while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
        elif('DEL [' in self.identifiers_file[self.line_index]):
            self.MatrixCall()
        else:
            if('DEL ;' in self.identifiers_file[self.line_index]):
                while('DEL ;' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                self.exception("';' DUPLICADO")
            self.exception("ESPERADO 'string' ou 'int' ou 'real' ou 'boolean' ou 'struct'")
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
        self.hasException()
        return_identifier = []
        vector_matrix = 0
        
        if('DEL ;' in self.identifiers_file[self.line_index]):
            return return_identifier
        elif('DEL [' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            if('NRO' in self.identifiers_file[self.line_index]):
                vector_large = self.contentIdentifier()
                self.nextIdentifier()
                if('DEL ]' in self.identifiers_file[self.line_index]):
                    return_matrix = self.Matrix()
                    if(return_matrix > 0):
                        vector_matrix = 2
                        return_identifier.append(vector_matrix)
                        return_identifier.append(vector_large)
                        return_identifier.append(return_matrix)
                    else:
                        vector_matrix = 1
                        return_identifier.append(vector_matrix)
                        return_identifier.append(vector_large)
                else:
                    self.exception("COLCHETES DECLARADOS DE FORMA INCORRETA")
                    while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
            else:
                self.exception("ESPERADO NUMERO INTEIRO")
                while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
        elif('REL =' in self.identifiers_file[self.line_index]):
            init_value = self.Init()
            return_identifier.append(vector_matrix)
            return_identifier.append(init_value)
        else:
            self.exception("ESPERADO '=' ou '['")
            while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
        return return_identifier
        
    def Matrix(self): # matriz
        self.hasException()
        
        if('DEL ;' in self.identifiers_file[self.line_index]):
            return -1
        elif('DEL [' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            if('NRO' in self.identifiers_file[self.line_index]):
                matrix_height = self.contentIdentifier()
                self.nextIdentifier()
                if('DEL ]' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                    return matrix_height
                else:
                    self.exception("COLCHETES DECLARADOS DE FORMA INCORRETA")
                    while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
            else:
                self.exception("ESPERADO NUMERO INTEIRO")
                while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
        else:
            self.exception("ESPERADO '='")
            while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
    
    def Init(self): # inicializacao
        self.nextIdentifier()
        
        if("DEL ;" in self.identifiers_file[self.line_index]):
            return
        elif('REL =' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            return self.Value()
            
    def FunctionDeclaration(self):
        self.hasException()
        func_table = {}
        func_content = []
        func_params = []
        isProcedure = False
        
        if("PRE start" in self.identifiers_file[self.line_index]):
            return func_table
        elif("PRE function" in self.identifiers_file[self.line_index] or "PRE procedure" in self.identifiers_file[self.line_index]):
            if("PRE function" in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                func_content.append(self.ReturnType())
            else:
                self.nextIdentifier()
                isProcedure = True
            
            if('IDE' in self.identifiers_file[self.line_index]):
                func_name = self.contentIdentifier()
                func_table[func_name] = func_content
                self.nextIdentifier()
                if('DEL (' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                    if(not 'DEL )' in self.identifiers_file[self.line_index]):
                        func_params = self.Params()
                    if('DEL )' in self.identifiers_file[self.line_index]):
                        func_content.append(func_params)
                        self.nextIdentifier()
                        if('DEL {' in self.identifiers_file[self.line_index]):
                            self.nextIdentifier()
                            if(not 'DEL }' in self.identifiers_file[self.line_index]):
                                self.FunctionParam(isProcedure)
                            if('DEL }' in self.identifiers_file[self.line_index]):
                                self.nextIdentifier()
                                func_table.update(self.FunctionDeclaration())
                            elif('IDE' in self.identifiers_file[self.line_index]):
                                self.FunctionCall()
                                self.nextIdentifier()
                                if('DEL ;' in self.identifiers_file[self.line_index]):
                                    self.nextIdentifier()
                                
                                if('PRE return' in self.identifiers_file[self.line_index]):
                                    self.nextIdentifier()
                                    
                                    if(
                                        'IDE' in self.identifiers_file[self.line_index] or
                                        'NRO' in self.identifiers_file[self.line_index] or
                                        'CAD' in self.identifiers_file[self.line_index] or
                                        'SIM' in self.identifiers_file[self.line_index] or
                                        'PRE true' in self.identifiers_file[self.line_index] or
                                        'PRE false' in self.identifiers_file[self.line_index]
                                    ):
                                        self.nextIdentifier()
                                    if('DEL ;' in self.identifiers_file[self.line_index]):
                                        self.nextIdentifier()
                                    else:
                                        self.exception("ESPARADO ';'")
                                        while(not 'DEL }' in self.identifiers_file[self.line_index]):
                                            self.nextIdentifier()
                                    # return
                                if('DEL }' in self.identifiers_file[self.line_index]):
                                    self.nextIdentifier()
                                    print("LLLLLLLLLLLLLLLLLLLLLLLLLL", self.contentIdentifier(), self.line_index)
                                    
                                    if('PRE function' in self.identifiers_file[self.line_index] or 'PRE procedure' in self.identifiers_file[self.line_index]):
                                        self.FunctionDeclaration()
                            else:
                                self.exception("ESPERADO '}'")
                                while(not 'PRE start' in self.identifiers_file[self.line_index] or not 'PRE function' in self.identifiers_file[self.line_index] or not "PRE procedure" in self.identifiers_file[self.line_index]):
                                    self.nextIdentifier()
                        else:
                            self.exception("ESPERADO '{'")
                            while(not 'PRE start' in self.identifiers_file[self.line_index] or not 'PRE function' in self.identifiers_file[self.line_index] or not "PRE procedure" in self.identifiers_file[self.line_index]):
                                self.nextIdentifier()
                    else:
                        self.exception("ESPERADO ')'")
                        while(not 'PRE start' in self.identifiers_file[self.line_index] or not 'PRE function' in self.identifiers_file[self.line_index] or not "PRE procedure" in self.identifiers_file[self.line_index]):
                            self.nextIdentifier()
                else:
                    self.exception("ESPERADO '('")
                    while('PRE start' in self.identifiers_file[self.line_index] or 'PRE function' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
                    while(not 'PRE start' in self.identifiers_file[self.line_index] or not 'PRE function' in self.identifiers_file[self.line_index] or not "PRE procedure" in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
            else:
                self.exception("ESPERADO UM IDENTIFICADOR")
                while(not 'PRE start' in self.identifiers_file[self.line_index] or not 'PRE function' in self.identifiers_file[self.line_index] or not "PRE procedure" in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
        else:
            self.exception("ESPERADO '{'")
            if('PRE start' in self.identifiers_file[self.line_index] or 'PRE function' in self.identifiers_file[self.line_index] or "PRE procedure" in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
            while(not 'PRE start' in self.identifiers_file[self.line_index] or not 'PRE function' in self.identifiers_file[self.line_index] or not "PRE procedure" in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
        return func_table
    
    def ReturnType(self): # tipo_return TIRAMOS UMA PARTE DO COD ORIGIN
        self.hasException()
        
        return_type = []
        
        if('IDE' in self.identifiers_file[self.line_index]):
            return_type.append(self.contentIdentifier())
            return_type.append("struct")
            self.nextIdentifier()
        elif(
            #'PRE ' in self.identifiers_file[self.line_index] or
            'PRE real' in self.identifiers_file[self.line_index] or
            'PRE int' in self.identifiers_file[self.line_index] or
            'PRE string' in self.identifiers_file[self.line_index] or
            'PRE boolean' in self.identifiers_file[self.line_index]
        ):
            return_type.append(self.Type())
            vector_matrix = self.MatrixIdentifier()
            if(vector_matrix == 0):
                return_type.append('simple')
            elif(vector_matrix == 1):
                return_type.append('vector')
            elif(vector_matrix == 2):
                return_type.append('matrix')
        else:
            self.exception('ESPERADO RETORNO')
            while(not 'IDE' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
        return return_type
    
    def Params(self): # decl_param
        self.hasException()
        params = []
        params_list = []
        
        if('IDE' in self.identifiers_file[self.line_index]):
            param_type = self.contentIdentifier()
            self.nextIdentifier()
            if('IDE' in self.identifiers_file[self.line_index]):
                param_name = self.contentIdentifier()
                params_list.append(param_name)
                params_list.append(param_type)
                params_list.append("struct")
                params.append(params_list)
                self.nextIdentifier()
                params += self.Param()
            else:
                self.exception("ESPERADO UM IDENTIFICADOR")
                while(not 'DEL ,' in self.identifiers_file[self.line_index] or not 'DEL )' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
        elif(
            'PRE CADEIA' in self.identifiers_file[self.line_index] or
            'PRE real' in self.identifiers_file[self.line_index] or
            'PRE int' in self.identifiers_file[self.line_index] or
            'PRE string' in self.identifiers_file[self.line_index] or
            'PRE boolean' in self.identifiers_file[self.line_index]
        ):
            decl = self.Decl()
            param_name = list(decl.keys())
            params_list.append(param_name[0])
            params_list.append(decl[param_name[0]])
            
            vector_matrix = self.MatrixIdentifier()
            if(vector_matrix == 0):
                params_list.append('simple')
            elif(vector_matrix == 1):
                params_list.append('vector')
            elif(vector_matrix == 2):
                params_list.append('matrix')
            params.append(params_list)
            params += self.Param()
        else:
            self.exception("ESPERADO UM TIPO")
            while(not 'DEL ,' in self.identifiers_file[self.line_index] or not 'DEL )' in self.identifiers_file[self.line_index]):
                self.nextIdentifier
        return params
    
    def MatrixIdentifier(self): # identificador_param_deriva
        self.hasException()
        vector_matrix = 0
        
        if(
            'DEL ,' in self.identifiers_file[self.line_index] or
            'DEL )' in self.identifiers_file[self.line_index] or
            'IDE' in self.identifiers_file[self.line_index] 
        ):
            return vector_matrix
        elif('DEL [' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            if('DEL ]' in self.identifiers_file[self.line_index]):
                vector_matrix = 1
                self.nextIdentifier()
                vector_matrix += self.MatrixParam()
            else:
                self.exception("ESPERADO ']'")
                while(
                    not 'DEL ,' in self.identifiers_file[self.line_index] or
                    not 'DEL )' in self.identifiers_file[self.line_index] or
                    not 'IDE' in self.identifiers_file[self.line_index]
                ):
                    self.nextIdentifier()
        else:
            self.exception("ESPERADO '['")
            while(
                not 'DEL ,' in self.identifiers_file[self.line_index] or
                not 'DEL )' in self.identifiers_file[self.line_index] or
                not 'IDE' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
        return vector_matrix
    
    def MatrixParam(self): # matriz_param
        self.hasException()
        return_matrix = 0
        
        if(
            'DEL ,' in self.identifiers_file[self.line_index] or 
            'DEL )' in self.identifiers_file[self.line_index] or 
            'IDE' in self.identifiers_file[self.line_index]
        ):
            return return_matrix
        elif('DEL [' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            if('DEL ]' in self.identifiers_file[self.line_index]):
                return_matrix = 1
                self.nextIdentifier()
            else:
                self.exception("ESPERADO ']'")
                while(
                    not 'DEL ,' in self.identifiers_file[self.line_index] or
                    not 'DEL )' in self.identifiers_file[self.line_index] or
                    not 'IDE' in self.identifiers_file[self.line_index]
                ):
                    self.nextIdentifier()
        else:
            self.exception("ESPERADO '['")
            while(
                not 'DEL ,' in self.identifiers_file[self.line_index] or
                not 'DEL )' in self.identifiers_file[self.line_index] or
                not 'IDE' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
        return return_matrix
    
    def Param(self): # deriva_param
        self.hasException()
        return_param = []
        
        if('DEL )' in self.identifiers_file[self.line_index]):
            return return_param
        elif('DEL ,' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            return_param += self.Params()
        return return_param 
    
    def FunctionParam(self, isProcedure): # deriva_cont_funcao
        self.hasException()
        
        if('PRE var' in self.identifiers_file[self.line_index]):
            local_vars = self.VarDecl()
            self.PreDecls()
            if(
                'PRE if' in self.identifiers_file[self.line_index] or
                'PRE print' in self.identifiers_file[self.line_index] or
                'PRE read' in self.identifiers_file[self.line_index] or
                'PRE while' in self.identifiers_file[self.line_index] or
                'PRE for' in self.identifiers_file[self.line_index] or
                'DEL' in self.identifiers_file[self.line_index]
            ):
                self.PreDecls()
                if('PRE return' in self.identifiers_file[self.line_index] or 'DEL }' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                else:
                    self.exception("ESPERADO 'return'")
                    while(not 'DEL }' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
            elif('PRE return' in self.identifiers_file[self.line_index] and not isProcedure):
                self.nextIdentifier()
                self.Return()
                if('DEL ;' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                else:
                    self.exception("ESPERADO ';'")
                    while(not 'DEL }' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
            elif(not isProcedure):
                self.exception("ESPERADO 'return'")
                while(not 'DEL }' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
        elif(
            'PRE if' in self.identifiers_file[self.line_index] or
            'PRE print' in self.identifiers_file[self.line_index] or
            'PRE read' in self.identifiers_file[self.line_index] or
            'PRE while' in self.identifiers_file[self.line_index] or
            'PRE for' in self.identifiers_file[self.line_index] or
            'DEL' in self.identifiers_file[self.line_index]
        ):
            self.PreDecls()
            if('PRE return' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
            else:
                self.exception("ESPERADO 'return'")
                while(not 'DEL }' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
        else:
            self.exception("ESPERADO BLOCO DE VARIAVEIS")
            while(not 'DEL }' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                
                
    def Return(self): # return_deriva TIRAMOS UMA PARTE DO COD ORIGIN
        self.hasException()
        
        if('IDE' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            self.Reserved() # ALTERAR NOVO NOME
        if('PRE true' in self.identifiers_file[self.line_index] or 'PRE false' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
        elif(
            'PRE string' in self.identifiers_file[self.line_index] or
            'PRE real' in self.identifiers_file[self.line_index] or
            'PRE int' in self.identifiers_file[self.line_index] or
            'PRE boolean' in self.identifiers_file[self.line_index]
        ):
            self.Value()
        else:
            self.exception("ESPERADO RETORNO DA FUNCAO")
            while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
    
    def PreDecls(self): # decl_comandos
        self.hasException()
        if('PRE return' in self.identifiers_file[self.line_index] or 'DEL }' in self.identifiers_file[self.line_index]):
            return
        elif(
            'PRE if' in self.identifiers_file[self.line_index] or
            'PRE print' in self.identifiers_file[self.line_index] or
            'PRE read' in self.identifiers_file[self.line_index] or
            'PRE while' in self.identifiers_file[self.line_index] or
            'PRE for' in self.identifiers_file[self.line_index]
        ):
            self.Cmd()
            self.PreDecls()
        elif(
            'PRE local' in self.identifiers_file[self.line_index] or
            'PRE global' in self.identifiers_file[self.line_index]
        ):
            self.VariablesList()
        elif('IDE' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            if('DEL .' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                self.VariablesList()
            else:
                # self.nextIdentifier()
                # self.previousIdentifier()
                self.previousIdentifier()
                # if('DEL ')
                # print("_________TENAT AQUI", self.contentIdentifier(), self.line_index)
                self.FunctionCall()
            
        else:
            self.exception("ESPERADO ATRIBUICAO")
            while(
                not 'PRE return' in self.identifiers_file[self.line_index] or
                not 'DEL }' in self.identifiers_file[self.line_index] or
                not 'PRE if' in self.identifiers_file[self.line_index] or
                not 'PRE print' in self.identifiers_file[self.line_index] or
                not 'PRE read' in self.identifiers_file[self.line_index] or
                not 'PRE while' in self.identifiers_file[self.line_index] or
                not 'PRE for' in self.identifiers_file[self.line_index] or
                not 'IDE' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
    
    def Cmd(self): # comandos
        self.hasException()
        
        if('PRE if' in self.identifiers_file[self.line_index]):
            self.If()
        elif('PRE print' in self.identifiers_file[self.line_index]):
            self.Print()
        elif('PRE read' in self.identifiers_file[self.line_index]):
            self.Read()
        elif('PRE while' in self.identifiers_file[self.line_index]):
            self.While()
        elif('PRE for' in self.identifiers_file[self.line_index]):
            self.For()
        elif('IDE' in self.identifiers_file[self.line_index]):
            self.Assign()
        else:
            self.exception("ESPERADO UMA ATRIBUICAO")
            while(
                not 'PRE if' in self.identifiers_file[self.line_index] or
                not 'PRE print' in self.identifiers_file[self.line_index] or
                not 'PRE read' in self.identifiers_file[self.line_index] or
                not 'PRE while' in self.identifiers_file[self.line_index] or
                not 'PRE for' in self.identifiers_file[self.line_index] or
                not 'PRE return' in self.identifiers_file[self.line_index] or
                not 'DEL }' in self.identifiers_file[self.line_index] or
                not 'IDE' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
                
    def Assign(self): # atribuicao
        self.hasException()
        
        if('IDE' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            self.Reserved()
            if('REL =' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                self.Assigns()
                if('DEL ;' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                else:
                    self.exception("ESPERADO ';'")
                    while(
                        not 'PRE if' in self.identifiers_file[self.line_index] or
                        not 'PRE print' in self.identifiers_file[self.line_index] or
                        not 'PRE read' in self.identifiers_file[self.line_index] or
                        not 'PRE while' in self.identifiers_file[self.line_index] or
                        not 'PRE for' in self.identifiers_file[self.line_index] or
                        not 'PRE return' in self.identifiers_file[self.line_index] or
                        not 'DEL }' in self.identifiers_file[self.line_index] or
                        not 'IDE' in self.identifiers_file[self.line_index]
                    ):
                        self.nextIdentifier()
            else:
                self.exception("ESPERADO '='")
                while(
                    not 'PRE if' in self.identifiers_file[self.line_index] or
                    not 'PRE print' in self.identifiers_file[self.line_index] or
                    not 'PRE read' in self.identifiers_file[self.line_index] or
                    not 'PRE while' in self.identifiers_file[self.line_index] or
                    not 'PRE for' in self.identifiers_file[self.line_index] or
                    not 'PRE return' in self.identifiers_file[self.line_index] or
                    not 'DEL }' in self.identifiers_file[self.line_index] or
                    not 'IDE' in self.identifiers_file[self.line_index]
                ):
                    self.nextIdentifier()        
        else:
            self.exception("ESPERADO UMA VARIAVEL")
            while(
                not 'PRE if' in self.identifiers_file[self.line_index] or
                not 'PRE print' in self.identifiers_file[self.line_index] or
                not 'PRE read' in self.identifiers_file[self.line_index] or
                not 'PRE while' in self.identifiers_file[self.line_index] or
                not 'PRE for' in self.identifiers_file[self.line_index] or
                not 'PRE return' in self.identifiers_file[self.line_index] or
                not 'DEL }' in self.identifiers_file[self.line_index] or
                not 'IDE' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()     
                   
    def Assigns(self): # atribuicao_deriva
        self.hasException()
        
        if('IDE' in self.identifiers_file[self.line_index]):
            self.FunctionCall()
        elif(
            'DEL (' in self.identifiers_file[self.line_index] or
            'ART +' in self.identifiers_file[self.line_index] or
            'ART -' in self.identifiers_file[self.line_index] or
            'IDE' in self.identifiers_file[self.line_index] or
            'NRO' in self.identifiers_file[self.line_index]
        ):
            self.Exp()
        else:
            self.exception("ESPERADO EXPRESSAO ARITMETICA")
            while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                
    def FunctionCall(self): # chamada_funcao
        self.hasException()
        
        if('IDE' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            if('DEL (' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                self.ParamCall()
                if('DEL )' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                else:
                    self.exception("ESPERADO ')'")
                    while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
            else:
                self.exception("ESPERADO '('")
                while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
        else:
            self.previousIdentifier()
            
            self.exception("ESPERADO IDENTIFICADOR")
            while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                
    def ParamCall(self): # decl_param_chamada
        self.hasException()
        
        if('DEL )' in self.identifiers_file[self.line_index]):
            return
        elif(
            'IDE' in self.identifiers_file[self.line_index] or
            'CAD' in self.identifiers_file[self.line_index] or
            'SIM' in self.identifiers_file[self.line_index] or
            'NRO' in self.identifiers_file[self.line_index] or
            'PRE true' in self.identifiers_file[self.line_index] or
            'PRE false' in self.identifiers_file[self.line_index]
        ):
            self.DeclCall()
            self.ParamsCall()
        else:
            self.exception("ESPERADO EXPRESSAO ARITMETICA")
            while(not 'DEL ,' in self.identifiers_file[self.line_index] or not 'DEL )' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                
    def DeclCall(self): # decl_chamada
        self.hasException()
        
        if('IDE' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            self.Reserved()
        elif(
            'NRO' in self.identifiers_file[self.line_index] or 
            'CAD' in self.identifiers_file[self.line_index] or 
            'PRE true' in self.identifiers_file[self.line_index] or 
            'PRE false' in self.identifiers_file[self.line_index] or 
            'SIM' in self.identifiers_file[self.line_index]
        ):
            self.Value()
        else:
            self.exception("ESPERADO VALOR OU STRUCT OU MATRIX OU VETOR")
            while(not 'DEL ,' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
    
    def ParamsCall(self): # chamada_param_deriva
        self.hasException()
        
        if('DEL )' in self.identifiers_file[self.line_index]):
            return
        elif('DEL ,' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            self.ParamCall()
        else:
            self.exception("ESPERADO ','")
            while(not 'DEL ,' in self.identifiers_file[self.line_index] or not 'DEL )' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
    
    def Reserved(self): # identificador_imp_arm_deriva
        self.hasException()
        
        if(
            'DEL ;' in self.identifiers_file[self.line_index] or
            'REL =' in self.identifiers_file[self.line_index] or
            'DEL ,' in self.identifiers_file[self.line_index] or
            'DEL (' in self.identifiers_file[self.line_index] or
            'DEL )' in self.identifiers_file[self.line_index] or
            'ART +' in self.identifiers_file[self.line_index] or
            'ART -' in self.identifiers_file[self.line_index] or
            'ART *' in self.identifiers_file[self.line_index] or
            'ART /' in self.identifiers_file[self.line_index] or
            'ART ++' in self.identifiers_file[self.line_index] or
            'ART --' in self.identifiers_file[self.line_index] or
            'REL ==' in self.identifiers_file[self.line_index] or
            'REL !=' in self.identifiers_file[self.line_index] or
            'REL >' in self.identifiers_file[self.line_index] or
            'REL >=' in self.identifiers_file[self.line_index] or
            'REL <' in self.identifiers_file[self.line_index] or
            'REL <=' in self.identifiers_file[self.line_index] or
            'LOG &&' in self.identifiers_file[self.line_index] or
            'LOG ||' in self.identifiers_file[self.line_index] or
            'CAD' in self.identifiers_file[self.line_index] or
            'SIM' in self.identifiers_file[self.line_index] or
            'IDE' in self.identifiers_file[self.line_index] or
            'NRO' in self.identifiers_file[self.line_index] or
            'PRE string' in self.identifiers_file[self.line_index] or
            'PRE real' in self.identifiers_file[self.line_index] or
            'PRE int' in self.identifiers_file[self.line_index] or
            'PRE boolean' in self.identifiers_file[self.line_index]
        ):
            return
        elif('DEL .' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            if('IDE' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
        elif('DEL [' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            self.Index()
            if('DEL ]' in self.identifiers_file[self.line_index]):
                self.nextIndentifier()
                self.MatrixCall()
            else:
                self.exception("ESPERADO ']'")
                while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
        else:
            self.exception("ESPERADO ']' ou '.'")
            while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
    
    def MatrixCall(self): # matriz_chamada
        self.hasException()
        
        if('DEL ;' in self.identifiers_file[self.line_index]):
            return
        elif('DEL [' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            self.Index()
            if('DEL ]' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
            else:
                self.exception("ESPERADO ']'")
                while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
        else:
            self.nextIdentifier("ESPERADO '['")
            while(not 'DEL ;' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
    
    def Index(self):
        self.hasException()
        
        if('DEL ]' in self.identifiers_file[self.line_index]):
            return
        if('NRO' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
        else:
            self.exception("ESPERADO INDICE DO VETOR/MATRIZ")
            while(not 'DEL ]' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
    
    def If(self): # se_declaracao
        self.hasException()
        hasErro = False
        
        if('PRE if' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            if('DEL (' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                self.ConditionalExpression()
                if('DEL )' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                    if('PRE then' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
                        if('DEL {' in self.identifiers_file[self.line_index]):
                            self.nextIdentifier()
                            self.PreDecls()
                            if('PRE if' in self.identifiers_file[self.line_index]):
                                self.If()
                            if('DEL }' in self.identifiers_file[self.line_index]):
                                self.nextIdentifier()
                                self.Else()
                            else:
                                self.exception("ESPERADO '}'")
                                hasErro = True
                        else:
                            self.exception("ESPERADO '{'")
                            hasErro = True
                    else:
                        self.exception("ESPERADO 'then' APOS A DECLARACAO DA CONDICIONAL")
                        hasErro = True
                else:
                    self.exception("ESPERADO ')'")
                    hasErro = True
            else:
                self.exception("ESPERADO '('")
                hasErro = True
        else:
            self.exception("ESPERADO '}'")
            hasErro = True
                
        if(hasErro):
            while(
                not 'PRE if' in self.identifiers_file[self.line_index] or
                not 'PRE print' in self.identifiers_file[self.line_index] or
                not 'PRE read' in self.identifiers_file[self.line_index] or
                not 'PRE while' in self.identifiers_file[self.line_index] or
                not 'PRE for' in self.identifiers_file[self.line_index] or
                not 'PRE return' in self.identifiers_file[self.line_index] or
                not 'IDE' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
    
    def Else(self): # senao_decl
        self.hasException()
        hasErro = False
        
        if(
            'DEL }' in self.identifiers_file[self.line_index] or
            'PRE if' in self.identifiers_file[self.line_index] or
            'PRE print' in self.identifiers_file[self.line_index] or
            'PRE read' in self.identifiers_file[self.line_index] or
            'PRE while' in self.identifiers_file[self.line_index] or
            'PRE for' in self.identifiers_file[self.line_index] or
            'PRE return' in self.identifiers_file[self.line_index] or
            'IDE' in self.identifiers_file[self.line_index]
        ):
            return
        elif('PRE else' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            if('DEL {' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                self.PreDecls()
                if('DEL }' in self.identifiers_file[self.line_index] or 'DEL ;' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                else:
                    # print("TA CAINDO AQUI _-_---------__-___--", self.contentIdentifier())
                    self.exception("ESPERADO '}'")
                    hasErro = True
            else:
                self.exception("ESPERADO '{'")
                hasErro = True

        else:
            self.exception("ESPERADO BLOCO DO 'else'")
            hasErro = True
        
        if(hasErro):
            while(
                not 'PRE if' in self.identifiers_file[self.line_index] or
                not 'PRE print' in self.identifiers_file[self.line_index] or
                not 'PRE read' in self.identifiers_file[self.line_index] or
                not 'PRE while' in self.identifiers_file[self.line_index] or
                not 'PRE for' in self.identifiers_file[self.line_index] or
                not 'PRE return' in self.identifiers_file[self.line_index] or
                not 'IDE' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
        
    def While(self):
        self.hasException()
        hasErro = False
        
        if('PRE while' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            if('DEL (' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                self.ConditionalExpression()
                if('DEL )' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                    if('DEL {' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
                        self.PreDecls()
                        if('DEL }' in self.identifiers_file[self.line_index]):
                            self.nextIdentifier()
                        else:
                            self.exception("ESPERADO '}'")
                            hasErro = True
                    else:
                        self.exception("ESPERADO '{'")
                        hasErro = True
                else:
                    self.exception("ESPERADO ')'")
                    hasErro = True
            else:
                self.exception("ESPERADO '('")
                hasErro = True
        else:
            self.exception("ESPERADO LAÇO 'while'")
            hasErro = True
        
        if(hasErro):
            while(
                not 'PRE if' in self.identifiers_file[self.line_index] or
                not 'PRE print' in self.identifiers_file[self.line_index] or
                not 'PRE read' in self.identifiers_file[self.line_index] or
                not 'PRE while' in self.identifiers_file[self.line_index] or
                not 'PRE for' in self.identifiers_file[self.line_index] or
                not 'PRE return' in self.identifiers_file[self.line_index] or
                not 'IDE' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
    def For(self): # para_declaracao
        self.hasException()
        hasErro = False
        hasErroIDE = False
        
        if('PRE for' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            if('DEL (' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                if('IDE' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                    if('REL =' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
                        if('NRO' in self.identifiers_file[self.line_index]):
                            self.nextIdentifier()
                            if('DEL ;' in self.identifiers_file[self.line_index]):
                                self.nextIdentifier()
                                if('IDE' in self.identifiers_file[self.line_index]):
                                    self.nextIdentifier()
                                    self.Relational()
                                    if('NRO' in self.identifiers_file[self.line_index]):
                                        self.nextIdentifier()
                                        if('DEL ;' in self.identifiers_file[self.line_index]):
                                            self.nextIdentifier()
                                            if('IDE' in self.identifiers_file[self.line_index]):
                                                self.PpMm()
                                                if('DEL )' in self.identifiers_file[self.line_index]):
                                                    self.nextIdentifier()
                                                    if('DEL {' in self.identifiers_file[self.line_index]):
                                                        self.nextIdentifier()
                                                        self.PreDecls()
                                                        if('DEL }' in self.identifiers_file[self.line_index]):
                                                            self.nextIdentifier()
                                                        else:
                                                            self.exception("ESPERADO '}'")
                                                            hasErroIDE = True
                                                    else:
                                                        self.exception("ESPERADO '{'")
                                                        hasErroIDE = True
                                                else:
                                                    self.exception("ESPERADO ')'")
                                                    hasErroIDE = True
                                            else:
                                                self.exception("ESPERADO IDENTIFICADOR")
                                                hasErro = True
                                        else:
                                            self.exception("ESPERADO ';'")
                                            hasErro = True
                                    else:
                                        self.exception("ESPERADO NUMERO NO LAÇO 'for'")
                                        hasErro = True
                                else:
                                    self.exception("ESPERADO IDENTIFICADOR")
                                    hasErroIDE = True
                            else:
                                self.exception("ESPERADO ';'")
                                hasErro = True
                        else:
                            self.exception("ESPERADO NUMERO NO LAÇO 'for'")
                            hasErro = True
                    else:
                        self.exception("ESPERADO ATRIBUICAO ('=')")
                        hasErro = True
                else:
                    self.exception("ESPERADO IDENTIFICADOR PARA PERCORRER O LAÇO 'for'")
                    hasErro = True
            else:
                self.exception("ESPERADO '('")
                hasErro = True
        else:
            self.exception("ESPERADO LAÇO 'for'")
            hasErroIDE = True
        
        if(hasErroIDE):
            while(
                not 'PRE if' in self.identifiers_file[self.line_index] or
                not 'PRE print' in self.identifiers_file[self.line_index] or
                not 'PRE read' in self.identifiers_file[self.line_index] or
                not 'PRE while' in self.identifiers_file[self.line_index] or
                not 'PRE for' in self.identifiers_file[self.line_index] or
                not 'PRE return' in self.identifiers_file[self.line_index] or
                not 'IDE' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
        if(hasErro):
            while(
                not 'PRE if' in self.identifiers_file[self.line_index] or
                not 'PRE print' in self.identifiers_file[self.line_index] or
                not 'PRE read' in self.identifiers_file[self.line_index] or
                not 'PRE while' in self.identifiers_file[self.line_index] or
                not 'PRE for' in self.identifiers_file[self.line_index] or
                not 'PRE return' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
                
    def Read(self): # leia_declaracao
        self.hasException()
        hasErro = False
        
        if('PRE read' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            if('DEL (' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                self.FormalParameterListRead()
                if('DEL )' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                    if('DEL ;' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
                    else:
                        self.exception("ESPERADO ';'")
                        hasErro = True
                else:
                    self.exception("ESPERADO ')'")
                    hasErro = True
            else:
                self.exception("ESPERADO '('")
                hasErro = True
        else:
            self.exception("ESPERADO 'read'")
            hasErro = True
        
        if(hasErro):
            while(
                not 'PRE if' in self.identifiers_file[self.line_index] or
                not 'PRE print' in self.identifiers_file[self.line_index] or
                not 'PRE read' in self.identifiers_file[self.line_index] or
                not 'PRE while' in self.identifiers_file[self.line_index] or
                not 'PRE for' in self.identifiers_file[self.line_index] or
                not 'PRE return' in self.identifiers_file[self.line_index] or
                not 'IDE' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
    
    def FormalParameterListRead(self): # exp_leia
        self.hasException()
        
        if('DEL )' in self.identifiers_file[self.line_index]):
            return
        elif('IDE' in self.identifiers_file[self.line_index]):
            self.AuxRead1()
            self.AuxRead2()
            self.FormalParameterListRead()
        else:
            self.exception("ESPERADO IDENTIFICADOR")
            while(not 'DEL )' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
    
    def AuxRead1(self): # exp_armazena
        self.hasException()
        
        if('IDE' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            self.Reserved()
        else:
            self.exception("ESPERADO IDENTIFICADOR")
            while(not 'DEL )' in self.identifiers_file[self.line_index] or 'DEL ,' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
    
    def AuxRead2(self): # exp_leia_deriva
        self.hasException()
        
        if('DEL )' in self.identifiers_file[self.line_index]):
            return
        elif('DEL ,' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            self.AuxRead1()
        else:
            self.exception("ESPERADO ','")
            while(not 'DEL )' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
    
    def Print(self): # escreva_declaracao
        self.hasException()
        hasError = False
        
        if('PRE print' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            if('DEL (' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                self.AuxExpPrint()
                if('DEL )' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                    if('DEL ;' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
                    else:
                        self.exception("ESPERADO ';'")
                        hasError = True
                else:
                    self.exception("ESPERADO ')'")
                    hasError = True
            else:
                self.exception("ESPERADO '('")
                hasError = True
        else:
            self.exception("ESPERADO 'print'")
            hasError = True
        
        if(hasError):
            while(
                not 'PRE if' in self.identifiers_file[self.line_index] or
                not 'PRE print' in self.identifiers_file[self.line_index] or
                not 'PRE read' in self.identifiers_file[self.line_index] or
                not 'PRE while' in self.identifiers_file[self.line_index] or
                not 'PRE for' in self.identifiers_file[self.line_index] or
                not 'PRE return' in self.identifiers_file[self.line_index] or
                not 'IDE' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
    
    def AuxExpPrint(self): # exp_escreva
        self.hasException()
        
        if('DEL )' in self.identifiers_file[self.line_index]):
            return
        elif(
            'CAD' in self.identifiers_file[self.line_index] or
            'SIM' in self.identifiers_file[self.line_index] or
            'IDE' in self.identifiers_file[self.line_index] or
            '(' in self.identifiers_file[self.line_index]  
        ):
            self.AuxExpPrint3()
            self.AuxExpPrint2() # CASO DER MERDA TIRA AQUI
            self.AuxExpPrint()
        else:
            self.exception("ESPERADO IDENTIFICADOR OU CADEIA DE CARACTERES")
            while(not 'DEL )' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
        
    def AuxExpPrint2(self): # exp_escreva_deriva
        self.hasException()
        
        if('DEL )' in self.identifiers_file[self.line_index]):
            return
        elif('DEL ,' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            self.AuxExpPrint3()
        else:
            self.exception("ESPERADO ','")
            while(not 'DEL )' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
    
    def AuxExpPrint3(self): # exp_imprime
        self.hasException()
        hasError = False
        
        if(
            'CAD' in self.identifiers_file[self.line_index] or
            'SIM' in self.identifiers_file[self.line_index]
        ):
            self.nextIdentifier()
        elif('IDE' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            self.Reserved()
        elif('DEL (' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            self.AddExp()
            if('DEL )' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
            else:
                self.exception("ESPERADO ')'")
                hasError = True
        else:
            self.exception("ESPERADO '('")
            hasError = True
        
        if(hasError):
            while(not 'DEL )' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
        
    def ConditionalExpression(self): # exp_rel_bol
        self.hasException()
        
        if(
            'IDE' in self.identifiers_file[self.line_index] or
            'NRO' in self.identifiers_file[self.line_index] or
            'DEL (' in self.identifiers_file[self.line_index]
        ):
            # if('IDE' in self.identifiers_file[self.line_index]):
                # self.nextIdentifier()
                # if('DEL .' in self.identifiers_file[self.line_index]):
                #     self.nextIdentifier()
                # else:
                #     self.previousIdentifier()
            self.LogicalExpression()
            self.Relational()
            self.LogicalExpression()
            self.RelationalExpression()
        else:
            self.exception("ESPERADO IDENTIFICADOR, NUMERO OU '('")
            while(not 'DEL )' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
    
    def LogicalExpression(self): # exp_boll
        self.hasException()
        
        if(
            'IDE' in self.identifiers_file[self.line_index] or
            'NRO' in self.identifiers_file[self.line_index] or
            'CAD' in self.identifiers_file[self.line_index] or
            'SIM' in self.identifiers_file[self.line_index] or
            'DEL (' in self.identifiers_file[self.line_index]
        ):
            self.Term()
            self.Terms()
        else:
            self.exception("ESPERADO IDENTIFICADOR, NUMERO OU '('")
            while(
                not 'REL <=' in self.identifiers_file[self.line_index] or
                not 'REL >=' in self.identifiers_file[self.line_index] or
                not 'REL >' in self.identifiers_file[self.line_index] or
                not 'REL <' in self.identifiers_file[self.line_index] or
                not 'REL ==' in self.identifiers_file[self.line_index] or
                not 'REL !=' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
    
    def AddExp(self): # exp_simples
        self.hasException()
        
        if('ART +' in self.identifiers_file[self.line_index] or 'ART -' in self.identifiers_file[self.line_index]):
            self.Plus()
            self.Term()
            self.Terms()
        elif(
            'IDE' in self.identifiers_file[self.line_index] or
            'NRO' in self.identifiers_file[self.line_index] or
            'DEL (' in self.identifiers_file[self.line_index]
        ):
            self.Term()
            self.Terms()
        else:
            self.exception("ESPERADO IDENTIFICADOR, NUMERO, '(', '+' ou '-'")
            while(
                not 'REL <=' in self.identifiers_file[self.line_index] or
                not 'REL >=' in self.identifiers_file[self.line_index] or
                not 'REL >' in self.identifiers_file[self.line_index] or
                not 'REL <' in self.identifiers_file[self.line_index] or
                not 'REL ==' in self.identifiers_file[self.line_index] or
                not 'REL !=' in self.identifiers_file[self.line_index] or
                not 'LOG &&' in self.identifiers_file[self.line_index] or
                not 'LOG ||' in self.identifiers_file[self.line_index] or
                not 'DEL ;' in self.identifiers_file[self.line_index] or
                not 'DEL )' in self.identifiers_file[self.line_index] 
            ):
                self.nextIdentifier()
    
    def Relational(self): # op_relacional
        self.hasException()
        if(
            'REL <=' in self.identifiers_file[self.line_index] or
            'REL >=' in self.identifiers_file[self.line_index] or
            'REL >' in self.identifiers_file[self.line_index] or
            'REL <' in self.identifiers_file[self.line_index] or
            'REL ==' in self.identifiers_file[self.line_index] or
            'REL !=' in self.identifiers_file[self.line_index]
        ):
            self.nextIdentifier()
        else:
            self.exception("ESPERADO OPERADOR RELACIONAL ('<=', '>=', '<', '>', '==' ou '!=')")
            while(
                not 'IDE' in self.identifiers_file[self.line_index] or
                not 'NRO' in self.identifiers_file[self.line_index] or
                not 'ART +' in self.identifiers_file[self.line_index] or
                not 'ART -' in self.identifiers_file[self.line_index] or
                not 'DEL (' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
       
    def RelationalExpression(self): # exp_rel_deriva
        self.hasException()
        
        if('DEL )' in self.identifiers_file[self.line_index]):
            return
        elif('LOG &&' in self.identifiers_file[self.line_index] or 'LOG ||' in self.identifiers_file[self.line_index]):
            self.Logical()
            self.AddExp()
            self.Relational()
            self.AddExp()
            self.RelationalExpression()
        else:
            self.exception("ESPERADO '&&' ou '||'")
            while(not 'DEL ' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
    
    def Plus(self): # op_ss
        self.hasException()
        
        if(
            'ART +' in self.identifiers_file[self.line_index] or
            'ART -' in self.identifiers_file[self.line_index]
        ):
            self.nextIdentifier()
        else:
            self.exception("ESPERADO '+' ou '-'")
            while(
                not 'IDE' in self.identifiers_file[self.line_index] or
                not 'NRO' in self.identifiers_file[self.line_index] or
                not 'DEL (' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
    
    def Term(self): # termo
        self.hasException()
        
        if(
            'IDE' in self.identifiers_file[self.line_index] or
            'CAD' in self.identifiers_file[self.line_index] or
            'SIM' in self.identifiers_file[self.line_index] or
            'NRO' in self.identifiers_file[self.line_index] or
            'DEL (' in self.identifiers_file[self.line_index]
        ):
            self.Factor()
            self.FactorAux()
        else:
            
            self.exception("ESPERADO IDENTIFICADOR, NUMERO OU '('")
            while(not 'ART +' in self.identifiers_file[self.line_index] or not 'ART -' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
    
    def Terms(self): # termo_deriva
        self.hasException()
        
        if(
            'REL <=' in self.identifiers_file[self.line_index] or
            'REL >=' in self.identifiers_file[self.line_index] or
            'REL >' in self.identifiers_file[self.line_index] or
            'REL <' in self.identifiers_file[self.line_index] or
            'REL ==' in self.identifiers_file[self.line_index] or
            'REL !=' in self.identifiers_file[self.line_index] or
            'DEL )' in self.identifiers_file[self.line_index] or
            'DEL ;' in self.identifiers_file[self.line_index] or
            'LOG &&' in self.identifiers_file[self.line_index] or
            'LOG ||' in self.identifiers_file[self.line_index]
        ):
            return
        elif('ART +' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            self.Sum()
        elif('ART -' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            self.Subtraction()
        else:
            self.exception("ESPERADO '+' ou '-'")
            while(
                not 'REL <=' in self.identifiers_file[self.line_index] or
                not 'REL >=' in self.identifiers_file[self.line_index] or
                not 'REL >' in self.identifiers_file[self.line_index] or
                not 'REL <' in self.identifiers_file[self.line_index] or
                not 'REL ==' in self.identifiers_file[self.line_index] or
                not 'REL !=' in self.identifiers_file[self.line_index] or
                not 'DEL )' in self.identifiers_file[self.line_index] or
                not 'DEL ;' in self.identifiers_file[self.line_index] or
                not 'LOG &&' in self.identifiers_file[self.line_index] or
                not 'LOG ||' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
    
    def Logical(self): # op_bolleano
        self.hasException()
        
        if('LOG &&' in self.identifiers_file[self.line_index] or 'LOG ||' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
        else:
            self.exception("ESPERADO '&&' ou '||'")
            while(
                not 'ART +' in self.identifiers_file[self.line_index] or
                not 'ART -' in self.identifiers_file[self.line_index] or
                not 'IDE' in self.identifiers_file[self.line_index] or
                not 'NRO' in self.identifiers_file[self.line_index] or
                not 'DEL (' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
    
    def Factor(self): # fator
        self.hasException()
        
        if('IDE' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            self.Reserved()
        elif(
            'SIM' in self.identifiers_file[self.line_index] or
            'CAD' in self.identifiers_file[self.line_index] or
            'NRO' in self.identifiers_file[self.line_index]
            ):
            self.nextIdentifier()
        elif('DEL (' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            self.AddExp()
            if('DEL )' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
            else:
                self.exception("ESPERADO ')'")
        else:
            self.exception("ESPERADO IDENTIFICADOR OU NUMERO")
            while(
                not 'REL <=' in self.identifiers_file[self.line_index] or
                not 'REL >=' in self.identifiers_file[self.line_index] or
                not 'REL <' in self.identifiers_file[self.line_index] or
                not 'REL >' in self.identifiers_file[self.line_index] or
                not 'REL ==' in self.identifiers_file[self.line_index] or
                not 'REL !=' in self.identifiers_file[self.line_index] or
                not 'REL =' in self.identifiers_file[self.line_index] or
                not 'ART +' in self.identifiers_file[self.line_index] or
                not 'ART -' in self.identifiers_file[self.line_index] or
                not 'ART *' in self.identifiers_file[self.line_index] or
                not 'ART /' in self.identifiers_file[self.line_index] or
                not 'ART ++' in self.identifiers_file[self.line_index] or
                not 'ART --' in self.identifiers_file[self.line_index] or
                not 'LOG &&' in self.identifiers_file[self.line_index] or
                not 'LOG ||' in self.identifiers_file[self.line_index] or
                not 'DEL )' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
                
    def FactorAux(self): # fator_deriva
        self.hasException()
        
        if(
            not 'REL <=' in self.identifiers_file[self.line_index] or
            not 'REL >=' in self.identifiers_file[self.line_index] or
            not 'REL <' in self.identifiers_file[self.line_index] or
            not 'REL >' in self.identifiers_file[self.line_index] or
            not 'REL ==' in self.identifiers_file[self.line_index] or
            not 'REL !=' in self.identifiers_file[self.line_index] or
            not 'REL =' in self.identifiers_file[self.line_index] or
            not 'ART +' in self.identifiers_file[self.line_index] or
            not 'ART -' in self.identifiers_file[self.line_index] or
            not 'ART ++' in self.identifiers_file[self.line_index] or
            not 'ART --' in self.identifiers_file[self.line_index] or
            not 'LOG &&' in self.identifiers_file[self.line_index] or
            not 'LOG ||' in self.identifiers_file[self.line_index] or
            not 'DEL ;' in self.identifiers_file[self.line_index] or
            not 'DEL )' in self.identifiers_file[self.line_index]
        ):
            return
        elif('ART *' in self.identifiers_file[self.line_index] or 'ART /' in self.identifiers_file[self.line_index]):
            self.DivisorMultiplier()
            self.Term()
        else:
            self.exception("ESPERADO '*' ou '/'")
            while(
                not 'REL <=' in self.identifiers_file[self.line_index] or
                not 'REL >=' in self.identifiers_file[self.line_index] or
                not 'REL <' in self.identifiers_file[self.line_index] or
                not 'REL >' in self.identifiers_file[self.line_index] or
                not 'REL ==' in self.identifiers_file[self.line_index] or
                not 'REL !=' in self.identifiers_file[self.line_index] or
                not 'REL =' in self.identifiers_file[self.line_index] or
                not 'ART +' in self.identifiers_file[self.line_index] or
                not 'ART -' in self.identifiers_file[self.line_index] or
                not 'ART ++' in self.identifiers_file[self.line_index] or
                not 'ART --' in self.identifiers_file[self.line_index] or
                not 'LOG &&' in self.identifiers_file[self.line_index] or
                not 'LOG ||' in self.identifiers_file[self.line_index] or
                not 'DEL )' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
    
    def Sum(self): # op_soma_deriva
        self.hasException()
        
        if('ART +' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
        elif(
            'IDE' in self.identifiers_file[self.line_index] or
            'NRO' in self.identifiers_file[self.line_index] or
            'DEL (' in self.identifiers_file[self.line_index]
        ):
            self.Term()
            self.Terms()
        else:
            self.exception("ESPERADO '+'")
            while(
                not 'REL <=' in self.identifiers_file[self.line_index] or
                not 'REL <=' in self.identifiers_file[self.line_index] or
                not 'REL <' in self.identifiers_file[self.line_index] or
                not 'REL >' in self.identifiers_file[self.line_index] or
                not 'REL ==' in self.identifiers_file[self.line_index] or
                not 'REL !=' in self.identifiers_file[self.line_index] or
                not 'DEL )' in self.identifiers_file[self.line_index] or
                not 'DEL ;' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
    
    def Subtraction(self): # op_sub_deriva
        self.hasException()
        
        if('ART -' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
        elif(
            'IDE' in self.identifiers_file[self.line_index] or
            'NRO' in self.identifiers_file[self.line_index] or
            'DEL (' in self.identifiers_file[self.line_index]
        ):
            self.Term()
            self.Terms()
        else:
            self.exception("ESPERADO '-'")
            while(
                not 'REL <=' in self.identifiers_file[self.line_index] or
                not 'REL <=' in self.identifiers_file[self.line_index] or
                not 'REL <' in self.identifiers_file[self.line_index] or
                not 'REL >' in self.identifiers_file[self.line_index] or
                not 'REL ==' in self.identifiers_file[self.line_index] or
                not 'REL !=' in self.identifiers_file[self.line_index] or
                not 'DEL )' in self.identifiers_file[self.line_index] or
                not 'DEL ;' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
    
    def DivisorMultiplier(self):
        self.hasException()
        
        if('ART *' in self.identifiers_file[self.line_index] or 'ART /' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
        else:
            self.exception("ESPERADO '*' ou '/'")
            while(
                not 'IDE' in self.identifiers_file[self.line_index] or
                not 'NRO' in self.identifiers_file[self.line_index] or
                not 'DEL (' in self.identifiers_file[self.line_index]
            ):
                self.nextIdentifier()
    
    def PpMm(self): # op_cont
        self.hasException()
        
        if('ART ++' in self.identifiers_file[self.line_index] or 'ART --' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
        else:
            self.exception("ESPERADO '++' ou '--'")
            while(not 'DEL )' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
    
    def Start(self): # algoritmo_declaracao
        self.hasException()
        
        if('PRE start' in self.identifiers_file[self.line_index]):
            self.nextIdentifier()
            if('DEL (' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                if('DEL )' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
                    if('DEL {' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
                        self.StartAux()
                        if('DEL ;' in self.identifiers_file[self.line_index]):
                            self.nextIdentifier()
                        if('DEL }' in self.identifiers_file[self.line_index]):
                            self.nextIdentifier()
                        else:
                            self.exception("ESPERADO '}'")
                            while(not '$' in self.identifiers_file[self.line_index]):
                                self.nextIdentifier()  
                    else:
                        self.exception("ESPERADO '{'")
                        while(not '$' in self.identifiers_file[self.line_index]):
                            self.nextIdentifier()
                else:
                    self.exception("ESPERADO ')'")
                    while(not '$' in self.identifiers_file[self.line_index]):
                        self.nextIdentifier()
            else:  
                self.exception("ESPERADO '('")
                while(not '$' in self.identifiers_file[self.line_index]):
                    self.nextIdentifier()
        else:
            # self.previousIdentifier()
            print("TESTE AQUI__________________________________________", self.contentIdentifier())
            self.exception("ESPERADO 'start'")
            while(not '$' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
    
    def StartAux(self): # deriva_cont_principal
        self.hasException()
        
        if('DEL }' in self.identifiers_file[self.line_index]):
            return
        elif('PRE var' in self.identifiers_file[self.line_index]):
            self.VarDecl()
            
            self.PreDecls()
            self.nextIdentifier()
            
            if(
                'PRE if' in self.identifiers_file[self.line_index] or
                'PRE print' in self.identifiers_file[self.line_index] or
                'PRE read' in self.identifiers_file[self.line_index] or
                'PRE while' in self.identifiers_file[self.line_index] or
                'PRE for' in self.identifiers_file[self.line_index] or
                'PRE return' in self.identifiers_file[self.line_index] or
                'IDE' in self.identifiers_file[self.line_index]
            ):
                self.PreDecls()
                self.StartAux()
        elif(
            'PRE if' in self.identifiers_file[self.line_index] or
            'PRE print' in self.identifiers_file[self.line_index] or
            'PRE read' in self.identifiers_file[self.line_index] or
            'PRE while' in self.identifiers_file[self.line_index] or
            'PRE for' in self.identifiers_file[self.line_index] or
            'PRE return' in self.identifiers_file[self.line_index] or
            'IDE' in self.identifiers_file[self.line_index]
        ):
            self.PreDecls()
        else:
            # self.exception("ESPERADO")
            while('}' in self.identifiers_file[self.line_index]):
                self.nextIdentifier()
                
# Função main, cria um objeto e inicia o Analisador Sintatico
if __name__ == '__main__':
    analyzer = SyntacticAnalyzer()
    sys.exit()
