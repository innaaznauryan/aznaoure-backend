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


class ProductCreate(BaseModel):
    id: str = Field(..., min_length=1, max_length=100)
    name: TranslatedString
    price: int = Field(..., ge=0)
    category: ProductCategory
    image: str = Field(..., min_length=1, max_length=255)
    description: TranslatedString
    details: list[TranslatedString] = Field(default_factory=list)
    featured: bool = False
    favorite: bool = False


class ProductUpdate(BaseModel):
    name: TranslatedString | None = None
    price: int | None = Field(default=None, ge=0)
    category: ProductCategory | None = None
    image: str | None = Field(default=None, min_length=1, max_length=255)
    description: TranslatedString | None = None
    details: list[TranslatedString] | None = None
    featured: bool | None = None
    favorite: bool | None = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: TranslatedString
    price: int
    category: ProductCategory
    image: str
    description: TranslatedString
    details: list[TranslatedString]
    available: bool
    featured: bool
    favorite: bool
