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
        print("📊 GeoRetail: Exportação para Power BI")
        print("="*45)

        cidade = input("Qual cidade deseja preparar para o Dashboard? ").strip().upper()
        cidade_slug = cidade.lower().replace(' ', '_')
        
        # Busca o arquivo que já passou pelo enriquecimento e geomarketing
        
        path_input = os.path.join(self.processed_dir, f"base_{cidade_slug}_completa.csv")

        if not os.path.exists(path_input):
            print(f"❌ Erro: Base enriquecida não encontrada em: {path_input}")
            return

        print(f"⏳ Padronizando dados de {cidade}...")
        df = pd.read_csv(path_input, low_memory=False, dtype=str)

        # 1. Dicionário de Padronização (Garante que o Power BI sempre veja os mesmos nomes)
        colunas_map = {
            'nome_fantasia': 'NOME_NEGOCIO',
            'cnae_descricao': 'SETOR_ATIVIDADE',
            'bairro': 'BAIRRO',
            'cnae_principal': 'CODIGO_CNAE'
        }

        # Renomeia e filtra apenas o necessário
        df_dash = df.rename(columns=colunas_map)
        
        # Mantém apenas colunas úteis para o BI (ajuste conforme seu CSV)
        colunas_finais = ['NOME_NEGOCIO', 'SETOR_ATIVIDADE', 'BAIRRO', 'CODIGO_CNAE']
        
        # Verifica se latitude/longitude existem (caso já tenha rodado o geomarket_service)
        if 'latitude' in df.columns:
            df_dash['LATITUDE'] = df['latitude']
            df_dash['LONGITUDE'] = df['longitude']
            colunas_finais.extend(['LATITUDE', 'LONGITUDE'])

        df_dash = df_dash[colunas_finais].copy()

        # 2. Limpezas Finais
        df_dash['CIDADE'] = cidade
        df_dash['BAIRRO'] = df_dash['BAIRRO'].str.upper().str.strip()
        df_dash['NOME_NEGOCIO'] = df_dash['NOME_NEGOCIO'].fillna("NOME NÃO INFORMADO")

        # 3. Exportação
        output_path = os.path.join(self.export_dir, "base_dashboard.csv")
        
        # 'utf-8-sig' é o segredo para o Power BI e Excel não darem erro de acentuação
        df_dash.to_csv(output_path, index=False, encoding='utf-8-sig')

        print(f"✅ SUCESSO! Dados prontos para o Power BI.")
        print(f"📂 Arquivo gerado: {output_path}")
        print(f"💡 Dica: No Power BI, aponte a fonte de dados para este arquivo fixo.")

def main():
    GeoRetailExporter().preparar_dashboard()

if __name__ == "__main__":
    main()
