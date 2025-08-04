from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db
from app.services import tmdb_service
from datetime import datetime
import json

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)

@router.post("/", response_model=schemas.MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    if movie.tmdb_id:
        existing_movie = db.query(models.Movie).filter(models.Movie.tmdb_id == movie.tmdb_id).first()
        if existing_movie:
            raise HTTPException(status_code=400, detail="Movie already exists")

    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.get("/", response_model=List[schemas.MovieResponse])
def list_movies(
    skip: int = 0, 
    limit: int = 10, 
    title: str = None, 
    db: Session = Depends(get_db)
):
    query = db.query(models.Movie)
    if title:
        query = query.filter(models.Movie.title.ilike(f"%{title}%"))
    movies = query.offset(skip).limit(limit).all()
    return movies

@router.get("/{movie_id}", response_model=schemas.MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.put("/{movie_id}", response_model=schemas.MovieResponse)
def update_movie(movie_id: int, updated_movie: schemas.MovieUpdate, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    for key, value in updated_movie.dict(exclude_unset=True).items():
        setattr(movie, key, value)

    db.commit()
    db.refresh(movie)
    return movie

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    db.delete(movie)
    db.commit()
    return None

@router.post("/import/popular-movies", response_model=List[schemas.MovieResponse])
def import_popular_movies(db: Session = Depends(get_db)):
    data = tmdb_service.fetch_popular_movies()
    imported_movies = []

    for item in data.get("results", []):
        if db.query(models.Movie).filter(models.Movie.tmdb_id == item["id"]).first():
            continue

       
        release_date_str = item.get("release_date")
        release_date = None
        if release_date_str:
            try:
                release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
            except ValueError:
                release_date = None

        movie = models.Movie(
            tmdb_id=item["id"],
            title=item.get("title", "Sin título"),
            overview=item.get("overview"),
            release_date=release_date,  
            genre_ids=json.dumps(item.get("genre_ids", [])),
            vote_average=item.get("vote_average"),
            vote_count=item.get("vote_count"),
            poster_path=item.get("poster_path"),
            backdrop_path=item.get("backdrop_path"),
            created_at=datetime.utcnow()
        )
        db.add(movie)
        db.commit()
        db.refresh(movie)     
        imported_movies.append(movie)

    return imported_movies

@router.post("/import/{tmdb_id}", response_model=schemas.MovieResponse)
def import_movie(tmdb_id: int, db: Session = Depends(get_db)):
    data = tmdb_service.fetch_movie_by_id(tmdb_id)

    existing = db.query(models.Movie).filter(models.Movie.tmdb_id == tmdb_id).first()
    if existing:
        return existing

    genres = data.get("genres", [])
    if genres and isinstance(genres[0], dict):
        genres = [g.get("id") for g in genres]

    release_date_str = data.get("release_date")
    release_date = None
    if release_date_str:
        try:
            release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
        except ValueError:
            release_date = None  

    movie = models.Movie(
        tmdb_id=data.get("id"),
        title=data.get("title", "Sin título"),
        overview=data.get("overview"),
        release_date=release_date,  
        genre_ids=json.dumps(genres),
        vote_average=data.get("vote_average"),
        vote_count=data.get("vote_count"),
        poster_path=data.get("poster_path"),
        backdrop_path=data.get("backdrop_path"),
        created_at=datetime.utcnow()
    )
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie

# Buscar películas en TMDB
@router.get("/search/{query}")
def search_movies(query: str):
    data = tmdb_service.search_movies(query)
    return data.get("results", [])

