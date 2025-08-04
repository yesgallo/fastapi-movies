from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Crear usuario
@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verificar si username o email ya existen
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Crear o actualizar usuario (Upsert)
@router.post("/upsert", response_model=schemas.UserResponse)
def upsert_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.email).first()

    action = "created"

    if user:
        # Si ya existe, actualiza los datos
        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(user, key, value)
        action = "updated"
        db.commit()
        db.refresh(user)
        result = user
    else:
        # Si no existe, crea uno nuevo
        new_user = models.User(**user_data.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        result = new_user

    # Devuelve el usuario junto con la acción realizada
    return {
        **schemas.UserResponse.from_orm(result).dict(),
        "action": action
    }

# Listar usuarios
@router.get("/", response_model=List[schemas.UserResponse])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

# Obtener usuario por ID
@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Actualizar usuario
@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, updated_user: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if updated_user.username and \
       db.query(models.User).filter(models.User.username == updated_user.username, models.User.id != user_id).first():
        raise HTTPException(status_code=400, detail="Username already registered")

    if updated_user.email and \
       db.query(models.User).filter(models.User.email == updated_user.email, models.User.id != user_id).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    for key, value in updated_user.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


# Eliminar usuario (soft delete)
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False
    db.commit()
    return None
