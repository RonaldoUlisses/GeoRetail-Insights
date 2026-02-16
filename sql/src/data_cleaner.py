# ESTE CÓDIGO REALIZA A LIMPEZA DEFINITIVA DO BANCO DE DADOS,
#  MANTENDO APENAS AS COLUNAS ESSENCIAIS NA TABELA MASTER E CORRIGINDO A TABELA DE SEGURANÇA REGIONAL.

import sqlite3
import pandas as pd

def limpeza_definitiva():
    conn = sqlite3.connect('georetail_database.db')
    
    # 1. LIMPANDO A TABELA MASTER (Estabelecimentos + IBGE)
    print("🧹 Enxugando tb_georetail_master...")
    
    # Lista das colunas que importam
    colunas_manter = [
        'cnpj_basico', 'nome_fantasia', 'cnae_codigo', 'ramo_atividade',
        'latitude', 'longitude', 'bairro', 'municipio_ref',
        'renda_media_sm', 'renda_estimada_reais', 'massa_renda_total', 'score_potencial'
    ]
    
    try:
        # Carrega apenas o essencial
        df_master = pd.read_sql(f"SELECT {', '.join(colunas_manter)} FROM tb_georetail_master", conn)
        
        # Tratamento de Nome Fantasia: Se estiver vazio, usa o CNPJ ou um marcador
        df_master['nome_fantasia'] = df_master['nome_fantasia'].fillna('NOME NÃO INFORMADO')
        
        # Salva por cima (Overwrite)
        df_master.to_sql('tb_georetail_master', conn, if_exists='replace', index=False)
        print(f"✅ Master limpa! {len(colunas_manter)} colunas mantidas.")
    except Exception as e:
        print(f"⚠️ Erro na Master: {e}")

    # --- 2. LIMPANDO A TABELA DE SEGURANÇA ---
    print("🧹 Ajustando tb_seguranca_regional...")
    try:
        df_seg = pd.read_sql("SELECT * FROM tb_seguranca_regional", conn)
        
        # Limpa o caractere estranho ï»¿ e renomeia
        df_seg.columns = [c.strip().replace('ï»¿', '') for c in df_seg.columns]
        rename_map = {
            'natureza': 'tipo_crime',
            'municipio': 'cidade',
            'registros': 'qtd_registros'
        }
        df_seg.rename(columns=rename_map, inplace=True)
        
        # Salva por cima
        df_seg.to_sql('tb_seguranca_regional', conn, if_exists='replace', index=False)
        print("✅ Segurança limpa!")
    except Exception as e:
        print(f"⚠️ Erro na Segurança: {e}")

    conn.close()
    print("\n🚀 PROCESSO FINALIZADO: Seu banco de dados está leve e profissional!")

if __name__ == "__main__":
    limpeza_definitiva()