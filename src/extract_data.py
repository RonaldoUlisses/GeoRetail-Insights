# GEORETAIL - EXTRATOR DE DADOS DE EMPRESAS ATIVAS POR CIDADE
# Basicamente, encontra o código da cidade e extrai os CNPJs ativos daquela localidade.


import pandas as pd
import os

class GeoRetailExtractor:
    def __init__(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.raw_path = os.path.join(self.base_dir, "data", "raw")
        self.processed_dir = os.path.join(self.base_dir, "data", "processed")
        os.makedirs(self.processed_dir, exist_ok=True)

    def extrair(self):
        print("\n--- 🌐 GeoRetail: Extrator de Inteligência ---")
        cidade_nome = input("Digite o nome da cidade (ex: CONSELHEIRO LAFAIETE): ").strip().upper()

        # 1. Busca o Código no Dicionário de Municípios
        arq_mun = next((os.path.join(self.raw_path, f) for f in os.listdir(self.raw_path) if "MUNIC" in f.upper()), None)
        if not arq_mun:
            print("❌ Erro: Arquivo de Municípios não encontrado.")
            return

        df_mun = pd.read_csv(arq_mun, sep=';', encoding='latin-1', header=None, dtype=str)
        # Limpeza pesada no dicionário para garantir o match do código
        df_mun[0] = df_mun[0].str.replace(r'\D', '', regex=True)
        df_mun[1] = df_mun[1].str.replace('"', '').str.strip().str.upper()
        
        res = df_mun[df_mun[1] == cidade_nome]
        if res.empty:
            print(f"❌ Cidade '{cidade_nome}' não encontrada no dicionário.")
            return
        
        codigo_alvo = res.iloc[0][0]
        print(f"📍 Código RFB identificado para {cidade_nome}: {codigo_alvo}")

        # 2. Processamento dos Lotes de Estabelecimentos
        arqs_estab = [os.path.join(self.raw_path, f) for f in os.listdir(self.raw_path) 
                      if "ESTABELE" in f.upper() and not f.endswith(".zip")]

        output_name = f"cnpjs_{cidade_nome.lower().replace(' ', '_')}.csv"
        output_path = os.path.join(self.processed_dir, output_name)
        
        if os.path.exists(output_path): os.remove(output_path)

        total_encontrados = 0
        primeiro_chunk = True

        for arq in arqs_estab:
            print(f"📂 Varrendo lote: {os.path.basename(arq)}")
            reader = pd.read_csv(arq, sep=';', encoding='latin-1', header=None, 
                                 chunksize=500000, dtype=str)

            for chunk in reader:
                # Limpeza radical de aspas e espaços
                chunk = chunk.apply(lambda x: x.str.replace('"', '').str.strip() if x.dtype == "object" else x)
                
                # Filtro por Índice: Coluna 20 (Município) e Coluna 5 (Situação Ativa '02')
                filtro = chunk[(chunk[20] == codigo_alvo) & (chunk[5] == "02")]
                
                if not filtro.empty:
                    filtro.to_csv(output_path, mode='a', index=False, header=primeiro_chunk)
                    primeiro_chunk = False
                    total_encontrados += len(filtro)
            
        print(f"\n✨ SUCESSO! {total_encontrados} empresas ativas encontradas em {cidade_nome}.")
        print(f"📂 Arquivo salvo em: {output_path}")

def main():
    # Esta função será chamada pelo seu Painel de Controle
    extrator = GeoRetailExtractor()
    extrator.extrair()

if __name__ == "__main__":
    # Permite que você ainda execute este script individualmente se desejar
    main()