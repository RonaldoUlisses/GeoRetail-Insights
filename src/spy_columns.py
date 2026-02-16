# INVESTIGAÇÃO DE COLUNAS DO CSV
# Este script é para verificar o conteúdo das colunas do arquivo master processado, 
# garantindo que os dados estejam corretos antes de avançar para a etapa de exportação para o banco de dados.

import pandas as pd
import os

# Caminho para o arquivo master
path = "data/processed/base_conselheiro_lafaiete_final_master.csv"

# Lê apenas as 2 primeiras linhas para não pesar
df = pd.read_csv(path, nrows=2, low_memory=False)

print("\n🔍 INVESTIGAÇÃO DE COLUNAS:")
print("-" * 50)
for col in df.columns:
    # Mostra o índice da coluna e o que tem dentro dela
    valor = df[col].iloc[0]
    print(f"Coluna [{col}]: {valor}")
print("-" * 50)