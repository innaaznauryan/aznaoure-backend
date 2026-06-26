from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.address_repository import AddressRepository
from app.schemas.address import AddressCreate, AddressResponse

router = APIRouter()


def get_address_repository(db: Session = Depends(get_db)) -> AddressRepository:
    return AddressRepository(db)


@router.get("/", response_model=list[AddressResponse])
def get_addresses(
    user_id: int,
    repo: AddressRepository = Depends(get_address_repository),
):
    return repo.get_all_by_user(user_id)


@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(
    user_id: int,
    address_data: AddressCreate,
    repo: AddressRepository = Depends(get_address_repository),
):
    return repo.create(user_id, address_data)


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(
    address_id: int,
    user_id: int,
    repo: AddressRepository = Depends(get_address_repository),
):
    address = repo.get_by_id(address_id, user_id)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )
    repo.delete(address)
