# Authors: 
# Esdras Abreu (@EsdrasAbreu)
# Kevin Cerqueira (@KevinCerqueira)

import sys
import string

class LexicalAnalyzer():

    reservedWords = ['var', 'const', 'typedef', 'struct', 'extends', 'procedure', 'function', 'start', 'return', 'if', 'else', 'then', 'while', 'read', 'print', 'int', 'real', 'boolean', 'string', 'true', 'false', 'global', 'local']
    symbols = [" ","!","#","$","%","&","'","(",")","*","+",",","-",".","/","0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","?","@","A","B","C","D","E","F","G","H","J","K","L","M","N","O","P","Q","R","S","T","U","V","X","W","Y","Z","[","\\","]","^","_","`","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","x","w","y","z","{","|","}","~"]
    operators = ['+', '-', '*', '/', '++', '--', '==', '!=', '>', '>=', '<', '<=', '=', '&&', '||', '!']
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    delimiters = [';', ',', '(',')', '{', '}', '[', ']']

    file_input = 'input.txt'
    file_output = 'output.txt'

    def isReserved(self, word):
        if word in self.reservedWords:
            return True
        return False
        # return self.reservedWords.find(word)

    def isSymbol(self, word):
        if word in self.symbols:
            return True
        return False
        # return self.symbols.find(word)

    def isOperator(self, word):
        if word in self.operators:
            return True
        return False
        # return self.operators.find(word)

    def isDigit(self, word):
        if word in self.digits:
            return True
        return False
        # return self.digits.find(word)

    def isDelimiter(self, word):
        if word in self.delimiters:
            return True
        return False
        # return self.delimiters.find(word)
    def openFiles(self):
        try:
            read_file = open(self.file_input, 'r')
            write_file = open(self.file_output, 'w')
            return [read_file, write_file]
        except:
            write_file = open(self.file_output, 'w')
            write_file.write('ERRO Não foi possível ler o arquivo de entrada!')
            sys.exit()

    def start(self):
        read_file = self.openFiles()[0]
        write_file = self.openFiles()[1]

        line_file = read_file.readline()
        line_index = 1
        line_index_formated = '0'
        # while que lê o arquivo inteiro
        while(line_file):
            index = 0
            length_file = len(line_file)
            
            # while que lê linha por linha
            while(index < length_file):
                current_index = line_file[index]
                next_index = None

                if((index + 1) < length_file):
                    next_index = line_file[index+1]
                
                if(self.isDelimiter(current_index)):
                    write_file.write('{}{} DEL {} \n'.format(line_index_formated, line_index, current_index))
                elif(current_index == '/' and next_index == '/'):
                    index = length_file
                elif(current_index == '*' and next_index == '/'):
                    check = True
                    first_line = line_index
                    while(check and not(current_index == '/' and next_index == '*')):
                        if((index +2 ) < length_file):
                            index += 1
                            current_index = line_file[index] 
                            next_index = line_file[index+1]
                        else:
                            line_file = read_file.readline()
                            length_file = len(line_file)
                            line_index += 1
                            index = - 1
                            if(not line_file):
                                write_file.write ('ERRO Comentário de bloco não fechado adequadamente | | Linha -> {}'.format(first_line))
                                check = False

                index += 1
            
            line_file = read_file.readline()
            line_index += 1
            line_index_formated = ''
            if(line_index < 10):
                line_index_formated = '0'

        
        read_file.close()
        write_file.close()
        return

if __name__ == '__main__':
    analyzer = LexicalAnalyzer()
    analyzer.start()
    sys.exit()