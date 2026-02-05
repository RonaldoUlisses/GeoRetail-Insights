# CRIANDDO CÓDIGO PARA DEBUGAR O ARQUIVO DE LOTE 0 EXTRAÍDO

import pandas as pd
import os

# Caminho para o seu Lote 0 extraído
arquivo = r"G:\Meu Drive\GeoRetail-Insights\data\raw\K3241.K03200Y0.D60110.ESTABELE"

print(f"🔬 Analisando o DNA do arquivo: {os.path.basename(arquivo)}")

try:
    # Lendo apenas as colunas de Município (20) e Bairro (17) para ser rápido
    # Usamos header=None pois o arquivo não tem cabeçalho
    df = pd.read_csv(arquivo, sep=';', encoding='latin-1', header=None, 
                     nrows=500000, dtype=str, usecols=[17, 20])
    
    print("\n✅ Primeiras linhas encontradas (Bruto):")
    print(df.head(10))
    
    print("\n🔍 Códigos de Município que MAIS aparecem neste lote:")
    print(df[20].value_counts().head(20))
    
    print("\n🏙️ Amostra de nomes de Bairros neste lote:")
    print(df[17].dropna().unique()[:10])

except Exception as e:
    print(f"❌ Erro ao ler: {e}")