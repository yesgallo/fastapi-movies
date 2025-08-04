👨‍💻 Descripción

Este proyecto implementa una API REST para la gestión de usuarios y películas, con integración a la API externa The Movie DB (TMDB) para importar datos reales.

🔹 Stack utilizado: FastAPI, SQLAlchemy, SQLite, Pydantic, Requests
🔹 Arquitectura: modular, siguiendo buenas prácticas de desarrollo

🚀 Funcionalidades

✅ CRUD completo para Usuarios
✅ CRUD completo para Películas
✅ Integración con The Movie DB API
✅ Búsqueda de películas externas
✅ Importación de películas populares y por ID
✅ Validación de datos con Pydantic
✅ Manejo de errores y respuestas estructuradas
✅ Documentación automática en /docs

⚙️ Instalación y Configuración

1️⃣ Clonar el repositorio
git clone [URL_DEL_REPOSITORIO]
cd final_api

2️⃣ Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows

3️⃣ Instalar dependencias
pip install -r requirements.txt

4️⃣ Configurar variables de entorno
Editar .env:
TMDB_API_KEY=tu_api_key_aqui
TMDB_BASE_URL=https://api.themoviedb.org/3

▶️ Ejecutar la aplicación
uvicorn app.main:app --reload

📌 Endpoints de documentación:

Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc

🧪 Pruebas Automáticas

Este proyecto incluye un script para probar todos los endpoints principales:

test_api_endpoints.py → Pruebas completas de CRUD, importación y búsqueda en TMDB.

test_tmdb_api.py → Verifica conexión a la API TMDB y lista películas populares.

Ejecutar pruebas:
python test_api_endpoints.py
python test_tmdb_api.py

📚 Explicación del Diseño

FastAPI → Framework rápido y moderno para APIs, con docs automáticas.

SQLAlchemy → ORM para base de datos relacional.

SQLite → Base de datos ligera para proyectos educativos.

Pydantic → Validación estricta de datos.

Services → Lógica separada para consumo de APIs externas (TMDB).

Routers → Modularización de endpoints (Usuarios y Películas).

Soft Delete → Usuarios se desactivan (is_active=False) sin eliminarse físicamente.

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
POST /movies/import/popular-movies – Importar películas populares
GET /movies/search/{query} – Buscar películas en TMDB
DELETE /movies/{id} – Eliminar película

⚡ Flujo de Funcionamiento

Usuarios → Se crean con email único, listan, actualizan y desactivan.
Películas manuales → Creación independiente sin TMDB.
Importación TMDB → Descarga películas populares o por ID y evita duplicados.
Búsqueda TMDB → Consulta directa sin guardar en la BD.
Pruebas automáticas → Validan el correcto funcionamiento de toda la API.

