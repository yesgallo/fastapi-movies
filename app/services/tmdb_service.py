import requests
import os

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "TU_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# ✅ Helper para requests
def _get(endpoint: str, params: dict = None):
    url = f"{BASE_URL}/{endpoint}"
    params = params or {}
    params["api_key"] = TMDB_API_KEY
    params["language"] = "es-ES"  # Puedes cambiar a "en-US" si prefieres
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {}

    return response.json()

# 🔹 Buscar películas por ID
def fetch_movie_by_id(tmdb_id: int):
    data = _get(f"movie/{tmdb_id}")

    if not data or "id" not in data:
        return {
            "id": tmdb_id,
            "title": "Desconocido",
            "overview": "",
            "release_date": None,
            "genres": [],
            "vote_average": 0,
            "vote_count": 0,
            "poster_path": None,
            "backdrop_path": None
        }

    # 🔹 Normalizar géneros
    genres = data.get("genres", [])
    if genres and isinstance(genres[0], dict):
        genres = [g.get("id") for g in genres]

    return {
        "id": data.get("id"),
        "title": data.get("title", "Sin título"),
        "overview": data.get("overview", ""),
        "release_date": data.get("release_date"),
        "genres": genres,
        "vote_average": data.get("vote_average", 0),
        "vote_count": data.get("vote_count", 0),
        "poster_path": data.get("poster_path"),
        "backdrop_path": data.get("backdrop_path")
    }

# 🔹 Importar películas populares
def fetch_popular_movies(page: int = 1):
    data = _get("/movies/import/popular", params={"page": page})
    return data if data else {"results": []}

# 🔹 Buscar películas
def search_movies(query: str):
    data = _get("search/movie", params={"query": query})
    return data if data else {"results": []}
