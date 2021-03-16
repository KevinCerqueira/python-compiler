# Authors: 
# Esdras Abreu (@EsdrasAbreu)
# Kevin Cerqueira (@KevinCerqueira)
# EXA 869 - MI - Processadores de Linguagem de Programacao
# ==============================================================================
# Implementacao do analisador lexico de um compilador

# Bibliotecas para entrada e saida de arquivos
import sys
import string
import os

'''
    string.punctuation
    00 ! 
    01 "
    02 #
    03 $
    04 %
    05 [
    06 '
    07 &
    08 (
    09 )
    10 *
    11 +
    12 ,
    13  
    14 -
    15 .
    16 /
    17 :
    18 ;
    19 <
    20 =
    21 >
    22 ?
    23 @
    24 [
    25 \
    26 ]
    27 ^
    28 _
    29 `
    30 {
    31 |
    32 }
    33 ~
'''

class LexicalAnalyzer():
#Conjunto de tokens do analisador lexico
    reservedWords = ['var', 'const', 'typedef', 'struct', 'extends', 'procedure', 'function', 'start', 'return', 'if', 'else', 'then', 'while', 'read', 'print', 'int', 'real', 'boolean', 'string', 'true', 'false', 'global', 'local']
    symbols = ''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHJKLMNOPQRSTUVXWYZ[\]^_`abcdefghijklmnopqrstuvxwyz{|}~'''
    letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","X","W","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","x","w","y","z"]
    operatorsArithmetic = ['+', '-', '*', '/', '++', '--']
    operatorsRelational = ['==', '!=', '>', '>=', '<', '<=', '=']
    operatorsLogical = ['&&', '||', '!']
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    delimiters = [';', ',', '(',')', '{', '}', '[', ']']

    # Diretório de entrada
    dir_input = '\\input\\'
    # Diretório de saida
    dir_output = '\\output\\'

# Método que Verifica se é uma palavra reservada
    def isReserved(self, index):
        if index in self.reservedWords:
            return True
        return False

# Método que Verifica se é um símbolo
    def isSymbol(self, index):
        if index in self.symbols:
            return True
        return False

# Método que Verifica se é uma letra
    def isLetter(self, index):
        if index in self.letters:
            return True
        return False

# Método que Verifica se é um operador aritmetico
    def isOperatorArithmetic(self, index):
        if index in self.operatorsArithmetic:
            return True
        return False
    
# Método que Verifica se é um operador relacional
    def isOperatorRelational(self, index):
        if index in self.operatorsRelational:
            return True
        return False

# Método queVerifica se é um operador logico
    def isOperatorLogical(self, index):
        if index in self.operatorsLogical:
            return True
        return False

# Método que Verifica se é um operador 
    def isOperator(self, index):
        if (index in self.operatorsArithmetic) or (index in self.operatorsRelational) or (index in self.operatorsLogical):
            return True
        return False

#Método que Verifica se é um digito
    def isDigit(self, index):
        if index in self.digits:
            return True
        return False

#Método que Verifica se é um delimitador
    def isDelimiter(self, index):
        if index in self.delimiters:
            return True
        return False

#Leitura e escrita do arquivo
    def openFiles(self, file_input):
        try:
            read_file = open(os.getcwd() + self.dir_input + file_input, 'r')
            write_file = open(os.getcwd() + self.dir_output + str(file_input).replace('entrada', 'saida'), 'w')
            return [read_file, write_file]
        except:
            write_file = open(os.getcwd() + self.dir_input + str(file_input).replace('entrada', 'saida'), 'w')
            write_file.write('[ERRO] Não foi possível ler o arquivo de entrada!')
            sys.exit()

# Metodo que encontra os arquivos no diretorio raiz
    def openPrograms(self):
        if(not (os.path.isdir(os.getcwd() + self.dir_input))):
            print('[ERRO] Não foi possível encontrar o diretório de entrada!')
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

 # Metodo que executa o analisador léxico
    def start(self):
        files_programs = self.openPrograms()
        
        for file_program in files_programs:
            read_file = self.openFiles(file_program)[0]
            write_file = self.openFiles(file_program)[1]

            errors = "\n"

            line_file = read_file.readline()
            line_index = 1

            # while que lê o arquivo inteiro
            while(line_file):
                index = 0
                length_line = len(line_file)
                
                # while que lê linha por linha
                while(index < length_line):
                    current_index = line_file[index]
                    next_index = None

                    if((index + 1) < length_line):
                        next_index = line_file[index+1]

                    # Verifica se o caracter é um delimitador
                    if(self.isDelimiter(current_index)):
                        write_file.write('{} DEL {} \n'.format(str(line_index).zfill(2), current_index))

                    # Verifica se é um comentário simples
                    elif(current_index == '/' and next_index == '/'):
                        index = length_line

                    # Verifica se é um comentário em bloco
                    elif(current_index == '/' and next_index == '*'):
                        check = True # Variavel que impedirá o loop a seguir de continuar caso
                                     # seja falsa, isso acontece com erro fim inesperado de arquivo

                        first_line = line_index

                        # Verifica se é o comentário em bloco é fechado corretamente
                        while(check and not(current_index == '*' and next_index == '/')):
                            if((index +2 ) < length_line):
                                index += 1
                                current_index = line_file[index] 
                                next_index = line_file[index+1]
                            else:
                                line_file = read_file.readline()
                                length_line = len(line_file)
                                line_index += 1
                                index = - 1
                                if(not line_file):
                                    errors += ('[ERRO] Linha {} | Coluna {} | CoMF - Comentario mal formado\n'.format(first_line, str(index + 1).zfill(2)))
                                    check = False

                    # Verifica se o caracter é uma aspa dupla
                    elif(current_index == string.punctuation[1]):
                        index += 1
                        check = False  # Variavel de controle
                        index_last_quotes = 0
                        navigator = index
                        
                        while(navigator < length_line):
                            index_last_quotes += 1
                            if(line_file[navigator] == string.punctuation[1]):
                                check = True
                                break
                            navigator += 1

                        # Verifica se é a cadeia de caractere é fechado corretamente com aspa dupla        
                        if(not check):
                            errors += '[ERRO] Linha {} | Coluna {} | CMF - Cadeia de caracteres mal formada\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                            index -= 1
                        else:
                            index_last_quotes += index
                            inside_quotes = ''''''
                            navigator = index
                            index = index_last_quotes
                            while(navigator < index_last_quotes - 1):
                                inside_quotes += (line_file[navigator])
                                navigator += 1
                            for iterator in inside_quotes:
                                if(not self.isSymbol(iterator)):
                                    errors += '[ERRO] Linha {} | Coluna {} | CTI - Caractere invalido\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                                    check = False
                                    break
                            if(check):
                                write_file.write('{} CAD {} \n'.format(str(line_index).zfill(2), inside_quotes))

                    #Verifica se o caractere é uma aspa simples
                    elif(current_index == string.punctuation[6]):
                        navigator = index + 1
                        check = False

                        while(navigator < length_line):
                            if(line_file[navigator] == string.punctuation[6]):
                                check = True
                                break
                            navigator += 1

                        # Verificando Erros Lexicos - Caracter mal formado
                        if((not check) or line_file[index + 1] == '\n'):
                            errors += '[ERRO] Linha {} | Coluna {} | CrMF - Caractere mal formado\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                            index = length_line
                        # Escrevendo Caracter Reservado valido no arquivo
                        elif(line_file[index + 1] == string.punctuation[6]):
                            write_file.write('{} CRV {} \n'.format(str(line_index).zfill(2), "''"))
                            index += 1
                        # Verificando Erros Lexicos - Simbolo Invalido
                        elif((line_file[index + 1] == string.punctuation[6]) and (line_file[index + 2] == string.punctuation[6])):
                            errors += '[ERRO] Linha {} | Coluna {} | SIB - Simbolo invalido\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                            index += 2
                        # Escrevendo símbolo no arquivo
                        elif(self.isSymbol(line_file[index + 1]) and line_file[index + 2] == string.punctuation[6]):
                            write_file.write('{} SIM {} \n'.format(str(line_index).zfill(2), next_index))
                            index += 2
                        # Verificando Erros Lexicos - Tamanho do caractere invalido
                        else:
                            errors += '[ERRO] Linha {} | Coluna {} | TCI - Tamanho do caractere invalido\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                            navigator = index + 1
                            while(navigator < length_line):
                                if(string.punctuation[6] == line_file[navigator]):
                                    index = navigator + 1
                                    break
                                navigator += 1
                    
                    #Verifica se o caracter é uma letra
                    elif(self.isLetter(current_index)):
                        check = False
                        current_character = current_index
                        index += 1

                        while(index < length_line):
                            next_index = None
                            current_index = line_file[index]
                            
                            if(index + 1 < length_line):
                                next_index = line_file[index]

                            # Verifica Se o caracter seguinte é um digito                             
                            if(self.isLetter(current_index) or self.isDigit(current_index) or current_index == "_"):
                                current_character += current_index
                            # Verifica Se o caracter seguinte é um delimitador    
                            elif(self.isDelimiter(current_index) or current_index == ' ' or current_index == '\t' or current_index == '\r'):
                                index -= 1
                                break
                            # Verifica Se o caracter seguinte é um operador
                            elif(next_index != None and self.isOperator(current_index + next_index)) or self.isOperator(current_index):
                                index -=1
                                break
                              # Verificando Erros Lexicos - Identificador Invalido
                            elif current_index != '\n':
                                errors += '[ERRO] Linha {} | Coluna {} | IDI - Identificador invalido\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))
                                check = True
                                break

                            index += 1
                        
                        if(check):
                            while((index + 1) < length_line):
                                index += 1
                                current_index = line_file[index]
                                # Verifica se é um delimitador espaço, \t, \r ou uma /
                                if(self.isDelimiter(current_index) or current_index == ' ' or current_index == '\t' or current_index == '\r' or current_index == '/'):
                                    index -= 1
                                    break
                        else:
                            # escreve no arquivo se é palavra reservada
                            if(self.isReserved(current_character)):
                                write_file.write('{} PRE {} \n'.format(str(line_index).zfill(2), current_character))
                            # escreve no arquivo se é identificador
                            else:
                                write_file.write('{} IDE {} \n'.format(str(line_index).zfill(2), current_character))

                    # Verifica se é um digito        
                    elif(self.isDigit(current_index)):
                        current_character = current_index
                        maybe_signal = ''

                        # Verifica se o dígito é precedido de sinal negativo ou positivo
                        if(line_file[index - 1] in ['-', '+']):
                            maybe_signal = line_file[index - 1]

                        index += 1
                        check_index = 0
                        current_index = next_index
                        valid = False

                        
                        while (self.isDigit(current_index) and (index + 1 < length_line)):
                            current_character += current_index
                            index += 1
                            current_index = line_file[index]

                        # Verifica se após o digito tem ponto decimal
                        if(current_index == '.'):
                            if((index + 1) < length_line):
                                current_character += current_index
                                index += 1
                                current_index = line_file[index]
                                while(self.isDigit(current_index) and index < length_line - 1):
                                    check_index += 1
                                    current_character += current_index
                                    index += 1
                                    current_index = line_file[index]
                                
                                # Verifica se o ponto é um delimitador
                                if(current_index == '.'):
                                    check_index = 0
                                    while(index < length_line - 1):
                                        index += 1
                                        current_index = line_file[index]
                                        if(self.isDelimiter(current_index) or current_index == string.punctuation[13]):
                                            index -= 1
                                            break
                            else:
                                valid = False

                            if(check_index > 0):
                                valid = True
                            else:
                                valid = False
                            index -= 1
                        # Validação do dígito       
                        else:
                            valid = True
                            if(not self.isDigit(current_index)):
                                index -= 1

                          # Verificando Erros Lexicos - numero mal formado        
                        if(valid):
                            write_file.write('{} NRO {} \n'.format(str(line_index).zfill(2), maybe_signal + current_character))
                        else:
                            errors += '[ERRO] Linha {} | Coluna {} | NMF - Numero mal formado\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))   

                    # Verificando a categoria do operador
                    elif(next_index != None and self.isOperatorArithmetic(current_index + next_index)):
                        write_file.write('{} ART {} \n'.format(str(line_index).zfill(2), current_index + next_index))
                        index += 1
                    # Aritmetico
                    elif(self.isOperatorArithmetic(current_index)):
                        if((not self.isDigit(next_index)) and current_index in ['-', '+']):
                            write_file.write('{} ART {} \n'.format(str(line_index).zfill(2), current_index))
                    # Relacional
                    elif(next_index != None and self.isOperatorRelational(current_index + next_index)):
                        write_file.write('{} REL {} \n'.format(str(line_index).zfill(2), current_index + next_index))
                        index += 1
                    elif(self.isOperatorRelational(current_index)):
                        write_file.write('{} REL {} \n'.format(str(line_index).zfill(2), current_index))
                    # Lógico
                    elif(next_index != None and self.isOperatorLogical(current_index + next_index)):
                        write_file.write('{} LOG {} \n'.format(str(line_index).zfill(2), current_index + next_index))
                        index += 1
                    elif(self.isOperatorLogical(current_index)):
                        write_file.write('{} LOG {} \n'.format(str(line_index).zfill(2), current_index))
                    # Verificando Erros Lexicos -Simbolo invalido        
                    elif current_index != '\n' and current_index != ' ' and current_index != '\t' and current_index != '\r':
                        errors += '[ERRO] Linha {} | Coluna {} | SIB - Simbolo invalido\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2))

                    index += 1
                
                #Ler a proxima linha
                line_file = read_file.readline()
                line_index += 1

            #Fechando o arquivo
            read_file.close()
            write_file.write(errors)
            write_file.close()
        return

if __name__ == '__main__':
    analyzer = LexicalAnalyzer()
    analyzer.start()
    sys.exit()