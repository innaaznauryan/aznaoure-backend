from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class ProductCategory(str, Enum):
    rings = "rings"
    necklaces = "necklaces"
    earrings = "earrings"
    bracelets = "bracelets"
    brooches = "brooches"


class TranslatedString(BaseModel):
    en: str
    hy: str


class ProductBase(BaseModel):
    name: TranslatedString
    price: int = Field(..., ge=0)
    category: ProductCategory
    image: str = Field(..., min_length=1, max_length=255)
    description: TranslatedString
    details: list[TranslatedString] = Field(default_factory=list)
    available: int = Field(default=0, ge=0)
    featured: bool = False


class ProductCreate(ProductBase):
    id: str = Field(..., min_length=1, max_length=100)


class ProductUpdate(BaseModel):
    name: TranslatedString | None = None
    price: int | None = Field(default=None, ge=0)
    category: ProductCategory | None = None
    image: str | None = Field(default=None, min_length=1, max_length=255)
    description: TranslatedString | None = None
    details: list[TranslatedString] | None = None
    available: int | None = Field(default=None, ge=0)
    featured: bool | None = None


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
