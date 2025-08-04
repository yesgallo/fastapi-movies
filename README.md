📌 Proyecto Final – API REST con FastAPI, SQLAlchemy y SQLite

👨‍💻 Descripción

Este proyecto implementa una API REST que permite la gestión de usuarios y películas, incluyendo la integración con la API externa The Movie DB (TMDB) para importar datos reales.

Se utilizó FastAPI, SQLAlchemy, SQLite, Pydantic y Requests, siguiendo buenas prácticas de desarrollo y arquitectura modular.

🚀 Funcionalidades

✅ CRUD completo para Usuarios
✅ CRUD completo para Películas
✅ Integración con The Movie DB API
✅ Búsqueda de películas externas
✅ Importación de películas populares y por ID
✅ Validación de datos con Pydantic
✅ Manejo de errores y respuestas estructuradas
✅ Documentación automática en /docs

🏗️ Estructura del Proyecto

final_api/
├── app/
│   ├── __init__.py
│   ├── main.py               # Punto de entrada de la app
│   ├── database.py           # Configuración DB y sesión
│   ├── models/               # Modelos SQLAlchemy
│   │   ├── user.py
│   │   └── movie.py
│   ├── schemas/              # Esquemas Pydantic
│   │   ├── user.py
│   │   └── movie.py
│   ├── routers/              # Rutas separadas (Usuarios / Películas)
│   │   ├── users.py
│   │   └── movies.py
│   └── services/
│       └── tmdb_service.py   # Consumo API externa TMDB
├── test_api_endpoints.py     # Script de pruebas automáticas
├── requirements.txt
├── .env                      # Variables de entorno (TMDB API Key)
└── README.md

⚙️ Instalación y Configuración

1️⃣ Clonar repositorio
git clone [URL_DEL_REPOSITORIO]
cd final_api

2️⃣ Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate     # Mac/Linux
.venv\Scripts\activate        # Windows

3️⃣ Instalar dependencias
pip install -r requirements.txt

4️⃣ Configurar variables de entorno
Editar el archivo .env:
TMDB_API_KEY=tu_api_key_aqui
TMDB_BASE_URL=https://api.themoviedb.org/3

▶️ Ejecutar la aplicación
uvicorn app.main:app --reload

La API estará disponible en:
Swagger UI → http://127.0.0.1:8000/docs
ReDoc → http://127.0.0.1:8000/redoc

🧪 Pruebas Automáticas

Este proyecto incluye un script que prueba todos los endpoints principales.

Ejecutar tests
Con el servidor corriendo en otro terminal:
python test_api_endpoints.py

Salida esperada
Usuarios → crear, listar, actualizar, eliminar ✅
Películas → crear manualmente, listar, importar desde TMDB, buscar en TMDB, eliminar ✅
Todos los requests deberían devolver códigos 200, 201, 204 sin errores 405 ni 422.

📚 Explicación del Diseño

FastAPI: Framework rápido y moderno para APIs, con documentación automática.
SQLAlchemy: ORM para manejar la base de datos relacional SQLite.
SQLite: Base de datos ligera ideal para proyectos educativos.
Pydantic: Validación de datos en entradas y salidas.
Services: Separación de la lógica de consumo de APIs externas (TMDB).
Routers: Modularización de endpoints (Usuarios y Películas).
Soft Delete: Los usuarios no se eliminan físicamente, se desactivan (is_active=False).

🔑 Endpoints principales

👥 Usuarios

POST /users/ – Crear usuario
GET /users/ – Listar usuarios
GET /users/{id} – Obtener usuario
PUT /users/{id} – Actualizar usuario
DELETE /users/{id} – Desactivar usuario

🎬 Películas

POST /movies/ – Crear película manualmente
GET /movies/ – Listar películas
POST /movies/import/{tmdb_id} – Importar película por ID
POST /movies/import/popular – Importar películas populares
GET /movies/search/{query} – Buscar películas en TMDB
DELETE /movies/{id} – Eliminar película

