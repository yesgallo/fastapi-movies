import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3")

def test_tmdb_api():
    url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&language=es-ES&page=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("✅ Conexión exitosa con TMDB.")
        print(f"Películas populares encontradas: {len(data.get('results', []))}")
        print("Ejemplo:", data['results'][0]['title'])
    else:
        print("❌ Error al conectar con TMDB.")
        print("Código:", response.status_code)
        print("Respuesta:", response.text)

if __name__ == "__main__":
    test_tmdb_api()
