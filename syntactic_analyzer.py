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
    table_register = {}
    table_const = {}
    table_global = {}
    table_function = {}
    table_algorithm = {}
    
    def __init__(self):
        # Arquivos do programa
        files_programs = self.openPrograms()

        # Laço de repetição que percorre todos os arquivos encontrados na 
        # pasta de saida do analisador lexico (output_lexical/saidaX.txt).
        for file_program in files_programs:
            # Verifica se há algum erro sintático
            isError = False

            read_file = self.openFiles(file_program)[0]
            write_file = self.openFiles(file_program)[1]

            self.identifiers_file = read_file.readlines()

            self.line_index = 0
            self.line_current = ""
    
    # Vai para o próximo identificador/token
    def nextIdentifier(self):
        self.line_index += 1
        self.line_current = self.identifiers_file[self.line_index][self.identifiers_file[self.line_index].find(' ') + 1 : -1]
    
    # Pega o conteudo do indentificador/token
    def contentIdentifier(self):
        return self.identifiers_file[self.line_index][ : self.identifiers_file[self.line_index].find(' ')]
    
    # Procura por um erro, caso haja vai para a próxima linha
    def nextIndex(self):
        if("[ERRO]" in self.identifiers_file[self.line_file]):
            self.line_index += 1
            
    # <Program> ::= <Global Decl><Decls><Start>
    def Program(self):
        self.nextIndex()
            
    # <Global Decl> ::= <Const Decl> | <Var Decl> | <Const Decl><Var Decl>  | <Var Decl><Const Decl> |
    def GlobalDecl(self):
        self.nextIndex()
    
    # <Const Decl> ::= 'const' '{' <ConstList> '}' 
    def ConstDecl(self):
        self.nextIndex()
    
    # <ConstList> ::= <Type> <Const> <ConstList> | 
    def ConstList(self):
        self.nextIndex()
    
    # <Type> ::= int | real | boolean | string | struct Identifier | Identifier
    def Type(self):
        self.nextIndex()
    
    # <Const> ::= Identifier '=' <Value> <Delimiter Const> 
    def Const(self):
        self.nextIndex()
    
    # <Value> ::= <Number> | <Boolean Literal> | StringLiteral
    def Value(self):
        self.nextIndex()
    
    # <Number> ::= DecLiteral | OctLiteral | HexLiteral | FloatLiteral
    def Number(self):
        self.nextIndex()
    
    # <Boolean Literal> ::= 'true'| 'false'
    def BooleanLiteral(self):
        self.nextIndex()
    
    # <Delimiter Const> ::= ',' <Const> |';'
    def DelimiterConst(self):
        self.nextIndex()
    
    # <Var Decl> ::= 'var' '{' <VariablesList> '}'  
    def VarDecl(self):
        self.nextIndex()
    
    # <VariablesList> ::= <Type> <Variable> <VariablesList> |  
    def VariablesList(self):
        self.nextIndex()
    
    # <Variable> ::= Identifier<Aux>
    def Variable(self):
        self.nextIndex()
    
    # <Aux> ::= '=' <Value> <Delimiter Var> | <Delimiter Var>|  <Vector><Assignment_vector><Delimiter Var>  | <Matrix><Assignment_matrix><Delimiter Var>    
    def Aux(self):
        self.nextIndex()
    
    # <Delimiter Var> ::= ',' <Variable> |';'
    def DelimiterVar(self):
        self.nextIndex()
    
    # <Vector> ::= '['<Index>']'
    def Vector(self):
        self.nextIndex()
    
    # <Index> ::= DecLiteral | OctLiteral | Identifier
    def Index(self):
        self.nextIndex()
    
    # <Assignment_vector> ::= <Assignment_vector_aux1> | <Assignment_vector_aux2> | 
    def AssignmentVector(self):
        self.nextIndex()
    
    # <Assignment_vector_aux1> ::= '=' <Value>
    def AssignmentVectorAux1(self):
        self.nextIndex()
    
    # <Assignment_vector_aux2> ::= '=' '{'<Value_assigned_vector>'}'
    def AssignmentVectorAux2(self):
        self.nextIndex()
    
    # <Value_assigned_vector> ::= <Value> ',' <Value_assigned_vector> | <Value>
    def ValueAssignedVector(self):
        self.nextIndex()
    
    # <Matrix> ::= '['<Index>']' <Vector>
    def Matrix(self):
        self.nextIndex()
    
    # <Assignment_matrix> ::= <Assignment_matrix_aux1> | <Assignment_matrix_aux2> |
    def AssignmentMatrix(self):
        self.nextIndex()
    
    # <Assignment_matrix_aux1> ::=  <Assignment_vector_aux1>
    def AssignmentMatrixAux1(self):
        self.nextIndex()
    
    # <assignment_matrix_aux2> ::=  '=' '{' '{' <Value_assigned_matrix> '}' <Dimensao_matrix2>
    def AssignmentMatrixAux2(self):
        self.nextIndex()
    
    # <Value_assigned_matrix> ::= <Value> ',' <Value_assigned_matrix> | <Value> 
    def ValueAssignedMatrix(self):
        self.nextIndex()
    
    # <Dimensao_matrix2> ::= ',' '{'<Value_assigned_matrix> '}' '}'
    def DimensaoMatrix2(self):
        self.nextIndex()

    # <Decls> ::= <Decl> <Decls> |
    def Decls(self):
        self.nextIndex()

    #FAZER STRUCT DECL
    # <Decl>  ::= <Function Declaration>| <Proc Decl> | <Struct Decl> | <Typedef Decl>
    def Decl(self):
        self.nextIndex()

    # <Function Declaration> ::= 'function' <Type> Identifier '(' <Params> ')' '{' <Body> '}'
    def FunctionDeclaration(self):
        self.nextIndex()
    
    # <Params>     ::= <Param> ',' <Params>| <Param> | 
    def Params(self):
        self.nextIndex()

    # <Param>      ::= const <Type> Identifier  |  <Type> Identifier
    def Param(self):
        self.nextIndex()
    
    # <Proc Decl> ::= 'procedure' Identifier '(' <Params> ')' '{' <Body Procedure> '}'  | Identifier '(' <Formal Parameter List> ')' '{' <Body Procedure> '}'
     def ProcDecl(self):
        self.nextIndex()

    # <Body Procedure>  ::=  <Body Item Procedure><Body Procedure>   |  
    def BodyProcedure(self):
        self.nextIndex()

    # <Body Item Procedure>  ::=  <Var Decl> | <While Procedure> | <If Procedure> | <Read> | <Print> | <Assign>
    def BodyItemProcedure(self):
        self.nextIndex()

    # <While Procedure> ::= 'while' '(' <Conditional Expression> ')' '{' <Body Procedure> '}'
    def WhileProcedure(self):
        self.nextIndex()
        
    # <Conditional Expression> ::= <Boolean Literal>  | <Relational Expression>  | <Logical Expression>
    def ConditionalExpression(self):
        self.nextIndex()

    # <Boolean Literal> ::= 'true'  | 'false'
    def BooleanLiteral(self):
        self.nextIndex()

    # <Relational Expression>  ::= <Exp> <Relational> 
    def RelationalExpression(self):
        self.nextIndex()

    # <Exp> ::= <PrefixGlobalLocal> <Term> <Add Exp> | <Term> <Add Exp>
    def Exp(self):
        self.nextIndex()

    # <PrefixGlobalLocal> ::= 'global.' | 'local.'
    def PrefixGlobalLocal(self):
        self.nextIndex()

    # <Term> ::= <Expression Value> <Mult Exp>
    def Term(self):
        self.nextIndex()

    # <Expression Value>  ::= '-' <Expression Value>   |  Identifier | '(' <Exp> ')' | <Number>    | <Boolean Literal>  | StringLiteral  | <Function Call>
    def ExpressionValue(self):
        self.nextIndex()
    
    # <Function Call> ::= Identifier '(' <Formal Parameter List> ')'
    def FunctionCall(self):
        self.nextIndex()

    # <Formal Parameter List> ::= <Exp>   | <Exp> ',' <Formal Parameter List>    |
    def FormalParameterList(self):
        self.nextIndex()

    # <Mult Exp>    ::= '*' <Term>   |  '/' <Term>    |
    def MultExp(self):
        self.nextIndex()

    # <Add Exp>     ::=  '+'  <Exp>   |   '-'  <Exp>     | 
    def AddExp(self):
        self.nextIndex()

    # <Relational> ::= '>'  <Exp>    |  '<'  <Exp>   |  '<=' <Exp>   |  '>=' <Exp>  |  '==' <Exp>    !Equal  |  '!=' <Exp>    !Not equal
    def Relational(self):
        self.nextIndex()
         
    # <Logical Expression> ::= <Expression Value Logical> <Logical> | <Logical Denied> 
    def LogicalExpression(self):
        self.nextIndex()

    # <Expression Value Logical>  ::= Identifier    | <Boolean Literal>   | StringLiteral  | <Function Call>  | <Relational Expression>
    def ExpressionValueLogical(self):
        self.nextIndex()

    # <Logical> ::= <Conditional Operator> <Expression Value Logical> | <Conditional Operator> <Logical Denied>
    def Logical(self):
        self.nextIndex()

    # <Conditional Operator>  ::= '&&'  | '||' 
    def ConditionalOperator(self):
        self.nextIndex()

    # <Logical Denied> ::= '!' Identifier   | '!' <Boolean Literal  | '!' <Logical Expression>  | '!' <Relational Expression>
    def LogicalDenied(self):
        self.nextIndex()

    # <If Procedure> ::= 'if' '(' <Conditional Expression><Then Procedure> 
    def IfProcedure(self):
        self.nextIndex()
    
    # <Then Procedure> ::= ')' 'then' '{'<Body Procedure>'}' <Else Procedure>
    def ThenProcedure(self):
        self.nextIndex()

    # <Else Procedure> ::= 'else' '{' <Body Procedure> '}' | 
    def ElseProcedure(self):
        self.nextIndex()

    # <Read>  ::= read'(' <Formal Parameter List Read> ')' ';'
    def Read(self):
        self.nextIndex()

    # <Formal Parameter List> ::= <Exp>  | <Exp> ',' <Formal Parameter List>  |
    def FormalParameterList(self):
        self.nextIndex()

    # <Print> ::= print'(' <Formal Parameter List>  ')' ';'
    def Print(self):
        self.nextIndex()

    # <Assign> ::= <PrefixGlobalLocal> Identifier '=' <Exp> ';'  | Identifier '=' <Exp> ';'  | Identifier <Vector><Assignment_vector> ';' | Identifier <Matrix><Assignment_matrix> ';' | <Exp> ';' 
    def Assign(self):
        self.nextIndex()