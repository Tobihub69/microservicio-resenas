from typing import List, Optional, Tuple
from sqlmodel import Session, select, func
from .models import Review, ReviewCreate


def create_review(session: Session, review_in: ReviewCreate) -> Review:
    stmt = select(Review).where(
        (Review.producto_id == review_in.producto_id)
        & (Review.usuario_id == review_in.usuario_id)
    )
    existing = session.exec(stmt).first()
    if existing:
        raise ValueError("El usuario ya calificó este producto")
    review = Review.from_orm(review_in)
    session.add(review)
    session.commit()
    session.refresh(review)
    return review


def get_reviews(
    session: Session,
    producto_id: Optional[int] = None,
    usuario_id: Optional[int] = None,
    min_calificacion: Optional[int] = None,
    offset: int = 0,
    limit: int = 10,
) -> Tuple[List[Review], int]:
    q = select(Review)
    if producto_id is not None:
        q = q.where(Review.producto_id == producto_id)
    if usuario_id is not None:
        q = q.where(Review.usuario_id == usuario_id)
    if min_calificacion is not None:
        q = q.where(Review.calificacion >= min_calificacion)
    total = session.exec(select(func.count(Review.id)).where(q.whereclause) if q.whereclause is not None else select(func.count(Review.id))).one()
    # order and paginate
    q = q.order_by(Review.fecha.desc()).offset(offset).limit(limit)
    items = session.exec(q).all()
    return items, int(total)


def delete_review(session: Session, id: int) -> bool:
    review = session.get(Review, id)
    if not review:
        return False
    session.delete(review)
    session.commit()
    return True


def get_average_rating(session: Session, producto_id: int) -> Tuple[Optional[float], int]:
    stmt = select(func.avg(Review.calificacion), func.count(Review.id)).where(Review.producto_id == producto_id)
    avg_val, count = session.exec(stmt).one()
    if count == 0:
        return None, 0
    return float(avg_val), count
