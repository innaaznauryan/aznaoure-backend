from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database import get_db
from app.auth.user import get_current_user
from app.auth.admin import get_current_admin
from app.models.user import User
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.schemas.product import (
    ProductCategory,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    ProductSearchResponse,
    SemanticSearchQuota
)
from app.services.embeddings import embed_text

router = APIRouter()


def get_product_repository(db: Session = Depends(get_db)) -> ProductRepository:
    return ProductRepository(db)

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


@router.get("/", response_model=list[ProductResponse])
def list_products(
    skip: int = 0,
    limit: int = 100,
    category: ProductCategory | None = None,
    featured: bool | None = Query(default=None),
    repo: ProductRepository = Depends(get_product_repository),
):
    return repo.get_all(skip=skip, limit=limit, category=category, featured=featured)


@router.get("/search/quota", response_model=SemanticSearchQuota)
def get_search_quota(
    user_repo: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user),
):
    return SemanticSearchQuota(
        remaining=user_repo.semantic_searches_remaining(current_user),
        limit=settings.DAILY_SEMANTIC_SEARCH_LIMIT,
    )


@router.get("/search", response_model=ProductSearchResponse)
def search_products(
    q: str,
    limit: int = 10,
    repo: ProductRepository = Depends(get_product_repository),
    user_repo: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user),
):
    if user_repo.can_use_semantic_search(current_user):
        try:
            query_embedding = embed_text(q)
            products = repo.semantic_search(query_embedding, limit=limit)
            results = [ProductResponse.model_validate(p) for p in products]
            user_repo.increment_semantic_search_count(current_user)
            remaining = user_repo.semantic_searches_remaining(current_user)
            return ProductSearchResponse(results=results, semantic=True, semantic_remaining=remaining)
        except Exception:
            print("Semantic search unavailable for query %r, using keyword fallback", q)

    products = repo.keyword_search(q, limit=limit)
    results = [ProductResponse.model_validate(p) for p in products]
    remaining = user_repo.semantic_searches_remaining(current_user)
    return ProductSearchResponse(results=results, semantic=False, semantic_remaining=remaining)


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
    current_user: User = Depends(get_current_admin),
):
    if repo.get_by_id(product_data.id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product with this id already exists",
        )
    return repo.create(product_data)


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    product_data: ProductUpdate,
    repo: ProductRepository = Depends(get_product_repository),
    current_user: User = Depends(get_current_admin),
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
    current_user: User = Depends(get_current_admin),
):
    product = repo.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    repo.delete(product)
