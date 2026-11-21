from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.user import get_current_user
from app.database import get_db
from app.models.user import User
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.cart import CartItemResponse, CartQuantity

router = APIRouter()


def get_cart_repository(db: Session = Depends(get_db)) -> CartRepository:
    return CartRepository(db)


def get_product_repository(db: Session = Depends(get_db)) -> ProductRepository:
    return ProductRepository(db)


@router.get("/", response_model=list[CartItemResponse])
def get_cart(
    repo: CartRepository = Depends(get_cart_repository),
    current_user: User = Depends(get_current_user),
):
    return repo.get_items(current_user.id)


@router.post("/{product_id}", response_model=CartItemResponse)
def add_to_cart(
    product_id: str,
    payload: CartQuantity,
    cart_repo: CartRepository = Depends(get_cart_repository),
    product_repo: ProductRepository = Depends(get_product_repository),
    current_user: User = Depends(get_current_user),
):
    product = product_repo.get_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    item = cart_repo.add_quantity(current_user.id, product, payload.quantity)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Requested quantity exceeds available stock",
        )
    return item


@router.patch("/{product_id}", response_model=CartItemResponse)
def update_cart_quantity(
    product_id: str,
    payload: CartQuantity,
    cart_repo: CartRepository = Depends(get_cart_repository),
    product_repo: ProductRepository = Depends(get_product_repository),
    current_user: User = Depends(get_current_user),
):
    product = product_repo.get_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if payload.quantity > product.available:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Requested quantity exceeds available stock",
        )

    item = cart_repo.set_quantity(current_user.id, product_id, payload.quantity)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    return item


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(
    product_id: str,
    repo: CartRepository = Depends(get_cart_repository),
    current_user: User = Depends(get_current_user),
):
    repo.remove(current_user.id, product_id)