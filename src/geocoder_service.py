# 1- COLETANDO DADOS GEOGRAFICOS BASEADOS EM ENDEREÇOS ESTRUTURADOS

# ---------------------------------------------------------
# Geocoding API utilizada:
# Nominatim (OpenStreetMap)
# Documentação oficial:
# https://nominatim.org/release-docs/latest/api/Overview/
# ---------------------------------------------------------

from geopy.geocoders import Nominatim
import time

class GeocoderService:
    def __init__(self):
        # Define o agente do usuário para identificação nas requisições
        self.geolocator = Nominatim(user_agent="georetail_insights_app")

    def obter_coordenadas_estruturado(self, bairro, cidade, estado, pais="Brasil"):
        """Gera a localização detalhada a partir de componentes do endereço"""
        try:
            # Monta a busca padronizada para maior precisão
            query = f"{bairro}, {cidade}, {estado}, {pais}"
            
            # Respeita o limite de 1 requisição por segundo do serviço gratuito
            time.sleep(1) 
            location = self.geolocator.geocode(query)
            
            if location:
                return {
                    "exibicao": location.address,
                    "latitude": location.latitude,
                    "longitude": location.longitude
                }
            return None
        except Exception as e:
            print(f"Erro na geocodificação: {e}")
            return None

if __name__ == "__main__":
    service = GeocoderService()
    
    # Teste com as variáveis definidas via input
    bairro_teste = input("Digite o nome do bairro: ")
    cidade_teste = input("Digite o nome da cidade: ")
    estado_teste = input("Digite a sigla do estado: ")
    
    resultado = service.obter_coordenadas_estruturado(bairro_teste, cidade_teste, estado_teste)
    
    if resultado:
        print(f"\n📍 Localizado: {resultado['exibicao']}")
        print(f"🌎 Coordenadas: {resultado['latitude']}, {resultado['longitude']}")
    else:
        print("\n❌ Endereço não encontrado com os parâmetros fornecidos.")
