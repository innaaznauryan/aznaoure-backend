from pydantic import BaseModel, ConfigDict, Field


class AddressCreate(BaseModel):
    phone: str | None = Field(default=None, max_length=50)
    address: str = Field(..., min_length=1, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    zip_code: str = Field(..., min_length=1, max_length=20)
    country: str = Field(..., min_length=1, max_length=100)
    is_default: bool = False



class AddressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    phone: str | None
    address: str
    city: str
    zip_code: str
    country: str
    is_default: bool
