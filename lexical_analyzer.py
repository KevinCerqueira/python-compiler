# Authors: 
# Esdras Abreu (@EsdrasAbreu)
# Kevin Cerqueira (@KevinCerqueira)

import sys
import string
'''
    string.punctuation
    00 ! 
    01 "
    02 #
    03 $
    04 %
    05 [
    06 &
    07 '
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

    reservedWords = ['var', 'const', 'typedef', 'struct', 'extends', 'procedure', 'function', 'start', 'return', 'if', 'else', 'then', 'while', 'read', 'print', 'int', 'real', 'boolean', 'string', 'true', 'false', 'global', 'local']
    symbols = ''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHJKLMNOPQRSTUVXWYZ[\]^_`abcdefghijklmnopqrstuvxwyz{|}~'''
    letters = ["A","B","C","D","E","F","G","H","J","K","L","M","N","O","P","Q","R","S","T","U","V","X","W","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","x","w","y","z"]
    operatorsArithmetic = ['+', '-', '*', '/', '++', '--']
    operatorsRelational = ['==', '!=', '>', '>=', '<', '<=', '=']
    operatorsLogical = ['&&', '||', '!']
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    delimiters = [';', ',', '(',')', '{', '}', '[', ']']

    file_input = 'input.txt'
    file_output = 'output.txt'

    def isReserved(self, index):
        if index in self.reservedWords:
            return True
        return False

    def isSymbol(self, index):
        if index in self.symbols:
            return True
        return False

    def isLetter(self, index):
        if index in self.letters:
            return True
        return False

    def isOperatorArithmetic(self, index):
        if index in self.operatorsArithmetic:
            return True
        return False
    
    def isOperatorRelational(self, index):
        if index in self.operatorsRelational:
            return True
        return False
    
    def isOperatorLogical(self, index):
        if index in self.operatorsLogical:
            return True
        return False

    def isDigit(self, index):
        if index in self.digits:
            return True
        return False

    def isDelimiter(self, index):
        if index in self.delimiters:
            return True
        return False

    def openFiles(self):
        try:
            read_file = open(self.file_input, 'r')
            write_file = open(self.file_output, 'w')
            return [read_file, write_file]
        except:
            write_file = open(self.file_output, 'w')
            write_file.write('[ERRO] Linha {}:{} | Não foi possível ler o arquivo de entrada!')
            sys.exit()

    def start(self):
        read_file = self.openFiles()[0]
        write_file = self.openFiles()[1]

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
                
                if(self.isDelimiter(current_index)):
                    write_file.write('{} DEL {} \n'.format(str(line_index).zfill(2), current_index))

                elif(current_index == '/' and next_index == '/'):
                    index = length_line
                
                elif(current_index == '/' and next_index == '*'):
                    check = True
                    first_line = line_index
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
                                write_file.write ('[ERRO] Linha {}:{} | CML - Comentario de bloco não fechado adequadamente\n'.format(first_line, str(index + 1).zfill(2)))
                                check = False

                elif(current_index == string.punctuation[1]):
                    index += 1
                    check = False
                    index_last_quotes = 0
                    navigator = index
                    
                    while(navigator < length_line):
                        index_last_quotes += 1
                        if(line_file[navigator] == string.punctuation[1]):
                            check = True
                            break
                        navigator += 1
                            
                    if(not check):
                        write_file.write('[ERRO] Linha {}:{} | CMF - Cadeia de caracteres mal formada\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2)))
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
                                write_file.write('[ERRO] Linha {}:{} | CTI - Caractere invalido\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2)))
                                check = False
                                break
                        if(check):
                            write_file.write('{} CAD {} \n'.format(str(line_index).zfill(2), inside_quotes))

                elif(current_index == string.punctuation[6]):
                    navigator = index + 1
                    check = False

                    while(navigator < length_line):
                        if(line_file[navigator] == string.punctuation[6]):
                            check = True
                            break
                        navigator += 1

                    if((not check) or line_file[index + 1] == '\n'):
                        write_file.write('[ERRO] Linha {}:{} | CMF - Caractere mal formado\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2)))
                        index = length_line
                    elif(line_file[index + 1] == string.punctuation[6]):
                        write_file.write('{} CRV {} \n'.format(str(line_index).zfill(2), "''"))
                        index += 1
                    elif((line_file[index + 1] == string.punctuation[6]) and (line_file[index + 2] == string.punctuation[6])):
                        write_file.write('[ERRO] Linha {}:{} | SIB - Simbolo invalido\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2)))
                        index += 2
                    elif(self.isSymbol(line_file[index + 1]) and line_file[index + 2] == string.punctuation[6]):
                        write_file.write('{} SIM {} \n'.format(str(line_index).zfill(2), next_index))
                        index += 2
                    else:
                        write_file.write('[ERRO] Linha {}:{} | TCI - Tamanho do caractere invalido\n'.format(str(line_index).zfill(2), str(index + 1).zfill(2)))
                        navigator = index + 1
                        while(navigator < length_line):
                            if(string.punctuation[6] == line_file[navigator]):
                                index = navigator + 1
                                break
                            navigator += 1
                    
                elif(self.isDigit(current_index)):
                    current_character = current_index
                    maybe_signal = ''

                    if(line_file[index - 1] in ['-', '+']):
                        maybe_signal = line_file[index - 1]
                    elif((line_file[index - 2] in ['-', '+'] and line_file[index - 1] == ' ')):
                        maybe_signal = line_file[index - 2]

                    index += 1
                    check_index = 0
                    current_index = next_index
                    valid = False

                    while (self.isDigit(current_index) and (index + 1 < length_line)):
                        current_character += current_index
                        index += 1
                        current_index = line_file[index]

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
                            
                    else:
                        valid = True
                        if(not self.isDigit(current_index)):
                            index -= 1
                            
                    if(valid):
                        write_file.write('{} NMR {} \n'.format(str(line_index).zfill(2), maybe_signal + current_character))
                    else:
                        write_file.write('[ERRO] Linha {}:{} | NMF - Numero mal formado'.format(str(line_index).zfill(2), str(index + 1).zfill(2)))        

                elif(next_index != None and self.isOperatorArithmetic(current_index + next_index)):
                    write_file.write('{} ART {} \n'.format(str(line_index).zfill(2), current_index + next_index))
                    index += 1
                elif(self.isOperatorArithmetic(current_index)):
                    write_file.write('{} ART {} \n'.format(str(line_index).zfill(2), current_index))

                elif(next_index != None and self.isOperatorRelational(current_index + next_index)):
                    write_file.write('{} REL {} \n'.format(str(line_index).zfill(2), current_index + next_index))
                    index += 1
                elif(self.isOperatorRelational(current_index)):
                    write_file.write('{} REL {} \n'.format(str(line_index).zfill(2), current_index))

                elif(next_index != None and self.isOperatorLogical(current_index + next_index)):
                    write_file.write('{} LOG {} \n'.format(str(line_index).zfill(2), current_index + next_index))
                    index += 1
                elif(self.isOperatorLogical(current_index)):
                    write_file.write('{} LOG {} \n'.format(str(line_index).zfill(2), current_index))
                            

                index += 1
            
            line_file = read_file.readline()
            line_index += 1

        
        read_file.close()
        write_file.close()
        return

if __name__ == '__main__':
    analyzer = LexicalAnalyzer()
    analyzer.start()
    sys.exit()