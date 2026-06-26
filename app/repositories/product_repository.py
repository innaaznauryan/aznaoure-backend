from sqlalchemy.orm import Session

from app.models.product import Product, ProductCategory
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        category: ProductCategory | None = None,
        featured: bool | None = None,
    ) -> list[Product]:
        query = self.db.query(Product)

        if category is not None:
            query = query.filter(Product.category == category)
        if featured is not None:
            query = query.filter(Product.featured == featured)

        return query.order_by(Product.id).offset(skip).limit(limit).all()

    def get_by_id(self, product_id: str) -> Product | None:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def create(self, product_data: ProductCreate) -> Product:
        product = Product(
            id=product_data.id,
            name=product_data.name.model_dump(),
            price=product_data.price,
            category=product_data.category,
            image=product_data.image,
            description=product_data.description.model_dump(),
            details=[item.model_dump() for item in product_data.details],
            available=product_data.available,
            featured=product_data.featured,
            favorite=product_data.favorite,
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: Product, product_data: ProductUpdate) -> Product:
        for field, value in product_data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)

        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()

    def seed_if_empty(self, products_data: list[dict]) -> None:
        if self.db.query(Product).count() > 0:
            return

        for item in products_data:
            product = Product(
                id=item["id"],
                name=item["name"],
                price=item["price"],
                category=ProductCategory(item["category"]),
                image=item["image"],
                description=item["description"],
                details=item["details"],
                available=item["available"],
                featured=item.get("featured", False),
                favorite=item.get("favorite", False),
            )
            self.db.add(product)

        self.db.commit()
