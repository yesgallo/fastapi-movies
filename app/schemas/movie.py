from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class MovieBase(BaseModel):
    tmdb_id: Optional[int] = None
    title: str
    overview: Optional[str] = None
    release_date: Optional[date] = None
    genre_ids: Optional[str] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    tmdb_id: Optional[int] = None
    title: Optional[str] = None
    overview: Optional[str] = None
    release_date: Optional[date] = None
    genre_ids: Optional[str] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None

class MovieResponse(MovieBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
