import time
import requests
from geopy.geocoders import Nominatim

class GeoMarketService:
    def __init__(self):
        # Inicializa o geocodificador
        self.geolocator = Nominatim(user_agent="georetail_insights_app")
        # API para busca de CNPJs (Minha Receita / BrasilAPI)
        self.api_cnpj = "https://brasilapi.com.br/api/cnpj/v1/"

    def obter_coordenadas(self, bairro, cidade, estado):
        """Localiza o ponto geográfico e prepara a busca de mercado"""
        try:
            query = f"{bairro}, {cidade}, {estado}, Brasil"
            time.sleep(1) # Respeita o limite do serviço gratuito
            location = self.geolocator.geocode(query)
            
            if location:
                return {
                    "exibicao": location.address,
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "bairro": bairro,
                    "cidade": cidade
                }
            return None
        except Exception as e:
            print(f"Erro na geocodificação: {e}")
            return None

    def analisar_densidade_comercial(self, bairro, cidade):
        """
        Simula a contagem de CNPJs Ativos.
        Para escala real, aqui consultaremos sua base local de microdados.
        """
        print(f"\n🔍 Analisando densidade comercial no bairro {bairro}...")
        
        # Simulando a integração que faremos com os Microdados da Receita
        # Por enquanto, retornamos um status de pronto para integração
        return {
            "status": "Pronto para integração com Microdados",
            "fonte": "Receita Federal do Brasil",
            "municipio_alvo": cidade,
            "bairro_alvo": bairro
        }

if __name__ == "__main__":
    service = GeoMarketService()
    
    print("--- GeoRetail Insights: Motor de Inteligência ---")
    b = input("Digite o nome do bairro: ")
    c = input("Digite o nome da cidade: ")
    e = input("Digite a sigla do estado (ex: MG): ")
    
    # 1. Geocodificação
    resultado = service.obter_coordenadas(b, c, e)
    
    if resultado:
        print(f"\n📍 LOCALIZAÇÃO CONFIRMADA:")
        print(f"Endereço: {resultado['exibicao']}")
        print(f"Coordenadas: {resultado['latitude']}, {resultado['longitude']}")
        
        # 2. Inteligência de Mercado (CORRIGIDO: 'analisar' em vez de 'analisando')
        analise = service.analisar_densidade_comercial(resultado['bairro'], resultado['cidade'])
        print(f"\n📊 {analise['status']} para {analise['bairro_alvo']}.")
        print(f"💡 Próximo passo: Carregar CSV de microdados de {e} em 'data/raw/'.")
        
    else:
        print("\n❌ Não foi possível localizar este endereço. Verifique a ortografia.")