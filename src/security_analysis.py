# AQUI ESTAMOS ANALISANDO DADOS DE SEGURANÇA PÚBLICA PARA AS CIDADES DO ECOSSISTEMA
# O OBJETIVO É ENTENDER O PERFIL DE CRIMINALIDADE DAS CIDADES

import pandas as pd
import sqlite3
import os
import glob

def processar_seguranca():
    # Caminhos das pastas
    raw_security_dir = os.path.join("data", "raw", "security")
    db_path = "georetail_database.db"
    
    # 1. Localizar todos os arquivos CSV na pasta de segurança
    arquivos = glob.glob(os.path.join(raw_security_dir, "*.csv"))
    
    if not arquivos:
        print(f"❌ Nenhum arquivo CSV encontrado em {raw_security_dir}")
        return

    lista_df = []
    cidades_alvo = ['CONSELHEIRO LAFAIETE', 'CONGONHAS', 'ENTRE RIOS DE MINAS']

    print(f"📂 Iniciando leitura de {len(arquivos)} arquivos de segurança...")

    for arquivo in arquivos:
        try:
            # Lendo o CSV (arquivos do governo costumam usar sep=';' e encoding latin-1)
            df_temp = pd.read_csv(arquivo, sep=';', encoding='latin-1')
            
            # Padronizar nomes das colunas para maiúsculo para evitar erro de busca
            df_temp.columns = [col.upper() for col in df_temp.columns]
            
            # Filtrar cidades
            #
            col_municipio = [c for c in df_temp.columns if 'MUNIC' in c][0]
            
            df_filtrado = df_temp[df_temp[col_municipio].str.upper().isin(cidades_alvo)].copy()
            
            # Adicionar o nome do arquivo ou ano para histórico
            df_filtrado['FONTE_ARQUIVO'] = os.path.basename(arquivo)
            
            lista_df.append(df_filtrado)
            print(f"✅ {os.path.basename(arquivo)} processado.")
            
        except Exception as e:
            print(f"⚠️ Erro ao processar {arquivo}: {e}")

    if lista_df:
        # Unir todos os anos em um único DataFrame
        df_final = pd.concat(lista_df, ignore_index=True)

        # 2. Salvar no Banco de Dados SQL
        conn = sqlite3.connect(db_path)
        df_final.to_sql('tb_seguranca_regional', conn, if_exists='replace', index=False)
        conn.close()

        print("\n🚀 DADOS DE SEGURANÇA ATUALIZADOS NO BANCO!")
        print(f"📊 Total de registros de crimes importados: {len(df_final)}")
        print("Tabela criada: tb_seguranca_regional")
    else:
        print("❌ Nenhum dado foi processado.")

if __name__ == "__main__":
    processar_seguranca()