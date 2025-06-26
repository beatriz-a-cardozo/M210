import tkinter as tk
from Symplex import Symplex
from Sensibilidade import AnaliseDeSensibilidade
if __name__ == '__main__': # ============================================== FUNÇÃO MAIN
    
    print('=============== BEM VINDO AO SYMPLEX SOLVER ==============')
    print('-O software de otimizacao para resolver seus problemas-')
    print()
    obj = input('[+] Deseja maximizar[max] ou minimizar[min]: ')
    print()
    num_vars = int(input('[+] Quantas variaveis de decisao teremos: '))
    var = []
    for i in range(num_vars):
        print()

        nome = input(f"[+] Nome da variavel {i+1}: ")
        coef = float(input(f"[+] Lucro de {nome}: "))

        var.append({'nome':nome,'coef':coef})

    print()
    num_res = int(input('[+] Agora, quantas restriçoes temos: '))

    res = []

    for i in range(num_res):
        print()
        nome = input(f"[+] Nome da restriçao(tipo PESO, LIM.,2...): ")
        coefs = []
        for v in var:
            coef = input(f"[+] Insira o coeficiente da variavel {v['nome']}: ")
            coefs.append(coef)

        sinal = input(f"[+] A restriçao e [<=] ou [>=]. Insira a opcao desejada: ")
        dir = int(input(f"[+] Insira o limite da restricao {nome}: "))

        res.append({'nome': nome,'coefs': coefs, 'sinal': sinal, 'dir': dir})

    solver = Symplex(obj,var,res)
    resultado = solver.symplexSolver()

    print('=================== RESULTADO DO SYMPLEX =================')
    print(f"[-] LUCRO OTIMO :: R$ {resultado[0,-1]}")
    print()
    print('[-] PREÇO SOMBRA: ')
    for r in range(num_res):
        print(f"    {res[r]['nome']} :: {resultado[0,num_vars+r]} R$/un.")
    
    print() # --------------------------------------- inicia a Analise de Sensibilidade
    alt = input('[+] Deseja testar alguma alteracao [sim]/[nao]:') 
    print()

    if alt=='sim':
        while True:
            alteracoes = []
            for r in res: # entrada de dados das alterações já nos valores convertidos
                a = int(input(f"[+] Deseja alterar para quanto a restricao {r['nome']}: "))
                # a -= r['dir']
                alteracoes.append(a) 

            sen = AnaliseDeSensibilidade(resultado,num_vars,num_res,alteracoes)
            sen.condicaoDeAlteracao()

            alt = input('[+] Deseja testar alguma outra alteracao [sim]/[nao]:')
            if alt == 'nao':
                break

    # ====================================================================== CASO TESTE
    # obj = 'max'

    # var = [
    #     {'nome': 'e', 'coef': 80},
    #     {'nome': 'm', 'coef': 70},
    #     {'nome': 'a', 'coef': 100},
    #     {'nome': 'p', 'coef': 16}
    # ]

    # res = [
    #     {'coefs': [1, 1, 1, 4], 'sinal': '<=', 'dir': 250},
    #     {'coefs': [0, 1, 1, 2], 'sinal': '<=', 'dir': 600},
    #     {'coefs': [3, 2, 4, 0], 'sinal': '<=', 'dir': 500}
    # ]

    # solver = Symplex(obj, var, res)
    # res = solver.symplexSolver()

    # alteracoes = [-25,-60,-50]
    # sen = AnaliseDeSensibilidade(res,4,3,alteracoes)
    # sen.condicaoDeAlteracao()
