# GEORETAIL - INTEGRAÇÃO DE DADOS DO IBGE
# Este script é para integrar os dados de renda por distrito do IBGE com a base georreferenciada dos estabelecimentos, 
# criando uma base mestra que inclui informações de renda estimada para cada estabelecimento, com base no distrito em que está localizado.
# Ele realiza um merge entre a base georreferenciada e o arquivo de renda por distrito, utilizando as chaves de distrito para combinar as informações,
# e salva o resultado em um arquivo CSV que pode ser usado para análises avançadas e exportação para o banco de dados.

import pandas as pd
import os

class IBGEIntelligence:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.abspath(os.path.join(self.current_dir, ".."))
        self.processed_dir = os.path.join(self.base_dir, "data", "processed")
        self.external_dir = os.path.join(self.base_dir, "data", "external")

    def injetar_renda(self, cidade="CONSELHEIRO LAFAIETE"):
        slug_cidade = cidade.lower().replace(' ', '_')
        path_geo = os.path.join(self.processed_dir, f"base_{slug_cidade}_final_geo.csv")
        
        # 1. Carregar sua base georreferenciada
        if not os.path.exists(path_geo):
            print(f"❌ Base georreferenciada não encontrada.")
            return
        
        df_geo = pd.read_csv(path_geo, low_memory=False)

        # 2. Carregar o arquivo de Rendimento por Distrito
        path_renda = os.path.join(self.external_dir, "Agregados_por_distritos_renda_responsavel_BR.csv")
        
        if not os.path.exists(path_renda):
            print(f"❌ Arquivo de Rendimento não encontrado: {path_renda}")
            return
        
        print(f"💰 Carregando dados de renda...")
        # Adicionando o encoding='latin1'
        df_renda = pd.read_csv(path_renda, sep=';', low_memory=False, encoding='latin1')

        # 3. Realizar o Casamento (Merge)
        # O arquivo de distritos costuma usar 'Cod_distrito' ou 'CD_DIST'
        # identificando a coluna de ligação
        col_ligacao_ibge = 'Cod_distrito' if 'Cod_distrito' in df_renda.columns else df_renda.columns[0]
        col_ligacao_geo = 'CD_DIST' if 'CD_DIST' in df_geo.columns else 'index_right'

        print(f"🔗 Unindo dados via chaves: {col_ligacao_geo} <-> {col_ligacao_ibge}")
        
        df_final = pd.merge(
            df_geo, 
            df_renda, 
            left_on=col_ligacao_geo, 
            right_on=col_ligacao_ibge, 
            how='left'
        )

        # 4. Salvar a Base Mestra
        output_path = os.path.join(self.processed_dir, f"base_{slug_cidade}_final_master.csv")
        df_final.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        print(f"\n🏆 SUCESSO! Base Mestra gerada com {len(df_final)} registros.")

if __name__ == "__main__":
    IBGEIntelligence().injetar_renda()
