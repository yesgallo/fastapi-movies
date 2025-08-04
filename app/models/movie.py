from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Date
from datetime import datetime
from app.database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    tmdb_id = Column(Integer, unique=True)
    title = Column(String, nullable=False)
    overview = Column(Text)
    release_date = Column(Date)
    genre_ids = Column(String)  
    vote_average = Column(Float)
    vote_count = Column(Integer)
    poster_path = Column(String)
    backdrop_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
