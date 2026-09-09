import enum

from sqlalchemy import Boolean, Enum, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

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
    available: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(768), nullable=True)