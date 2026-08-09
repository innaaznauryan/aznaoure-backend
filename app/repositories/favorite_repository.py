from sqlalchemy.orm import Session

from app.models.favorite import Favorite
from app.models.product import Product


class FavoriteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_favorite_products(self, user_id: str) -> list[Product]:
        return (
            self.db.query(Product)
            .join(Favorite, Favorite.product_id == Product.id)
            .filter(Favorite.user_id == user_id)
            .all()
        )

    def exists(self, user_id: str, product_id: str) -> bool:
        return (
            self.db.query(Favorite)
            .filter(Favorite.user_id == user_id, Favorite.product_id == product_id)
            .first()
            is not None
        )

    def add(self, user_id: str, product_id: str) -> Favorite:
        favorite = Favorite(user_id=user_id, product_id=product_id)
        self.db.add(favorite)
        self.db.commit()
        self.db.refresh(favorite)
        return favorite

    def remove(self, user_id: str, product_id: str) -> None:
        self.db.query(Favorite).filter(
            Favorite.user_id == user_id, Favorite.product_id == product_id
        ).delete()
        self.db.commit()