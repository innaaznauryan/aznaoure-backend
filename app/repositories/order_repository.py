from sqlalchemy.orm import Session, joinedload

from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import OrderCreate


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, user_id: int, skip: int = 0, limit: int = 100) -> list[Order]:
        return (
            self.db.query(Order)
            .filter(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, order_id: int, user_id: int) -> Order | None:
        return (
            self.db.query(Order)
            .options(joinedload(Order.items))
            .filter(Order.id == order_id, Order.user_id == user_id)
            .first()
        )

    def create(self, user_id: int, order_data: OrderCreate) -> Order:
        subtotal = sum(
            item.unit_price * item.quantity for item in order_data.items
        )
        total_amount = subtotal + order_data.shipping_cost

        order = Order(
            user_id=user_id,
            email=order_data.email,
            phone=order_data.phone,
            first_name=order_data.first_name,
            last_name=order_data.last_name,
            address=order_data.address,
            city=order_data.city,
            zip_code=order_data.zip_code,
            country=order_data.country,
            subtotal=subtotal,
            shipping_cost=order_data.shipping_cost,
            total_amount=total_amount,
            status=OrderStatus.pending,
            items=[
                OrderItem(
                    product_id=item.product_id,
                    product_name=item.product_name,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
                for item in order_data.items
            ],
        )

        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return self.get_by_id(order.id, user_id)

    def update_status(self, order: Order, status: OrderStatus) -> Order:
        order.status = status
        self.db.commit()
        self.db.refresh(order)
        return order
