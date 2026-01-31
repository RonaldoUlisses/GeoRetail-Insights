from geopy.geocoders import Nominatim
import time

# Inicializa o geocodificador (definindo um nome para o seu projeto)
geolocator = Nominatim(user_agent="GeoRetail_Insights")

def testar_geocodificacao(endereco):
    try:
        print(f"Buscando coordenadas para: {endereco}...")
        location = geolocator.geocode(endereco)
        
        if location:
            print(f"Sucesso!")
            print(f"Endereço Completo: {location.address}")
            print(f"Latitude: {location.latitude}")
            print(f"Longitude: {location.longitude}")
        else:
            print("Endereço não encontrado.")
            
    except Exception as e:
        print(f"Erro: {e}")

# Exemplo de teste (você pode trocar por qualquer endereço de varejo)
if __name__ == "__main__":
    testar_geocodificacao("Avenida Paulista, 1000, São Paulo, Brasil")