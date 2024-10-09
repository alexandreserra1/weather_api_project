# data_extractor/extractor.py

import sys
import os
import time
import requests
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Adicionar o diretório raiz do projeto ao sys.path para permitir importações do pacote 'app'
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Importar módulos do pacote 'app'
from app import crud, database, models

# Configurações da API WeatherAPI.com
BASE_URL = "http://api.weatherapi.com/v1/current.json"
API_KEY = os.getenv("WEATHERAPI_KEY")

if not API_KEY:
    raise ValueError("A chave de API do WeatherAPI.com não está definida. Verifique o arquivo .env e certifique-se de que 'WEATHERAPI_KEY' está definido.")

CITIES = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Porto Alegre"]

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=10),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(requests.exceptions.RequestException),
)
def get_weather(city: str):
    """
    Faz uma requisição GET para a API WeatherAPI.com para obter dados climáticos de uma cidade.
    """
    params = {
        'key': API_KEY,
        'q': city,
        'lang': 'pt'
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def extract_and_store():
    """
    Extrai dados climáticos de uma lista de cidades e os armazena no banco de dados.
    Evita a inserção de registros duplicados com base na cidade e data/hora.
    """
    # Criar as tabelas no banco de dados, se ainda não existirem
    models.Base.metadata.create_all(bind=database.engine)
    
    # Iniciar uma sessão com o banco de dados
    db: Session = database.SessionLocal()
    
    for city in CITIES:
        try:
            data = get_weather(city)
        except requests.exceptions.HTTPError as e:
            print(f"Erro HTTP ao acessar a cidade {city}: {e}")
            continue
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão ao acessar a cidade {city}: {e}")
            continue
        
        # Extrair os dados de interesse
        current = data.get('current', {})
        location = data.get('location', {})
        if not current or not location:
            print(f"Dados climáticos não disponíveis para {city}")
            continue
        
        weather_data = {
            'city': location.get('name'),
            'region': location.get('region'),
            'country': location.get('country'),
            'latitude': location.get('lat'),
            'longitude': location.get('lon'),
            'temperature': current.get('temp_c'),
            'feels_like': current.get('feelslike_c'),
            'humidity': current.get('humidity'),
            'condition_text': current.get('condition', {}).get('text'),
            'condition_icon': current.get('condition', {}).get('icon'),
            'wind_speed': current.get('wind_kph'),
            'wind_degree': current.get('wind_degree'),
            'wind_dir': current.get('wind_dir'),
            'pressure_mb': current.get('pressure_mb'),
            'precip_mm': current.get('precip_mm'),
            'cloud': current.get('cloud'),
            'uv': current.get('uv'),
            'datetime': current.get('last_updated'),
        }
        
        # Verificar se já existe um registro para a cidade e data/hora
        existing_record = crud.get_weather_by_city_and_datetime(db, weather_data['city'], weather_data['datetime'])
        if existing_record:
            print(f"Dados climáticos para {weather_data['city']} em {weather_data['datetime']} já existem. Pulando inserção.")
            continue
        
        # Inserir os dados no banco de dados
        try:
            crud.create_weather(db=db, weather=weather_data)
            print(f"Dados climáticos para {weather_data['city']} inseridos com sucesso.")
        except Exception as e:
            print(f"Erro ao inserir dados climáticos para {weather_data['city']}: {e}")
            db.rollback()
            continue
        
        # Aguardar um intervalo para evitar sobrecarga na API
        time.sleep(1)
    
    # Fechar a sessão do banco de dados
    db.close()

if __name__ == "__main__":
    extract_and_store()
