from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCategory, ProductCreate, ProductResponse, ProductUpdate

router = APIRouter()


def get_product_repository(db: Session = Depends(get_db)) -> ProductRepository:
    return ProductRepository(db)


@router.get("/", response_model=list[ProductResponse])
def list_products(
    skip: int = 0,
    limit: int = 100,
    category: ProductCategory | None = None,
    featured: bool | None = Query(default=None),
    repo: ProductRepository = Depends(get_product_repository),
):
    return repo.get_all(skip=skip, limit=limit, category=category, featured=featured)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: str,
    repo: ProductRepository = Depends(get_product_repository),
):
    product = repo.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    repo: ProductRepository = Depends(get_product_repository),
):
    if repo.get_by_id(product_data.id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product with this id already exists",
        )
    return repo.create(product_data)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    product_data: ProductUpdate,
    repo: ProductRepository = Depends(get_product_repository),
):
    product = repo.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return repo.update(product, product_data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: str,
    repo: ProductRepository = Depends(get_product_repository),
):
    product = repo.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    repo.delete(product)
