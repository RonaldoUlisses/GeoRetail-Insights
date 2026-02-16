# CRIANDO UM RASTREADOR SIMPLES PARA ENCONTRAR O CÓDIGO DA CIDADE
# Este script é para varrer o arquivo de municípios da Receita Federal e encontrar o código RFB correspondente à cidade será obejto de  analise.

import pandas as pd
import os

class GeoRetailExporter:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.abspath(os.path.join(self.current_dir, ".."))
        self.processed_dir = os.path.join(self.base_dir, "data", "processed")
        self.export_dir = os.path.join(self.base_dir, "data", "dashboard")
        os.makedirs(self.export_dir, exist_ok=True)

    def preparar_dashboard(self):
        print("\n" + "="*45)
        print("📊 GeoRetail: Exportação com Coordenadas")
        print("="*45)

        cidade = input("Qual cidade deseja exportar para o mapa? ").strip().upper()
        cidade_slug = cidade.lower().replace(' ', '_')
        
        # O Power BI vai ler este arquivo fixo
        path_input = os.path.join(self.processed_dir, f"base_{cidade_slug}_completa.csv")

        if not os.path.exists(path_input):
            print(f"❌ Erro: Base de {cidade} não encontrada.")
            return

        df = pd.read_csv(path_input, low_memory=False)

        # 1. Padronização de Colunas incluindo GPS
        colunas_map = {
            'nome_fantasia': 'NOME_NEGOCIO',
            'cnae_descricao': 'SETOR_ATIVIDADE',
            'bairro': 'BAIRRO',
            'latitude': 'LATITUDE',
            'longitude': 'LONGITUDE'
        }

        df_dash = df.rename(columns=colunas_map)
        
        # Filtramos apenas o necessário para o BI
        colunas_finais = ['NOME_NEGOCIO', 'SETOR_ATIVIDADE', 'BAIRRO', 'LATITUDE', 'LONGITUDE']
        
        # Garante que só exporte o que tem localização (evita erros no mapa)
        df_dash = df_dash.dropna(subset=['LATITUDE', 'LONGITUDE'])
        df_dash = df_dash[colunas_finais].copy()

        # 2. Informação da Cidade
        df_dash['CIDADE'] = cidade

        # 3. Exportação com encoding para acentuação (UTF-8 com BOM)
        output_path = os.path.join(self.export_dir, "base_dashboard.csv")
        df_dash.to_csv(output_path, index=False, encoding='utf-8-sig')

        print(f"✅ SUCESSO! {len(df_dash)} pontos mapeados para {cidade}.")
        print(f"📂 Arquivo pronto: {output_path}")

if __name__ == "__main__":
    GeoRetailExporter().preparar_dashboard()