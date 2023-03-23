from sqlalchemy.orm import Session
from ..database import models, schemas
from fastapi import HTTPException, status
from ..authentication.hashing import Hash


def show_all(db: Session):
    sock = db.query(models.Sock).all()
    if not sock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No sock available",
        )
    return sock


def show_specific(id: int, db: Session):
    sock = db.query(models.Sock).filter(models.Sock.id == id).first()
    if not sock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sock with the id {id} is not available",
        )
    return sock


# def create(request: schemas.User, db: Session):
#     new_user = models.User(
#         name=request.name, email=request.email, password=Hash.bcrypt(request.password)
#     )
#     # db.add(new_user)
#     # db.commit()
#     # db.refresh(new_user)
#     return new_user
