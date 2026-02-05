# Aqui vamos buscar a concetração de estabelecimentos por bairro; criando um ranking simples;

import pandas as pd
import os

def analisar_bairros():
    # Esta lógica sobe 4 níveis para sair de src/src/src/src e chegar na raiz
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "..", ".."))
    
    cidade = "conselheiro_lafaiete"
    path_base = os.path.join(base_dir, "data", "processed", f"base_{cidade}_completa.csv")

    print(f"📂 Procurando base em: {path_base}")

    if not os.path.exists(path_base):
        print(f"❌ Erro: O arquivo não foi encontrado.")
        print(f"💡 Dica: Verifique se o arquivo existe na pasta: {os.path.dirname(path_base)}")
        return

    print(f"📖 Lendo base de dados... Isso pode levar alguns segundos.")
    # Lemos apenas as colunas que importam para ser mais rápido
    df = pd.read_csv(path_base, dtype=str, usecols=['bairro', 'cnae_descricao', 'nome_fantasia'])

    # 1. Ranking Geral de Bairros
    print(f"\n🏘️ RANKING CONCENTRAÇÃO DE CNPJS POR BAIRROS EM LAFAIETE (TOP 10):")
    # Limpeza para evitar que 'SAO JOAO' e 'Sao Joao' sejam contados separados
    df['bairro'] = df['bairro'].str.strip().str.upper()
    ranking = df['bairro'].value_counts().head(10)
    print(ranking)

    # 2. Foco no São João
    bairro_alvo = "SAO JOAO"
    print(f"\n🎯 ANÁLISE DO BAIRRO: {bairro_alvo}")
    df_bairro = df[df['bairro'] == bairro_alvo]
    
    if not df_bairro.empty:
        print(f"Total de empresas ativas: {len(df_bairro)}")
        print("\n🏢 Top 10 Atividades no São João:")
        print(df_bairro['cnae_descricao'].value_counts().head(10))
    else:
        print(f"⚠️ Bairro {bairro_alvo} não encontrado no arquivo.")

if __name__ == "__main__":
    analisar_bairros()