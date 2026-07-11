from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_google_id(self, google_id: str) -> User | None:
        return self.db.query(User).filter(User.google_id == google_id).first()

    def create(
        self,
        email: str,
        first_name: str,
        last_name: str,
        hashed_password: str | None = None,
        google_id: str | None = None,
        phone: str | None = None,
    ) -> User:
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            hashed_password=hashed_password,
            google_id=google_id,
            phone=phone,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def link_google_id(self, user: User, google_id: str) -> User:
        user.google_id = google_id
        self.db.commit()
        self.db.refresh(user)
        return user