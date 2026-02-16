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
        
        # Tenta primeiro o nome padrão 'final_master'
        path_master = os.path.join(self.processed_dir, f"base_{slug_cidade}_final_master.csv")
        
        # Se não encontrar, tenta o nome 'completa' (que é o caso de Congonhas agora)
        if not os.path.exists(path_master):
            path_master = os.path.join(self.processed_dir, f"base_{slug_cidade}_completa.csv")
        
        if not os.path.exists(path_master):
            print(f"❌ Arquivo não encontrado em: {self.processed_dir}")
            print(f"Procurei por: base_{slug_cidade}_final_master.csv OU base_{slug_cidade}_completa.csv")
            return

        print(f"📂 Arquivo encontrado: {os.path.basename(path_master)}")
        df = pd.read_csv(path_master, low_memory=False, dtype=str)

        mapeamento = {
            '0': 'cnpj_basico',
            'cnae_descricao': 'ramo_atividade',
            'bairro': 'bairro',
            'latitude': 'latitude',
            'longitude': 'longitude',
            'V06003': 'renda_media_sm',
            'V06004': 'renda_mediana_nominal',
            'V06005': 'massa_renda_total'
        }
        df.rename(columns=mapeamento, inplace=True)

        # Tratamento numérico
        cols_numericas = ['renda_media_sm', 'renda_mediana_nominal', 'massa_renda_total', 'latitude', 'longitude']
        for col in cols_numericas:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(',', '.')
                df[col] = pd.to_numeric(df[col], errors='coerce')

        salario_base = 1509.00
        if 'renda_media_sm' in df.columns:
            df['renda_estimada_reais'] = df['renda_media_sm'] * salario_base
        
        df['MUNICIPIO_REF'] = cidade_input

        # --- LÓGICA DE ACÚMULO (MULTI-CIDADE) ---
        conn = sqlite3.connect(self.db_path)
        
        # Remove dados antigos APENAS da cidade atual antes de inserir (evita duplicados)
        conn.execute("DELETE FROM tb_georetail_master WHERE MUNICIPIO_REF = ?", (cidade_input,))
        
        # Agora usamos if_exists='append' para manter as outras cidades no banco
        df.to_sql('tb_georetail_master', conn, if_exists='append', index=False)
        
        conn.commit()
        conn.close()
        
        print(f"\n✅ SUCESSO! Dados de {cidade_input} adicionados ao Banco Master.")

if __name__ == "__main__":
    GeoRetailSQL().importar_cidade()
