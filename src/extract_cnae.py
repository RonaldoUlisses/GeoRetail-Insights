# GEORETAIL - EXTRAÇÃO E CLASSIFICAÇÃO DE CNAEs
# Este script é para extrair e classificar os CNAEs a partir do arquivo bruto de CNAEs extraído da Receita Federal.
# Ele limpa os dados, padroniza os códigos e descrições, e salva um dicionário de CNAEs que pode ser usado para enriquecer a base de estabelecimentos posteriormente.


import pandas as pd
import os

class CnaeExtractor:
    def __init__(self):
        # Pega a pasta onde o script está (src) e sobe um nível para a raiz (GeoRetail-Insights)
        # Se o script estiver em src/src, precisa subir dois níveis
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Se está rodando de dentro de g:/Meu Drive/GeoRetail-Insights/src/
        # precisa garantir que ele ache a pasta 'data' na raiz
        self.base_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
        
        self.raw_path = os.path.join(self.base_dir, "data", "raw")
        self.processed_dir = os.path.join(self.base_dir, "data", "processed")
        
        print(f"📂 Verificando pasta de dados em: {self.raw_path}")
        os.makedirs(self.processed_dir, exist_ok=True)
    def processar(self):
        print("\n--- 📝 GeoRetail: Processador de Dicionário CNAE ---")
        
        # Localiza o arquivo de CNAEs extraído
        arq_cnae = next((os.path.join(self.raw_path, f) for f in os.listdir(self.raw_path) 
                         if "CNAE" in f.upper() and not f.endswith(".zip")), None)
        
        if not arq_cnae:
            print("❌ Erro: Arquivo CNAE extraído não encontrado em data/raw.")
            return

        print(f"📖 Lendo arquivo: {os.path.basename(arq_cnae)}")
        
        # O arquivo de CNAE tem apenas 2 colunas: Código e Descrição
        df = pd.read_csv(arq_cnae, sep=';', encoding='latin-1', header=None, dtype=str)
        
        # Limpeza
        df[0] = df[0].str.replace(r'\D', '', regex=True) # Código
        df[1] = df[1].str.replace('"', '').str.strip().str.upper() # Descrição
        
        df.columns = ['cnae_codigo', 'cnae_descricao']
        
        output_path = os.path.join(self.processed_dir, "dicionario_cnae.csv")
        df.to_csv(output_path, index=False)
        
        print(f"✅ Dicionário com {len(df)} atividades criado em: {output_path}")

if __name__ == "__main__":
    CnaeExtractor().processar()