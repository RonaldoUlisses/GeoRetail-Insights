# GEORETAIL - EXPORTAÇÃO PARA DASHBOARD
# Este script é para preparar os dados para serem usados no Power BI,
# garantindo que as colunas estejam com nomes amigáveis e que os dados de latitude e longitude estejam presentes para o mapeamento geográfico.
# Também inclui uma etapa de limpeza final para garantir que o arquivo exportado seja leve e fácil de usar no dashboard.

import pandas as pd
import os

class GeoRetailExporter:
    def __init__(self):
        # Localiza as pastas do projeto de forma dinâmica
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.abspath(os.path.join(self.current_dir, ".."))
        self.processed_dir = os.path.join(self.base_dir, "data", "processed")
        self.export_dir = os.path.join(self.base_dir, "data", "dashboard")
        
        # Cria a pasta de exportação se ela não existir
        os.makedirs(self.export_dir, exist_ok=True)

    def preparar_dashboard(self):
        print("\n" + "="*45)
        print("📊 GeoRetail: Exportação para Power BI")
        print("="*45)

        cidade = input("Qual cidade deseja preparar para o Dashboard? ").strip().upper()
        cidade_slug = cidade.lower().replace(' ', '_')
        
        # Define o caminho do arquivo de entrada (base enriquecida)
        path_input = os.path.join(self.processed_dir, f"base_{cidade_slug}_completa.csv")

        if not os.path.exists(path_input):
            print(f"❌ Erro: Base enriquecida não encontrada em: {path_input}")
            print("💡 Dica: Certifique-se de que a Opção [2] foi executada com sucesso.")
            return

        print(f"⏳ Padronizando dados de {cidade}...")
        
        # Leitura do arquivo (Correção de indentação aplicada)
        df = pd.read_csv(path_input, low_memory=False)

        # Padroniza os nomes das colunas para minúsculo para evitar conflitos de busca
        df.columns = df.columns.str.lower()

        # 1. Dicionário de Mapeamento para nomes amigáveis no Power BI
        colunas_map = {
            'nome_fantasia': 'NOME_NEGOCIO',
            'cnae_descricao': 'SETOR_ATIVIDADE',
            'bairro': 'BAIRRO',
            'latitude': 'LATITUDE',
            'longitude': 'LONGITUDE'
        }

        # Verifica a presença de coordenadas para atender requisito de mapeamento geográfico
        if 'latitude' not in df.columns or 'longitude' not in df.columns:
            print("\n⚠️ Aviso: Colunas de coordenadas não encontradas no arquivo.")
            print("💡 Dica: Para ver os pontos no mapa, rode o Motor de Geomarketing (Opção 4) primeiro.")
            return

        # Renomeia as colunas conforme o dicionário
        df_dash = df.rename(columns=colunas_map)
        
        # Remove linhas sem coordenadas (essencial para não quebrar o mapa do Power BI)
        df_dash = df_dash.dropna(subset=['LATITUDE', 'LONGITUDE'])
        
        # Seleciona apenas as colunas necessárias para manter o arquivo leve
        colunas_finais = ['NOME_NEGOCIO', 'SETOR_ATIVIDADE', 'BAIRRO', 'LATITUDE', 'LONGITUDE']
        df_dash = df_dash[colunas_finais].copy()

        # 2. Limpezas e Adições Finais
        df_dash['CIDADE'] = cidade
        df_dash['BAIRRO'] = df_dash['BAIRRO'].str.upper().str.strip()
        df_dash['NOME_NEGOCIO'] = df_dash['NOME_NEGOCIO'].fillna("NOME NÃO INFORMADO")

        # 3. Exportação Final
        output_path = os.path.join(self.export_dir, "base_dashboard.csv")
        
        # utf-8-sig garante que o Windows/Excel/Power BI leiam acentos corretamente
        df_dash.to_csv(output_path, index=False, encoding='utf-8-sig')

        print(f"\n✅ SUCESSO! {len(df_dash)} registros preparados com coordenadas.")
        print(f"📂 Arquivo gerado para o Power BI: {output_path}")

def main():
    GeoRetailExporter().preparar_dashboard()

if __name__ == "__main__":
    main()
