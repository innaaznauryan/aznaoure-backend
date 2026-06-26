import enum

from sqlalchemy import Boolean, Enum, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ProductCategory(str, enum.Enum):
    rings = "rings"
    necklaces = "necklaces"
    earrings = "earrings"
    bracelets = "bracelets"
    brooches = "brooches"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[dict] = mapped_column(JSON, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[ProductCategory] = mapped_column(Enum(ProductCategory), nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[dict] = mapped_column(JSON, nullable=False)
    details: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    favorite: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
