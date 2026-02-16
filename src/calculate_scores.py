# ESTE CÓDIGO CALCULA O SCORE DE POTENCIAL DE VENDAS PARA CADA BAIRRO/SETOR COM BASE NA RENDA MÉDIA E NA MASSA DE RENDA TOTAL.
# O SCORE É NORMALIZADO ENTRE 0 E 10, ONDE 10 REPRESENTA O MAIOR POTENCIAL RELATIVO ENTRE OS REGISTROS ANALISADOS.
# OS RESULTADOS SÃO SALVOS NA TABELA 'tb_georetail_master' NO BANCO DE DADOS E EXIBIDOS NO CONSOLE.


import sqlite3
import pandas as pd

def calcular_scores():
    conn = sqlite3.connect("georetail_database.db")
    
    # Lendo todos os dados do banco
    df = pd.read_sql("SELECT * FROM tb_georetail_master", conn)
    
    if df.empty:
        print("❌ Banco vazio! Certifique-se de que exportou os dados primeiro.")
        return

    # 1. Normalização Min-Max (Transforma valores brutos em escala 0-1)
    # Criando a nota baseada na Renda Média e na Massa de Renda Total
    df['n_renda'] = (df['renda_media_sm'] - df['renda_media_sm'].min()) / (df['renda_media_sm'].max() - df['renda_media_sm'].min())
    df['n_massa'] = (df['massa_renda_total'] - df['massa_renda_total'].min()) / (df['massa_renda_total'].max() - df['massa_renda_total'].min())
    
    # 2. Cálculo do Score (0 a 10)
    # Peso equilibrado: 50% para renda individual, 50% para volume financeiro do bairro
    df['score_potencial'] = ((df['n_renda'] * 5) + (df['n_massa'] * 5)).round(2)
    
    # Preenche possíveis valores nulos com 0
    df['score_potencial'] = df['score_potencial'].fillna(0)

    # 3. Salva de volta no Banco de Dados
    df.to_sql('tb_georetail_master', conn, if_exists='replace', index=False)
    conn.close()
    
    print("\n🚀 INTELIGÊNCIA GEOGRÁFICA ATUALIZADA!")
    print("✅ Score de Potencial (0-10) calculado para todos os registros.")
    
    # Mostra os 5 bairros/setores com maior potencial na região
    top_spots = df[['MUNICIPIO_REF', 'bairro', 'ramo_atividade', 'score_potencial']].sort_values(by='score_potencial', ascending=False).head(5)
    print("\n🔝 TOP 5 OPORTUNIDADES NA REGIÃO:")
    print(top_spots)

if __name__ == "__main__":
    calcular_scores()