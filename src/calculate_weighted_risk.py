import sqlite3
import pandas as pd

def calculate_weighted_risk():
    conn = sqlite3.connect('georetail_database.db')
    
    # Lendo os crimes
    df_crimes = pd.read_sql("SELECT * FROM tb_seguranca_regional", conn)
    
    # Normalizando os nomes das colunas (remove espaços e coloca tudo em minúsculo)
    df_crimes.columns = [c.lower().strip().replace('ï»¿', '') for c in df_crimes.columns]
    
    print(f"📋 Colunas detectadas no banco: {list(df_crimes.columns)}")

    # Dicionário de pesos com nomes em MAIÚSCULO para bater com os dados da SEJUSP
    pesos = {
        'ROUBO CONSUMADO': 1.5,
        'ESTUPRO CONSUMADO': 2.0,
        'EXTORSAO CONSUMADO': 1.2,
        'HOMICIDIO CONSUMADO': 2.0,
        'FURTO CONSUMADO': 0.8 
    }
    
    # Garantindo que a coluna natureza exista após a limpeza
    if 'natureza' in df_crimes.columns:
        # Forçamos a coluna natureza para maiúsculo para bater com o dicionário de pesos
        df_crimes['natureza'] = df_crimes['natureza'].str.upper()
        
        df_crimes['peso_gravidade'] = df_crimes['natureza'].map(pesos).fillna(1.0)
        
        # O campo registros também pode estar com o nome sujo
        col_registros = 'registros' if 'registros' in df_crimes.columns else df_crimes.columns[0]
        
        df_crimes['score_ponderado'] = df_crimes[col_registros] * df_crimes['peso_gravidade']
        
        # Agrupa por município
        df_final = df_crimes.groupby('municipio')['score_ponderado'].sum().reset_index()
        
        # Salva em uma nova tabela
        df_final.to_sql('tb_risco_ponderado', conn, if_exists='replace', index=False)
        print("✅ Sucesso! Tabela 'tb_risco_ponderado' criada.")
        print(df_final.head())
    else:
        print("❌ Erro: Coluna 'natureza' não encontrada mesmo após limpeza!")

    conn.close()

if __name__ == "__main__":
    calculate_weighted_risk()