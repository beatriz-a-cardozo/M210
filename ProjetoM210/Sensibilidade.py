import numpy as np

class AnaliseDeSensibilidade:
    def __init__(self, tableau_final, num_var, num_res, alteracoes):
        self.tableau_final = tableau_final
        self.num_var = num_var
        self.num_res = num_res
        self.alteracoes = alteracoes

    def calculoNovoLucro(self): # ------------------------------- CALCULO DO NOVO LUCRO

        l_obj = self.tableau_final[0, self.num_var:self.num_var + self.num_res + 1]
        
        antigo_lucro = l_obj[-1]
        novo_lucro = antigo_lucro

        for i in range(self.num_res):
            novo_lucro += l_obj[i] * self.alteracoes[i]

        print()
        print(f"[-]     LUCRO NOVO :: R$ {novo_lucro}")

        return novo_lucro

    def condicaoDeAlteracao(self): # --------------- VERIFICA SE É UMA ALTERAÇÃO VIÁVEL
        flag = 0

        for i in range(self.num_res):
            linha = self.tableau_final[i+1, self.num_var:self.num_var + self.num_res + 1]
            
            coef_original = linha[-1]
            
            novo_valor = coef_original
            for j in range(self.num_res):
                novo_valor += linha[j] * self.alteracoes[j]
            
            print()

            if novo_valor < 0:
                print(f'[-] ALTERAÇÃO INVIAVEL! - Restrição {i+1} violada')
                flag = 1
                break
            else:
                continue

        if flag == 0: # ---- caso seja uma alteração viável, ele calcula o novo lucro e
            print('[-] ALTERAÇÃO VIAVEL!')
            self.calculoNovoLucro()
            self.limites_preco_sombra() # --------- também mostra as alterações limites
            return
        
        else:
            return None
        
    def limites_preco_sombra(self):
    
        limites = []
        
        for i in range(self.num_res):
            
            linha = self.tableau_final[i+1, :]
            
            coefs = linha[self.num_var:self.num_var + self.num_res]
            
            b_i = linha[-1]
            
            delta_mais = np.inf
            delta_menos = np.inf
            
            for j in range(self.num_res):
                if coefs[j] > 0:
                    delta_mais = min(delta_mais, b_i / coefs[j])
                elif coefs[j] < 0:
                    delta_menos = min(delta_menos, -b_i / coefs[j])
            
            limite_inferior = b_i - (delta_menos if delta_menos != np.inf else 0)
            limite_superior = b_i + (delta_mais if delta_mais != np.inf else 0)
            
            limites.append((limite_inferior, limite_superior))

        print()
        print("\n[-] LIMITES DE VALIDADE DO PREÇO SOMBRA:")
        for i, (lim_inf, lim_sup) in enumerate(limites):
            print(f"Restrição {i+1}: {lim_inf} ≤ b_{i+1} ≤ {lim_sup}")
        
        return limites