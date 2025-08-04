import requests

BASE_URL = "http://127.0.0.1:8000"

# ---------- Usuarios ----------

def test_users():
    print("=== 👤 Testing Usuarios ===")

    # Crear usuario
    user_data = {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "123456",
        "name": "John Doe"
    }
    r = requests.post(f"{BASE_URL}/users/", json=user_data)
    print("POST /users/ →", r.status_code, r.json() if r.status_code != 204 else "No Content")

    # Upsert (crear o actualizar)
    upsert_data = {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "newpass",
        "name": "John Updated"
    }
    r = requests.post(f"{BASE_URL}/users/upsert", json=upsert_data)
    print("POST /users/upsert →", r.status_code, r.json())

    # Listar usuarios
    r = requests.get(f"{BASE_URL}/users/")
    print("GET /users/ →", r.status_code, r.json())

    if r.json():
        user_id = r.json()[0]["id"]

        # Obtener usuario
        r = requests.get(f"{BASE_URL}/users/{user_id}")
        print(f"GET /users/{user_id} →", r.status_code, r.json())

        # Actualizar usuario
        update_data = {"name": "John Edited"}
        r = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
        print(f"PUT /users/{user_id} →", r.status_code, r.json())

        # Eliminar usuario (soft delete)
        r = requests.delete(f"{BASE_URL}/users/{user_id}")
        print(f"DELETE /users/{user_id} →", r.status_code)


# ---------- Películas ----------

def test_movies():
    print("\n=== 🎬 Testing Películas ===")

    # Crear película manual
    movie_data = {
        "tmdb_id": 12345,
        "title": "Mi Película",
        "overview": "Una prueba de creación manual",
        "release_date": "2025-01-01"
    }
    r = requests.post(f"{BASE_URL}/movies/", json=movie_data)
    print("POST /movies/ →", r.status_code, r.json() if r.status_code != 204 else "No Content")

    # Listar películas
    r = requests.get(f"{BASE_URL}/movies/")
    print("GET /movies/ →", r.status_code, r.json())

    if r.json():
        movie_id = r.json()[0]["id"]

        # Actualizar película
        update_data = {"title": "Película Editada"}
        r = requests.put(f"{BASE_URL}/movies/{movie_id}", json=update_data)
        print(f"PUT /movies/{movie_id} →", r.status_code, r.json())

        # Eliminar película
        r = requests.delete(f"{BASE_URL}/movies/{movie_id}")
        print(f"DELETE /movies/{movie_id} →", r.status_code)

    # Buscar película
    r = requests.get(f"{BASE_URL}/movies/search/Mi")
    print("GET /movies/search/Mi →", r.status_code, r.json())

    # Importar película Fight Club (550)
    r = requests.post(f"{BASE_URL}/movies/import/550")
    print("POST /movies/import/550 →", r.status_code, r.json() if r.status_code == 200 else r.text)

    # Importar películas populares
    r = requests.post(f"{BASE_URL}/movies/import/popular-movies")
    print("POST /movies/import/popular-movies →", r.status_code, r.json() if r.status_code == 200 else r.text)


if __name__ == "__main__":
    test_users()
    test_movies()

