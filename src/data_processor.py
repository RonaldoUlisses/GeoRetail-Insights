# CRIANDO UM RASTREADOR SIMPLES PARA ENCONTRAR O CÓDIGO DA CIDADE
# Este script é para varrer o arquivo de municípios da Receita Federal e encontrar o código RFB correspondente à cidade será obejto de  analise.

import pandas as pd
import os

class DataProcessor:
    def __init__(self):
        self.raw_path = "data/raw"
        
    def buscar_codigo_municipio(self, nome_cidade):
        """Varre o arquivo de municípios para achar o código RFB"""
        # O arquivo de municípios costuma ter o nome começado com 'K330.K1400.MUNICIPI'
        arquivos = [f for f in os.listdir(self.raw_path) if 'Municipios' in f.upper()]
        
        if not arquivos:
            return "❌ Arquivo de municípios não encontrado em data/raw."
        
        caminho = os.path.join(self.raw_path, arquivos[0])
        
        # Definindo as colunas conforme o layout da Receita
        # Coluna 0: Código | Coluna 1: Nome do Município
        print(f"🔍 Vasculhando {arquivos[0]} por '{nome_cidade.upper()}'...")
        
        try:
            # Lendo com separador ';' e codificação Latin-1 (padrão do governo)
            df = pd.read_csv(caminho, sep=';', encoding='latin-1', header=None, names=['codigo', 'nome'])
            
            # Filtra pela cidade (removendo espaços extras)
            resultado = df[df['nome'].str.strip() == nome_cidade.upper()]
            
            if not resultado.empty:
                return resultado.iloc[0]['codigo']
            return "❌ Município não encontrado no arquivo."
            
        except Exception as e:
            return f"❌ Erro ao ler arquivo: {e}"

if __name__ == "__main__":
    processor = DataProcessor()
    cidade = "CONSELHEIRO LAFAIETE"
    codigo = processor.buscar_codigo_municipio(cidade)
    
    print(f"\n✅ RESULTADO:")
    print(f"O código da Receita Federal para {cidade} é: {codigo}")