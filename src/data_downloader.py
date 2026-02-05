# AQUI ESTAMOS REALIZANDO DOWNLOADS DE ARQUIVOS ZIP DE MICRODADOS

import os
import requests
import zipfile

class DataDownloader:
    def __init__(self):
        # Define os caminhos relativos baseados na sua estrutura de pastas
        self.raw_path = os.path.join("data", "raw")
        self.processed_path = os.path.join("data", "processed")
        self.base_url = "https://dadosabertos.rfb.gov.br/CNPJ/"
        
        # Cria as pastas caso não existam no Explorer
        for path in [self.raw_path, self.processed_path]:
            os.makedirs(path, exist_ok=True)

    def processar_arquivo(self, nome_arquivo):
        """Tenta extrair se existir localmente; caso contrário, tenta o download"""
        destino_zip = os.path.join(self.raw_path, nome_arquivo)
        
        # 1. Verifica se o arquivo já estÃO na pasta (Download Manual)
        if os.path.exists(destino_zip):
            print(f"📦 Arquivo {nome_arquivo} detectado localmente. Iniciando extração...")
            self._extrair_zip(destino_zip)
        else:
            # 2. Se não existir, tenta o download automático
            print(f"🌐 {nome_arquivo} não encontrado. Iniciando tentativa de download...")
            sucesso = self._baixar_via_web(nome_arquivo, destino_zip)
            if sucesso:
                self._extrair_zip(destino_zip)

    def _baixar_via_web(self, nome_arquivo, destino_zip):
        """Lógica de download com Headers para evitar bloqueios do servidor"""
        url = f"{self.base_url}{nome_arquivo}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            # Timeout de 60 segundos para dar tempo ao servidor instável da Receita
            response = requests.get(url, headers=headers, stream=True, timeout=60)
            if response.status_code == 200:
                with open(destino_zip, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024*1024): # 1MB chunks
                        if chunk:
                            f.write(chunk)
                print(f"✅ Download concluído: {nome_arquivo}")
                return True
            else:
                print(f"⚠️ Servidor recusou (Erro {response.status_code}). Baixe manualmente em: {url}")
                return False
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            print(f"👉 Dica: Baixe o arquivo no navegador e coloque em: {self.raw_path}")
            return False

    def _extrair_zip(self, caminho_zip):
        """Extrai o conteúdo"""
        try:
            with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                zip_ref.extractall(self.raw_path)
            print(f"📂 Conteúdo de {os.path.basename(caminho_zip)} extraído para {self.raw_path}")
        except Exception as e:
            print(f"❌ Erro ao extrair: {e}")

if __name__ == "__main__":
    downloader = DataDownloader()
    
    print("--- 🛠️ GeoRetail: Gerenciador de Microdados ---")
    
    # Lista de arquivos fundamentais para começar
    arquivos_alvo = ["Municipios.zip", "Cnaes.zip"]
    
    for arquivo in arquivos_alvo:
        downloader.processar_arquivo(arquivo)
        print("-" * 30)

    print("\n💡 Próxima etapa: Ler os CSVs extraídos para identificar o código de Lafaiete.")