# VALIDAÇÃO FINAL DO BANCO DE DADOS
# Este script é para validar que os dados foram corretamente exportados para o banco de dados SQLite
# Ele faz uma consulta simples para verificar se as colunas estão lá e se os dados fazem sentido, especialmente os campos de latitude e longitude.

import sqlite3
import pandas as pd

# Conecta ao banco
conn = sqlite3.connect("georetail_database.db")

# Ajustado para os nomes reais: cnpj_basico, ramo_atividade, renda_media_sm, massa_renda_total
query = """
SELECT 
    MUNICIPIO_REF as CIDADE, 
    cnpj_basico,
    ramo_atividade, 
    latitude, 
    longitude, 
    renda_media_sm,
    renda_estimada_reais,
    massa_renda_total
FROM tb_georetail_master 
WHERE latitude IS NOT NULL
LIMIT 10
"""

try:
    df_check = pd.read_sql(query, conn)
    print("\n🚀 VALIDAÇÃO FINAL - BANCO DE DADOS TURBINADO:")
    print(df_check)
except Exception as e:
    print(f"❌ Erro na consulta: {e}")
    print("\n💡 Verifique se você rodou o 'sql/export_to_sql.py' após a última alteração.")

conn.close()