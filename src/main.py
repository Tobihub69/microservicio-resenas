from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from fastapi import Security
import os
from typing import List, Optional
from sqlmodel import Session
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from .database import create_db_and_tables, get_session
from .models import ReviewCreate, ReviewRead, Review
from .crud import create_review, get_reviews, delete_review, get_average_rating

app = FastAPI(title="Microservicio de Reseñas")

# Allow simple browser access for the static UI/demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# API Key security (optional)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_api_key(api_key: str = Security(api_key_header)) -> str | None:
    expected = os.getenv("API_KEY")
    if expected is None:
        # no API key configured -> allow anonymous access
        return None
    if api_key == expected:
        return api_key
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API Key")



@app.get("/", include_in_schema=False)
def root_ui():
    # Serve the static single-page demo UI
    return FileResponse("static/index.html")


@app.post("/resenas", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
def post_resena(review: ReviewCreate, session: Session = Depends(get_session), api_key: str = Depends(get_api_key)):
    # API key protection is applied via dependency below (if configured)
    try:
        created = create_review(session, review)
        return created
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@app.get("/resenas")
def list_resenas(
    producto_id: Optional[int] = None,
    usuario_id: Optional[int] = None,
    min_calificacion: Optional[int] = None,
    page: int = 1,
    size: int = 10,
    session: Session = Depends(get_session),
):
    # pagination params
    if page < 1:
        page = 1
    if size < 1:
        size = 10
    offset = (page - 1) * size
    items, total = get_reviews(
        session,
        producto_id=producto_id,
        usuario_id=usuario_id,
        min_calificacion=min_calificacion,
        offset=offset,
        limit=size,
    )
    return {"items": items, "total": total, "page": page, "size": size}


@app.delete("/resenas/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resena(id: int, session: Session = Depends(get_session), api_key: str = Depends(get_api_key)):
    success = delete_review(session, id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reseña no encontrada")


@app.get("/productos/{id}/promedio")
def producto_promedio(id: int, session: Session = Depends(get_session)):
    promedio, cantidad = get_average_rating(session, id)
    return {"producto_id": id, "promedio": promedio, "cantidad": cantidad}
