# GEORETAIL - MENU PRINCIPAL
# Este script é o ponto de entrada para o GeoRetail Insights,
# oferecendo um menu interativo para acessar as principais funcionalidades do projeto, 
# como extração de dados, enriquecimento, análise de bairros, motor de geomarketing e preparação de dashboards.

import os
import sys

# Garante que o Python encontre os módulos na pasta src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def menu():
    while True:
        print("\n" + "="*45)
        print("   🌍 GEORAETAIL - INTELIGÊNCIA GEOGRÁFICA")
        print("="*45)
        print("[1] 📥 Extrair Microdados (Filtro por Cidade)")
        print("[2] 💎 Enriquecer Dados (Cruzamento CNAE)")
        print("[3] 📊 Analisar Bairros (Ranking de Densidade)")
        print("[4] 📍 Motor de Geomarketing (Busca Dinâmica)")
        print("[5] 📊 Preparar Dashboard (Power BI)")
        print("[0] ❌ Sair")
        print("="*45)
        
        opcao = input("Escolha uma funcionalidade: ")

        if opcao == "1":
            # Aqui digita a cidade que deseja extrair do arquivo bruto
            from extract_data import main as extrair
            extrair()
        elif opcao == "2":
            # Processa o enriquecimento para a cidade que você informar no script
            from enrich_data import main as enriquecer
            enriquecer()
        elif opcao == "3":
            # Gera o ranking de qualquer cidade já processada
            from neighborhood_analysis import main as analisar
            analisar()
        elif opcao == "4":
            # O motor que pergunta: Cidade? Bairro? Atividade?
            from geomarket_service import GeoRetailExplorer
            GeoRetailExplorer().buscar_oportunidades()
        elif opcao == "5":
            from export_dashboard import main as exportar
            exportar()
        elif opcao == "0":
            print("Encerrando GeoRetail. Até logo!")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()