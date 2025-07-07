from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
import logging
from .. import models, schemas
from ..database import get_db
from ..utils import hash

logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.userResponse
)
def create_user(payload: schemas.createUser, db: Session = Depends(get_db)):

    # hash the password
    hashedPassword = hash(payload.password)
    payload.password = hashedPassword
    new_user = models.User(**payload.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.userResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} is not found",
        )
    return user
