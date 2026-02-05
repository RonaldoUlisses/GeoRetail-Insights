# Aqui vamos Enriquecer os dados dos estabelecimentos com informações adicionais

import pandas as pd
import os

class GeoRetailEnricher:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
        self.processed_dir = os.path.join(self.base_dir, "data", "processed")

    def enriquecer_dados(self):
        print("\n--- 💎 GeoRetail: Enriquecimento de Dados ---")
        cidade_input = input("Para qual cidade deseja cruzar os dados? (ex: CONSELHEIRO LAFAIETE): ").strip()
        cidade_slug = cidade_input.lower().replace(' ', '_')
        
        path_empresas = os.path.join(self.processed_dir, f"cnpjs_{cidade_slug}.csv")
        path_cnae = os.path.join(self.processed_dir, "dicionario_cnae.csv")
        output_path = os.path.join(self.processed_dir, f"base_{cidade_slug}_completa.csv")

        if not os.path.exists(path_empresas):
            print(f"❌ Erro: Arquivo {path_empresas} não encontrado.")
            return
        
        print(f"🔄 Carregando dados de {cidade_input.upper()} ({path_empresas})...")
        
        # Carregamos o CSV sem nomes de colunas
        df_empresas = pd.read_csv(path_empresas, dtype=str, header=None)
        
        # Verificamos em qual coluna está o CNAE e o Bairro baseado no deslocamento (índice)
        #Se houver 30 colunas, a ordem correta para Bairro e CEP costuma ser:
        if len(df_empresas.columns) >= 30:
            col_cnae = 11      # CNAE Fiscal
            col_bairro = 17    # Bairro (Antes estava 18, que é o CEP)
            col_fantasia = 4   # Nome Fantasia
            col_municipio = 20 # Município
        else:
            # Layout padrão de 21 colunas
            col_cnae = 11
            col_bairro = 17
            col_fantasia = 4

        # Renomeamos apenas o necessário para o merge
        df_empresas = df_empresas.rename(columns={col_cnae: 'cnae_principal', col_bairro: 'bairro', col_fantasia: 'nome_fantasia'})
        
        df_cnae = pd.read_csv(path_cnae, dtype=str)

        print("🔗 Padronizando códigos e cruzando dados...")
        
        # Limpeza e padronização para 7 dígitos
        df_empresas['cnae_principal'] = df_empresas['cnae_principal'].str.replace('"', '').str.replace(r'\D', '', regex=True).str.strip().str.zfill(7)
        df_cnae['cnae_codigo'] = df_cnae['cnae_codigo'].str.replace('"', '').str.replace(r'\D', '', regex=True).str.strip().str.zfill(7)

        # DEBUG: Agora deve mostrar um CNAE (ex: 4711302)
        print(f"DEBUG Empresa (CNAE): {df_empresas['cnae_principal'].iloc[0]}")
        print(f"DEBUG Dicionário (CNAE): {df_cnae['cnae_codigo'].iloc[0]}")

        # Merge
        df_final = pd.merge(df_empresas, df_cnae, left_on='cnae_principal', right_on='cnae_codigo', how='left')

        df_final.to_csv(output_path, index=False)
        
        print(f"✨ SUCESSO! Base enriquecida gerada.")
        
        if 'cnae_descricao' in df_final.columns:
            print(f"\n📊 TOP 10 ATIVIDADES EM {cidade_input.upper()}:")
            print(df_final['cnae_descricao'].value_counts().head(10))
        else:
            print("⚠️ Erro ao mapear descrições. Verifique o dicionário.")

if __name__ == "__main__":
    GeoRetailEnricher().enriquecer_dados()