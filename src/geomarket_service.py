# GEORETAIL EXPLORER – ANÁLISE ESPACIAL DE ATIVIDADES ECONÔMICAS
# Este script é para explorar os dados de estabelecimentos em uma cidade e bairro específicos, utilizando geocodificação para mapear os locais e gerar arquivos prontos para visualização.
# Ele permite filtrar por tipo de atividade, e salva as coordenadas geográficas na base principal para uso em dashboards e análises futuras.

# Aqui é o cerebro dinâmico para buscar oportunidades de negócios em bairros específicos;
# Utiliza geocodificação para mapear locais e gerar arquivos prontos para visualização;

import pandas as pd
import os
import time
import unicodedata
from geopy.geocoders import Nominatim

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

        # Carrega o CSV principal
        df = pd.read_csv(path_base, dtype=str).apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        # 1. Localiza o Bairro
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
            mask_ativ = df_local.apply(lambda row: row.astype(str).str.contains(termo, case=False).any(), axis=1)
            df_local = df_local[mask_ativ]
            print(f"🔍 Filtrado para '{termo}': {len(df_local)} negócios.")

        if df_local.empty: return

        # 3. Geocodificação com "Carimbo" na Base Principal
        # Criamos as colunas de coordenadas no DataFrame principal se não existirem
        if 'latitude' not in df.columns:
            df['latitude'] = None
            df['longitude'] = None

        # Vamos processar os primeiros 15 para teste
        df_mapa = df_local.head(15).copy()
        df_mapa['lat'], df_mapa['lon'] = None, None

        print(f"\n🌍 Localizando {len(df_mapa)} pontos por endereço completo...")
        
        for idx, row in df_mapa.iterrows():
            try:
                # Vamos buscar pelos nomes das colunas. 
                # Ajuste os nomes abaixo se forem diferentes no CSV:
                rua = row.get('logradouro', 'RUA DESCONHECIDA')
                num = row.get('numero', 'S/N')
                
                # Se os nomes acima falharem, tentaremos os índices seguros (14 e 15)
                if rua == 'RUA DESCONHECIDA':
                    rua = row.iloc[14]
                    num = row.iloc[15] # Geralmente o número vem logo após a rua

                endereco = f"{rua}, {num}, {bairro}, {cidade}, MG, Brasil"
                
                location = self.geolocator.geocode(endereco, timeout=10)
                
                if location:
                    df.at[idx, 'latitude'] = str(location.latitude)
                    df.at[idx, 'longitude'] = str(location.longitude)
                    
                    print(f"✅ Localizado: {rua}, {num}")
                else:
                    print(f"⚠️ Endereço não encontrado: {rua}")
                
                time.sleep(1.2)
            except Exception as e:
                print(f"❌ Erro ao processar linha {idx}: {e}")
                continue

        # SALVAMENTO FINAL: Atualiza a base principal com as coordenadas
        df.to_csv(path_base, index=False, encoding='utf-8-sig')

        # Gera o arquivo geo_ de conferência
        output_name = f"geo_{slug_cidade}_{bairro.lower()}.csv"
        df_mapa.dropna(subset=['lat']).to_csv(os.path.join(self.processed_dir, output_name), index=False, encoding='utf-8-sig')
        
        print(f"\n✨ SUCESSO! Coordenadas salvas na base principal.")
        print(f"📂 Agora você pode rodar a Opção [5] para o Dashboard.")

if __name__ == "__main__":
    GeoRetailExplorer().buscar_oportunidades()


