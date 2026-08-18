from fastapi import FastAPI, Depends, HTTPException, status
from typing import List, Optional
from sqlmodel import Session

from .database import create_db_and_tables, get_session
from .models import ReviewCreate, ReviewRead, Review
from .crud import create_review, get_reviews_by_product, delete_review, get_average_rating

app = FastAPI(title="Microservicio de Reseñas")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/resenas", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
def post_resena(review: ReviewCreate, session: Session = Depends(get_session)):
    try:
        created = create_review(session, review)
        return created
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@app.get("/resenas", response_model=List[ReviewRead])
def list_resenas(producto_id: Optional[int] = None, session: Session = Depends(get_session)):
    if producto_id is None:
        # return all reseñas
        from sqlmodel import select

        stmt = select(Review)
        return session.exec(stmt).all()
    return get_reviews_by_product(session, producto_id)


@app.delete("/resenas/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resena(id: int, session: Session = Depends(get_session)):
    success = delete_review(session, id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reseña no encontrada")


@app.get("/productos/{id}/promedio")
def producto_promedio(id: int, session: Session = Depends(get_session)):
    promedio, cantidad = get_average_rating(session, id)
    return {"producto_id": id, "promedio": promedio, "cantidad": cantidad}
