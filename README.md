# Authors: 
# Esdras Abreu (@EsdrasAbreu)
# Kevin Cerqueira (@KevinCerqueira)
# EXA 869 - MI - Processadores de Linguagem de Programacao
# ==============================================================================
# Setup:
	- Python 3.9.2
	- Bibliotecas utilizadas:
		- sys
		- string
		- os 	
# Instruções:
	- Para rodar todo o sistema basta inicializar o arquivo 'run.py', que o mesmo irá começar inicializando o arquivo 'lexical_analyzer.py' que este por sua vez pegará os arquivos de entrada contidos na pasta 'input_lexical' com os pré-fixos 'entrada_lexica', e armazenará a(s) sua(s) saida(s) na pasta 'output_lexica' com os pré-fixos 'saida_lexical'. Após isso, o arquivo run.py irá iniciar o analisador sintático, que por sua vez pegará as saidas do analisador lexico contidos na pasta 'output_lexical' com os pré-fixos 'saida_lexica' e armazenará sua saida na pasta 'output_syntactic' com os pré-fixos 'saida_sintatica'. 
	
	Após isso, o arquivo run.py irá finalizar seu funcionamento, e será necessário executar o arquivo 'run_semantic.py' para iniciar o analisador semântico, que o mesmo irá ler a saída do analisador sintático que se encontra na pasta 'output_syntactic', e após seu processamento irá colocar a sua saída na pasta 'output_semantic'.

# OBS
	- O arquivo de saída do análisador semântico está estruturado igual ao do arquivo de saída do análisador sintático, ou seja, imprime identificador por identificador, e quando encontra um erro semântico ele imprime o erro e segue imprimindo o restante dos identificadores, caso encontre um erro sintático irá imprimi-lo e continuará seu funcionamento.

# Ordem de execução:
1 -- run.py
2 -- run_semantic.py  
