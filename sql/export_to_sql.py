# TRABALHANDO COM SQLITE PARA EXPORTAR DADOS DO CSV PARA O BANCO DE DADOS
# O script lê o CSV processado, faz um mapeamento otimizado das colunas


import pandas as pd
import sqlite3
import os

class GeoRetailSQL:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.abspath(os.path.join(self.current_dir, ".."))
        self.processed_dir = os.path.join(self.base_dir, "data", "processed")
        self.db_path = os.path.join(self.base_dir, "georetail_database.db")

    def importar_cidade(self):
        cidade_input = input("Cidade para exportação (Ex: CONSELHEIRO LAFAIETE): ").strip().upper()
        slug_cidade = cidade_input.lower().replace(' ', '_')
        path_master = os.path.join(self.processed_dir, f"base_{slug_cidade}_final_master.csv")
        
        if not os.path.exists(path_master):
            print(f"❌ Arquivo não encontrado: {path_master}")
            return

        # Lendo o CSV
        df = pd.read_csv(path_master, low_memory=False, dtype=str)

        # MAPEAMENTO OTIMIZADO
        mapeamento = {
            '0': 'cnpj_basico',
            'cnae_descricao': 'ramo_atividade',
            'bairro': 'bairro',
            'latitude': 'latitude',
            'longitude': 'longitude',
            'V06003': 'renda_media_sm',      # Em Salários Mínimos
            'V06004': 'renda_mediana_nominal',
            'V06005': 'massa_renda_total'    # Potencial total do setor
        }
        
        df.rename(columns=mapeamento, inplace=True)

        # TRATAMENTO NUMÉRICO
        cols_numericas = ['renda_media_sm', 'renda_mediana_nominal', 'massa_renda_total', 'latitude', 'longitude']
        
        for col in cols_numericas:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(',', '.')
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # CÁLCULOS EXTRAS
        salario_base = 1509.00
        if 'renda_media_sm' in df.columns:
            df['renda_estimada_reais'] = df['renda_media_sm'] * salario_base
        
        df['MUNICIPIO_REF'] = cidade_input

        # SALVANDO NO SQLITE
        conn = sqlite3.connect(self.db_path)
        df.to_sql('tb_georetail_master', conn, if_exists='replace', index=False)
        conn.close()
        
        print(f"\n✅ SUCESSO! Banco de dados atualizado para {cidade_input}.")
        print(f"📊 Colunas ricas do IBGE incluídas: Renda Média, Mediana e Massa Total.")

if __name__ == "__main__":
    GeoRetailSQL().importar_cidade()
