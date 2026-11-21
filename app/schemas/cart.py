from pydantic import BaseModel, ConfigDict, Field

from app.schemas.product import ProductResponse


class CartQuantity(BaseModel):
    quantity: int = Field(..., gt=0)


class CartItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: str
    quantity: int
    product: ProductResponse