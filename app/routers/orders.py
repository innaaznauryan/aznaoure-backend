from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.repositories.order_repository import OrderRepository
from app.schemas.order import (
    OrderCreate,
    OrderListResponse,
    OrderResponse,
    OrderUpdateStatus,
)

router = APIRouter()


def get_order_repository(db: Session = Depends(get_db)) -> OrderRepository:
    return OrderRepository(db)


@router.get("/", response_model=list[OrderListResponse])
def list_orders(
    skip: int = 0,
    limit: int = 100,
    repo: OrderRepository = Depends(get_order_repository),
    current_user: User = Depends(get_current_user),
):
    return repo.get_all(current_user.id, skip=skip, limit=limit)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    repo: OrderRepository = Depends(get_order_repository),
    current_user: User = Depends(get_current_user),
):
    order = repo.get_by_id(order_id, current_user.id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return order


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    repo: OrderRepository = Depends(get_order_repository),
    current_user: User = Depends(get_current_user),
):
    return repo.create(current_user.id, order_data)

@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_update: OrderUpdateStatus,
    repo: OrderRepository = Depends(get_order_repository),
    current_user: User = Depends(get_current_user),
):
    order = repo.get_by_id(order_id, current_user.id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return repo.update_status(order, status_update.status)
