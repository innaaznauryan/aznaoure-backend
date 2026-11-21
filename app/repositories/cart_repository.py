from sqlalchemy.orm import Session, joinedload

from app.models.cart import CartItem
from app.models.product import Product


class CartRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_items(self, user_id: int) -> list[CartItem]:
        return (
            self.db.query(CartItem)
            .options(joinedload(CartItem.product))
            .filter(CartItem.user_id == user_id)
            .order_by(CartItem.created_at)
            .all()
        )

    def get_item(self, user_id: int, product_id: str) -> CartItem | None:
        return (
            self.db.query(CartItem)
            .options(joinedload(CartItem.product))
            .filter(CartItem.user_id == user_id, CartItem.product_id == product_id)
            .first()
        )

    def add_quantity(
        self, user_id: int, product: Product, quantity: int
    ) -> CartItem | None:
        item = (
            self.db.query(CartItem)
            .filter(CartItem.user_id == user_id, CartItem.product_id == product.id)
            .with_for_update()
            .first()
        )
        updated_quantity = (item.quantity if item else 0) + quantity
        if updated_quantity > product.available:
            return None

        if item:
            item.quantity = updated_quantity
        else:
            item = CartItem(
                user_id=user_id, product_id=product.id, quantity=updated_quantity
            )
            self.db.add(item)

        self.db.commit()
        return self.get_item(user_id, product.id)

    def set_quantity(
        self, user_id: int, product_id: str, quantity: int
    ) -> CartItem | None:
        item = self.get_item(user_id, product_id)
        if item is None:
            return None

        item.quantity = quantity
        self.db.commit()
        return self.get_item(user_id, product_id)

    def remove(self, user_id: int, product_id: str) -> None:
        self.db.query(CartItem).filter(
            CartItem.user_id == user_id, CartItem.product_id == product_id
        ).delete()
        self.db.commit()