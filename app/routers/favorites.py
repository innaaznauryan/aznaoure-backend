from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.repositories.favorite_repository import FavoriteRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductResponse

router = APIRouter()


def get_favorite_repository(db: Session = Depends(get_db)) -> FavoriteRepository:
    return FavoriteRepository(db)


def get_product_repository(db: Session = Depends(get_db)) -> ProductRepository:
    return ProductRepository(db)


@router.get("/", response_model=list[ProductResponse])
def list_favorites(
    repo: FavoriteRepository = Depends(get_favorite_repository),
    current_user: User = Depends(get_current_user),
):
    return repo.get_favorite_products(current_user.id)


@router.post("/{product_id}", status_code=status.HTTP_201_CREATED)
def add_favorite(
    product_id: str,
    favorite_repo: FavoriteRepository = Depends(get_favorite_repository),
    product_repo: ProductRepository = Depends(get_product_repository),
    current_user: User = Depends(get_current_user),
):
    if not product_repo.get_by_id(product_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if not favorite_repo.exists(current_user.id, product_id):
        favorite_repo.add(current_user.id, product_id)

    return {"status": "added"}


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(
    product_id: str,
    repo: FavoriteRepository = Depends(get_favorite_repository),
    current_user: User = Depends(get_current_user),
):
    repo.remove(current_user.id, product_id)