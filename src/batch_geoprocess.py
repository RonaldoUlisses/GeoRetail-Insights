# GEOLOCALIZAÇÃO EM MASSA - MODO SEGURO
# Este script é para geolocalizar os registros pendentes (ativos sem latitude/longitude) usando o Nominatim do OpenStreetMap, com uma abordagem mais segura e otimizada para evitar bloqueios.
# Ele tenta identificar os campos de endereço de forma flexível, usando tanto nomes comuns quanto índices padrão da Receita, e inclui salvamentos periódicos para garantir que o progresso não seja perdido.

import pandas as pd
import os
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeopyError

class GeoRetailMassLoader:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.abspath(os.path.join(self.current_dir, ".."))
        self.processed_dir = os.path.join(self.base_dir, "data", "processed")
        self.geolocator = Nominatim(user_agent="georetail_mass_v3")

    def processar_cidade(self):
        print("\n" + "="*45)
        print("🚀 CARGA MÁXIMA - MODO SEGURO")
        print("="*45)
        
        cidade_input = input("Qual cidade deseja processar? ").strip().upper()
        slug_cidade = cidade_input.lower().replace(' ', '_')
        path_base = os.path.join(self.processed_dir, f"base_{slug_cidade}_completa.csv")

        if not os.path.exists(path_base):
            print(f"❌ Arquivo não encontrado: {path_base}")
            return

        df = pd.read_csv(path_base, low_memory=False, dtype=str)
        
        # Garante colunas de latitude/longitude
        if 'latitude' not in df.columns:
            df['latitude'] = None
            df['longitude'] = None

        # Filtra apenas Ativos (Situação cadastral costuma ser a 6ª coluna, índice 5)
        mask_pendente = (df.iloc[:, 5] == "02") & (df['latitude'].isna())
        df_pendente = df[mask_pendente]

        total = len(df_pendente)
        if total == 0:
            print(f"✅ Nada pendente para {cidade_input}.")
            return

        print(f"📊 Registros para processar: {total}")
        
        contador = 0
        try:
            for idx, row in df_pendente.iterrows():
                try:
                    # TENTATIVA 1: Pelos nomes comuns de colunas
                    # TENTATIVA 2: Pelos índices padrão da Receita (14=Rua, 17=Bairro, 15=Número)
                    rua = row.get('logradouro', row.iloc[14])
                    num = row.get('numero', row.iloc[15]) # Usando 15 em vez de 83 por segurança
                    bairro = row.get('bairro', row.iloc[17])
                    
                    endereco = f"{rua}, {num}, {bairro}, {cidade_input}, MG, Brasil"
                    
                    location = self.geolocator.geocode(endereco, timeout=10)
                    
                    if location:
                        df.at[idx, 'latitude'] = str(location.latitude)
                        df.at[idx, 'longitude'] = str(location.longitude)
                        status = "✅"
                    else:
                        df.at[idx, 'latitude'] = 'N/A'
                        status = "⚠️"

                    contador += 1
                    print(f"[{contador}/{total}] {status} {rua}, {num}")

                    if contador % 15 == 0:
                        df.to_csv(path_base, index=False, encoding='utf-8-sig')
                        print("💾 Progresso salvo...")

                    time.sleep(1.2)

                except Exception as e:
                    print(f"❌ Erro no registro {idx}: {e}")
                    continue

        except KeyboardInterrupt:
            print("\n🛑 Pausado.")
        finally:
            df.to_csv(path_base, index=False, encoding='utf-8-sig')
            print(f"\n🏁 Finalizado: {contador} registros novos.")

if __name__ == "__main__":
    GeoRetailMassLoader().processar_cidade()