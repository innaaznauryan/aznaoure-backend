from sqlalchemy.orm import Session

from app.models.address import Address
from app.schemas.address import AddressCreate


class AddressRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_user(self, user_id: int) -> list[Address]:
        return (
            self.db.query(Address)
            .filter(Address.user_id == user_id)
            .all()
        )

    def create(self, user_id: int, address_data: AddressCreate) -> Address:
        if address_data.is_default:
            self._unset_default(user_id)

        address = Address(user_id=user_id, **address_data.model_dump())
        self.db.add(address)
        self.db.commit()
        self.db.refresh(address)
        return address

    def delete(self, address: Address) -> None:
        self.db.delete(address)
        self.db.commit()

    def _unset_default(self, user_id: int) -> None:
        self.db.query(Address).filter(Address.user_id == user_id).update(
            {"is_default": False}
        )
