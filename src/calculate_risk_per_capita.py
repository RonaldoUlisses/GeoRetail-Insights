#AQUI ESTÁ O CÓDIGO PARA CALCULAR O RISCO PER CAPITA CORRIGIDO COM A POPULAÇÃO REAL DO CENSO 2022,
#GARANTINDO QUE A TAXA DE CRIMES POR 100 MIL HABITANTES ESTEJA CORRETA. O SCORE DE RISCO É NORMALIZADO ENTRE 0 E 10,
#ONDE 10 REPRESENTA O MAIOR RISCO RELATIVO ENTRE OS MUNICÍPIOS ANALISADOS. 
#OS RESULTADOS SÃO SALVOS NA TABELA 'tb_score_risco_detalhado' NO BANCO DE DADOS E EXIBIDOS NO CONSOLE.


import sqlite3
import pandas as pd

def calcular_risco_per_capita():
    conn = sqlite3.connect("georetail_database.db")
    
    # 1. Carregar Crimes (Unificando nomes para bater com o IBGE)
    df_crimes_raw = pd.read_sql("SELECT * FROM tb_seguranca_regional", conn)
    df_crimes_raw.columns = [c.upper() for c in df_crimes_raw.columns]
    col_mun_crime = [c for c in df_crimes_raw.columns if 'MUNIC' in c][0]
    
    resumo_crimes = df_crimes_raw.groupby(col_mun_crime).size().reset_index(name='qtd_crimes')
    resumo_crimes.columns = ['MUNICIPIO', 'qtd_crimes']
    resumo_crimes['MUNICIPIO'] = resumo_crimes['MUNICIPIO'].str.upper().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.strip()

    # 2. População Real (Censo 2022 Aproximado para garantir a taxa correta)
    # dicionário com a população real para corrigir o erro de soma do banco
    pop_real = {
        'CONSELHEIRO LAFAIETE': 131621,
        'CONGONHAS': 52890,
        'ENTRE RIOS DE MINAS': 15219
    }
    
    df_pop = pd.DataFrame(list(pop_real.items()), columns=['MUNICIPIO', 'POP'])

    # 3. Cruzamento (Merge)
    df_final = pd.merge(resumo_crimes, df_pop, on='MUNICIPIO')

    # 4. Cálculo da Taxa por 100 mil hab
    df_final['crimes_per_100k'] = (df_final['qtd_crimes'] / df_final['POP']) * 100000

    # 5. Score 0 a 10
    max_t = df_final['crimes_per_100k'].max()
    min_t = df_final['crimes_per_100k'].min()
    
    if max_t > min_t:
        df_final['score_risco_per_capita'] = ((df_final['crimes_per_100k'] - min_t) / (max_t - min_t)) * 10
    else:
        df_final['score_risco_per_capita'] = 5.0 # Empate
        
    df_final['score_risco_per_capita'] = df_final['score_risco_per_capita'].round(2)

    # 6. Salvar no banco
    df_final.to_sql('tb_score_risco_detalhado', conn, if_exists='replace', index=False)
    conn.close()
    
    print("\n🛡️ ANÁLISE PER CAPITA CORRIGIDA (POPULAÇÃO REAL)!")
    print(df_final[['MUNICIPIO', 'POP', 'qtd_crimes', 'score_risco_per_capita']])

if __name__ == "__main__":
    calcular_risco_per_capita()