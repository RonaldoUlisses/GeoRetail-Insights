# ESTE CÓDIGO É UM SCRIPT DE INVESTIGAÇÃO PARA EXPLORAR OS DADOS DE SEGURANÇA REGIONAL DA SEJUSP.
# LÊ OS ARQUIVOS CSV DE SEGURANÇA, EXIBE AS COLUNAS DISPONÍVEIS E MOSTRA UMA AMOSTRA DE DADOS PARA IDENTIFICAR CAMPOS ÚTEIS COMO BAIRRO, LOGRADOURO, NATUREZA DO CRIME, ETC.
# ESSA ANÁLISE É IMPORTANTE PARA ENTENDER SE É POSSÍVEL CRUZAR OS DADOS DE CRIMES COM OS DADOS DE ESTABELECIMENTOS PARA CALCULAR RISCOS POR BAIRRO/SETOR.


import pandas as pd
import os
import glob

def investigar_colunas_detalhadas():
    # Caminho onde estão os seus CSVs de segurança
    path = os.path.join("data", "raw", "security")
    arquivos = glob.glob(os.path.join(path, "*.csv"))
    
    if not arquivos:
        print("❌ Nenhum arquivo CSV encontrado em data/raw/security!")
        print("Verifique se os arquivos da SEJUSP estão na pasta correta.")
        return

    # Vamos analisar o primeiro arquivo da lista
    arquivo_teste = arquivos[0]
    print(f"🧐 Analisando a estrutura de: {os.path.basename(arquivo_teste)}")
    
    try:
        # Lendo apenas as 5 primeiras linhas para ser rápido
        df = pd.read_csv(arquivo_teste, sep=';', encoding='latin-1', nrows=5)
        
        print("\n--- COLUNAS ENCONTRADAS ---")
        for i, col in enumerate(df.columns):
            print(f"{i+1}. {col}")
            
        print("\n--- AMOSTRA DE DADOS (Primeira Linha) ---")
        print(df.iloc[0].to_dict())
        
        # Busca específica por termos de interesse
        termos_busca = ['BAIRRO', 'LOGRADOURO', 'ENDERECO', 'LOCAL', 'NATUREZA', 'LATITUDE']
        print("\n--- BUSCA POR CAMPOS CHAVE ---")
        encontrados = [c for c in df.columns if any(termo in c.upper() for termo in termos_busca)]
        
        if encontrados:
            print(f"✅ Colunas promissoras encontradas: {encontrados}")
        else:
            print("⚠️ Nenhuma coluna óbvia de Bairro ou Logradouro detectada.")

    except Exception as e:
        print(f"❌ Erro ao ler o arquivo: {e}")

if __name__ == "__main__":
    investigar_colunas_detalhadas()