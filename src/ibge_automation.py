# AQUI O OBJETIVO É USAR AS APIs DO IBGE PARA BAIXAR DADOS DE RENDA E MAPAS GEOGRÁFICOS
# API USADA: SIDRA (Sistema IBGE de Recuperação Automática)
# Documentação: https://apisidra.ibge.gov.br/#

import pandas as pd
import geopandas as gpd
import os
import requests

class IBGEAutomation:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.abspath(os.path.join(self.current_dir, ".."))
        self.processed_dir = os.path.join(self.base_dir, "data", "processed")
        self.external_dir = os.path.join(self.base_dir, "data", "external")
        
        # Código IBGE de Conselheiro Lafaiete
        self.codigo_municipio = "3118304" 
        
        # Garante que a pasta external exista
        os.makedirs(self.external_dir, exist_ok=True)

    def carregar_malha(self):
        """
        Tenta carregar a malha localmente. 
        Mantém a lógica de API comentada para uso futuro.
        """
        # --- OPÇÃO 1: CARGA LOCAL (RECOMENDADA) ---
        arquivos_locais = [f for f in os.listdir(self.external_dir) if f.endswith(('.shp', '.json', '.geojson'))]
        
        if arquivos_locais:
            caminho = os.path.join(self.external_dir, arquivos_locais[0])
            print(f"🌍 Carregando malha local: {caminho}...")
            malha = gpd.read_file(caminho)
            
            # Filtro por município (caso o arquivo seja do estado todo)
            colunas_mun = ['CD_MUN', 'cd_mun', 'GEOCODIGO', 'codigo_municipio']
            for col in colunas_mun:
                if col in malha.columns:
                    malha = malha[malha[col].astype(str).str.contains(self.codigo_municipio)]
                    break
            return malha

        # --- OPÇÃO 2: API DO IBGE (COMENTADA PARA FUTURO) ---
        """
        print(f"📡 Tentando baixar malha via API para {self.codigo_municipio}...")
        url_api = f"https://servicodados.ibge.gov.br/api/v3/malhas/municipios/{self.codigo_municipio}?formato=application/vnd.geo+json&qualidade=maxima&intrarregiao=setor-censitario"
        try:
            malha_api = gpd.read_file(url_api)
            return malha_api
        except Exception as e:
            print(f"❌ Falha na API: {e}")
        """
        
        print(f"⚠️ Nenhum arquivo encontrado em {self.external_dir}. Baixe o Shapefile de MG no portal do IBGE.")
        return None

    def realizar_cruzamento(self, cidade="CONSELHEIRO LAFAIETE"):
        slug_cidade = cidade.lower().replace(' ', '_')
        path_base = os.path.join(self.processed_dir, f"base_{slug_cidade}_completa.csv")

        if not os.path.exists(path_base):
            print(f"❌ Arquivo base não encontrado: {path_base}")
            return

        # 1. Carregar registros com coordenadas (2.722 pontos)
        df = pd.read_csv(path_base, low_memory=False)
        df_geo = df.dropna(subset=['latitude', 'longitude']).copy()
        df_geo = df_geo[df_geo['latitude'] != 'N/A']

        # 2. Criar GeoDataFrame
        gdf_cnpjs = gpd.GeoDataFrame(
            df_geo, 
            geometry=gpd.points_from_xy(df_geo.longitude.astype(float), df_geo.latitude.astype(float)),
            crs="EPSG:4326"
        )

        # 3. Carregar Malha e Cruzar
        gdf_setores = self.carregar_malha()

        if gdf_setores is not None:
            # Sincroniza sistemas de coordenadas
            if gdf_setores.crs != gdf_cnpjs.crs:
                gdf_setores = gdf_setores.to_crs(gdf_cnpjs.crs)
            
            print(f"🔗 Cruzando {len(gdf_cnpjs)} pontos com a malha do IBGE...")
            resultado = gpd.sjoin(gdf_cnpjs, gdf_setores, how="left", predicate="within")

            # 4. Salvar Resultado
            output_path = os.path.join(self.processed_dir, f"base_{slug_cidade}_final_geo.csv")
            resultado.drop(columns='geometry').to_csv(output_path, index=False, encoding='utf-8-sig')
            
            print(f"✨ SUCESSO! Base georreferenciada salva em: {output_path}")

if __name__ == "__main__":
    IBGEAutomation().realizar_cruzamento()