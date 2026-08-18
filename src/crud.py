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


def get_reviews_by_product(session: Session, producto_id: int) -> List[Review]:
    stmt = select(Review).where(Review.producto_id == producto_id).order_by(Review.fecha.desc())
    return session.exec(stmt).all()


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
