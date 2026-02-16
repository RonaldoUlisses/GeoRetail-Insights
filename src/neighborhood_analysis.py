# GEORETAIL - ANÁLISE DE BAIRROS
# Este script é para analisar a concentração de estabelecimentos por bairro em uma cidade específica,
# criando um ranking simples que pode ser usado para identificar áreas de maior atividade econômica e oportunidades de negócios.
# Ele lê a base de dados processada, conta o número de estabelecimentos por bairro, e permite uma busca dinâmica para detalhar um bairro específico,
# mostrando as atividades econômicas mais comuns naquela região.
# Aqui vamos buscar a concetração de estabelecimentos por bairro; criando um ranking simples;

import pandas as pd
import os

def main(): # <--- O painel vai procurar por este nome
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(current_dir, ".."))
    
    print("\n" + "="*45)
    print("📊 GeoRetail: Ranking de Densidade por Bairro")
    print("="*45)

    cidade_input = input("Para qual cidade deseja analisar os bairros? ").strip().upper()
    cidade_slug = cidade_input.lower().replace(' ', '_')
    
    path_base = os.path.join(base_dir, "data", "processed", f"base_{cidade_slug}_completa.csv")

    if not os.path.exists(path_base):
        print(f"❌ Erro: O arquivo não foi encontrado em: {path_base}")
        return

    print(f"📖 Lendo base de dados de {cidade_input}... Aguarde.")
    
    # Lendo apenas as colunas de bairro e cnae
    df = pd.read_csv(path_base, dtype=str, usecols=['bairro', 'cnae_descricao'])

    # 1. Ranking Geral de Bairros
    print(f"\n🏘️ RANKING DE CNPJS POR BAIRROS (TOP 10):")
    df['bairro'] = df['bairro'].str.strip().str.upper()
    ranking = df['bairro'].value_counts().head(10)
    print(ranking)

    # 2. Busca Dinâmica de Bairro
    bairro_alvo = input("\n🎯 Deseja detalhar algum bairro específico? (ou deixe em branco): ").strip().upper()
    
    if bairro_alvo:
        df_bairro = df[df['bairro'] == bairro_alvo]
        if not df_bairro.empty:
            print(f"\n✅ Total de empresas ativas no {bairro_alvo}: {len(df_bairro)}")
            print(f"🏢 Top 10 Atividades no {bairro_alvo}:")
            print(df_bairro['cnae_descricao'].value_counts().head(10))
        else:
            print(f"⚠️ Bairro {bairro_alvo} não encontrado.")

if __name__ == "__main__":
    main()