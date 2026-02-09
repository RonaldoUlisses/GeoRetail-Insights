# CRIANDO UM RASTREADOR SIMPLES PARA ENCONTRAR O CÓDIGO DA CIDADE

import pandas as pd
import os

class NeighborhoodTracker:
    def __init__(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        # Testando  Lote 0 para descobrir o código real
        self.raw_file = os.path.join(self.base_dir, "data", "raw", "K3241.K03200Y0.D60110.ESTABELE")

    def rastrear(self):
        if not os.path.exists(self.raw_file):
            print("❌ Arquivo Lote 0 não encontrado.")
            return

        print(f"🔍 Buscando por 'SAO JOAO' em Minas Gerais (MG)...")

        # Lendo apenas as colunas essenciais: 17 (Bairro), 19 (UF) e 20 (Município)
        reader = pd.read_csv(self.raw_file, sep=';', encoding='latin-1', header=None, 
                             chunksize=500000, dtype=str, usecols=[14, 17, 19, 20])

        for i, chunk in enumerate(reader):
            # Limpeza rápida
            chunk[17] = chunk[17].str.replace('"', '').str.strip().str.upper()
            chunk[19] = chunk[19].str.replace('"', '').str.strip().str.upper()
            chunk[20] = chunk[20].str.replace('"', '').str.strip()
            
            # FILTRO DUPLO: Bairro correto E Estado de Minas Gerais
            match = chunk[(chunk[17] == "SAO JOAO") & (chunk[19] == "MG")]
            
            if not match.empty:
                print(f"\n✅ Encontrado no lote!")
                # Mostra: Logradouro, Bairro, UF, Código Município
                print(match.head(10)) 
                print("\n💡 Verifique se o logradouro (rua) pertence a Lafaiete.")
                print(f"O código da cidade usado pela RFB aqui é: {match[20].unique()}")
                return # Para assim que achar a primeira evidência

            if i % 4 == 0:
                print(f"⏳ Analisadas {i * 500000} linhas...")

if __name__ == "__main__":
    tracker = NeighborhoodTracker()
    tracker.rastrear()