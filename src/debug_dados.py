# ANALISANDO A ESTRUTURA DOS DADOS BRUTOS
# Este script é para verificar a estrutura dos arquivos brutos extraídos,
# especialmente para entender como a coluna de município está formatada,
# issoé crucial para o processo de geolocalização e análise posterior. 
# Ele lê as primeiras linhas do arquivo bruto e mostra os valores únicos da coluna de município
# para garantir que esta sendo identificado corretamente o código da cidade.


import pandas as pd
import os

# Caminho para o arquivo extraído
arquivo = r"g:/Meu Drive/GeoRetail-Insights/data/raw/K3241.K03200Y8.D60110.ESTABELE"

print("🔬 Analisando as primeiras 5 linhas do arquivo bruto...")
# Lendo sem filtro para ver como os dados aparecem
df = pd.read_csv(arquivo, sep=';', encoding='latin-1', header=None, nrows=5, dtype=str)

# A coluna de município é a 20 (índice 20 no layout da RFB)
print("\n📋 Amostra da coluna de Município (Coluna 20):")
print(df.iloc[:, 20].unique())

print("\n💡 Verifique se os números acima se parecem com '4365'.")