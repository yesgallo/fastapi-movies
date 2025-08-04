from fastapi import FastAPI
from app.routers import users, movies
from app.database import Base, engine
from app.models import user, movie

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Proyecto de Gestión de Usuarios y Películas")

app.include_router(users.router)
app.include_router(movies.router)

