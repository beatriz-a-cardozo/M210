# =========================================================== IMPORTAÇÃO DE BIBLIOTECAS
import numpy as np  # biblioteca numpy para armazenar os dados em matrizes
from tkinter import messagebox

np.set_printoptions(suppress=True)  # desativa a notação científica

class Symplex:
    def __init__(self, obj, var, res):
        # =========================================== VARIÁVEIS PARA ARMAZENAR OS DADOS
        self.obj = obj  # armazena o objetivo da função
        self.var = var  # lista de variáveis no problema
        self.res = res  # lista de restrições

    def montarTableau(self):  # ======================================= MONTAR O TABLEAU
        c = np.array([var['coef'] for var in self.var], dtype=float)  # armazena os coeficientes

        if self.obj == 'min':
            c = -c  # caso seja uma minimização, os dados são invertidos

        num_vars = len(self.var)
        num_res = len(self.res)

        num_cols = num_vars + num_res + 1  
        tableau = np.zeros((num_res + 1, num_cols))  # inicializa o tableau com zeros
        tableau[0, :num_vars] = -c  # inverte os valores da primeira linha
        tableau[0, -1] = 0  

        for i, res in enumerate(self.res):
            tableau[i + 1, :num_vars] = res['coefs']  
            
            if res['sinal'] == '<=': # caso seja menor menor que
                tableau[i + 1, num_vars + i] = 1  
            elif res['sinal'] == '>=': # caso seja maior que
                tableau[i + 1, num_vars + i] = -1  
            
            tableau[i + 1, -1] = res['dir']  

        return tableau

    def symplexSolver(self):
        try:
            if len(self.var) == 0:
                messagebox.showerror('Erro', 'Adicione pelo menos uma variável de decisão!')
                return

            tableau = self.montarTableau()

            while True:
                # ----------------------------------------- procurando pela coluna pivô
                l_obj = tableau[0, 1:-1]

                if np.min(l_obj) >= 0:
                    return tableau

                coluna_pivo = np.argmin(l_obj) + 1  

                # ----------------------------- procurando pelo elemento pivô na coluna
                coluna_dir = tableau[:, -1]
                coluna_pivo_vals = tableau[:, coluna_pivo]

                with np.errstate(divide='ignore'):
                    razoes = np.where(
                        coluna_pivo_vals > 0,
                        coluna_dir / coluna_pivo_vals,
                        np.inf
                    )

                linha_pivo = np.argmin(razoes[1:]) + 1  
                # -------------------------------------------------------- PIVOTEAMENTO
                pivo = tableau[linha_pivo, coluna_pivo]
                tableau[linha_pivo] /= pivo

                for i in range(tableau.shape[0]):
                    if i != linha_pivo:
                        fator = tableau[i, coluna_pivo]
                        tableau[i] -= fator * tableau[linha_pivo]

        except Exception as e:
            messagebox.showerror('Erro', f'Ocorreu um erro ao resolver o problema: \n{str(e)}')

