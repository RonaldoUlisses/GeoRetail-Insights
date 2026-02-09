# GEORETAIL EXPLORER – ANÁLISE ESPACIAL DE ATIVIDADES ECONÔMICAS

# Aqui é o cerebro dinâmico para buscar oportunidades de negócios em bairros específicos;
# Utiliza geocodificação para mapear locais e gerar arquivos prontos para visualização;

import pandas as pd
import os
import time
import unicodedata
from geopy.geocoders import Nominatim

# ---------------------------------------------------------
# Geocoding API utilizada:
# Nominatim (OpenStreetMap)
# Documentação oficial:
# https://nominatim.org/release-docs/latest/api/Overview/
# ---------------------------------------------------------


class GeoRetailExplorer:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.abspath(os.path.join(current_dir, ".."))
        self.processed_dir = os.path.join(self.base_dir, "data", "processed")
        self.geolocator = Nominatim(user_agent="georetail_final_v3")

    def remover_acentos(self, texto):
        if not isinstance(texto, str): return ""
        return "".join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn').upper()

    def buscar_oportunidades(self):
        print("\n--- 📍 GeoRetail: Busca Inteligente (Auto-Scan) ---")
        cidade = input("Cidade: ").strip().upper()
        bairro = input("Bairro: ").strip().upper()
        
        slug_cidade = cidade.lower().replace(' ', '_')
        path_base = os.path.join(self.processed_dir, f"base_{slug_cidade}_completa.csv")

        if not os.path.exists(path_base):
            print(f"❌ Arquivo não encontrado: {path_base}")
            return

        # Carrega o CSV e limpa espaços extras de todas as células
        df = pd.read_csv(path_base, dtype=str).apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        # 1. Localiza o Bairro (Procura em todas as colunas até achar o bairro digitado)
        mask_bairro = df.apply(lambda row: row.astype(str).str.contains(bairro, case=False).any(), axis=1)
        df_local = df[mask_bairro].copy()

        if df_local.empty:
            print(f"⚠️ Bairro {bairro} não localizado.")
            return

        print(f"✅ Sucesso! {len(df_local)} registros encontrados na região de {bairro}.")
        
        # 2. Filtro de Atividade
        filtro_input = input("\nO que busca? (ex: TRANSPORTE, ROUPAS, BELEZA): ").strip()
        if filtro_input:
            termo = self.remover_acentos(filtro_input)
            # Busca o termo em QUALQUER coluna do arquivo (garante que ache o CNAE)
            mask_ativ = df_local.apply(lambda row: row.astype(str).str.contains(termo, case=False).any(), axis=1)
            df_local = df_local[mask_ativ]
            print(f"🔍 Filtrado para '{termo}': {len(df_local)} negócios.")

        if df_local.empty: return

        # 3. Geocodificação (usando índices fixos que foi mapeado antes para o endereço)
        df_local['lat'], df_local['lon'] = None, None
        df_mapa = df_local.head(15).copy()

        print(f"\n🌍 Localizando {len(df_mapa)} pontos no mapa...")
        for idx, row in df_mapa.iterrows():
            # Peguei as colunas 14 (Rua), 15 (Num) e 17 (Bairro) pelo índice numérico
            try:
                endereco = f"{row.iloc[14]}, {row.iloc[83]}, {bairro}, {cidade}, MG"
                location = self.geolocator.geocode(endereco, timeout=10)
                if location:
                    df_mapa.at[idx, 'lat'] = location.latitude
                    df_mapa.at[idx, 'lon'] = location.longitude
                print(f"✅ Registro localizado.")
                time.sleep(1.2)
            except:
                continue

        output_name = f"geo_{slug_cidade}_{bairro.lower()}.csv"
        df_mapa.dropna(subset=['lat']).to_csv(os.path.join(self.processed_dir, output_name), index=False)
        print(f"\n✨ Arquivo pronto: {output_name}")

if __name__ == "__main__":
    GeoRetailExplorer().buscar_oportunidades()


