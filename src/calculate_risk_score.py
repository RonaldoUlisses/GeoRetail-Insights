# ESTE CÓDIGO CALCULA O ÍNDICE DE RISCO DE CRIMES POR MUNICÍPIO COM BASE NOS DADOS DE SEGURANÇA REGIONAL.
# O SCORE DE RISCO É NORMALIZADO ENTRE 0 E 10, ONDE 10 REPRESENTA O MAIOR RISCO RELATIVO ENTRE OS MUNICÍPIOS ANALISADOS.
# OS RESULTADOS SÃO SALVOS NA TABELA 'tb_score_risco_municipio' NO BANCO DE DADOS E EXIBIDOS NO CONSOLE.


import sqlite3
import pandas as pd

def calcular_score_risco():
    conn = sqlite3.connect("georetail_database.db")
    
    # 1. Carregar os dados de segurança
    df_crimes = pd.read_sql("SELECT * FROM tb_seguranca_regional", conn)
    
    if df_crimes.empty:
        print("❌ Tabela de segurança não encontrada ou vazia.")
        conn.close()
        return

    # Padronizar nomes das colunas para evitar o KeyError
    df_crimes.columns = [col.upper().strip() for col in df_crimes.columns]
    
    # Tenta encontrar a coluna de município (pode estar como MUNICIPIO ou MUNICÍPIO)
    col_municipio = [c for c in df_crimes.columns if 'MUNIC' in c][0]
    print(f"🔍 Usando a coluna '{col_municipio}' para agrupar os crimes.")

    # 2. Calcular o volume de crimes por município
    risco_por_cidade = df_crimes.groupby(col_municipio).size().reset_index(name='qtd_crimes')
    risco_por_cidade.columns = ['MUNICIPIO', 'qtd_crimes'] # Renomeia para padrão

    # 3. Normalização Min-Max (0 a 10)
    min_c = risco_por_cidade['qtd_crimes'].min()
    max_c = risco_por_cidade['qtd_crimes'].max()
    
    if max_c > min_c:
        risco_por_cidade['score_risco'] = ((risco_por_cidade['qtd_crimes'] - min_c) / (max_c - min_c)) * 10
    else:
        risco_por_cidade['score_risco'] = 5.0
        
    risco_por_cidade['score_risco'] = risco_por_cidade['score_risco'].round(2)

    # 4. Salvar o Score de Risco
    risco_por_cidade.to_sql('tb_score_risco_municipio', conn, if_exists='replace', index=False)
    conn.close()
    
    print("\n🛡️ ÍNDICE DE RISCO CALCULADO COM SUCESSO!")
    print(risco_por_cidade)

if __name__ == "__main__":
    calcular_score_risco()