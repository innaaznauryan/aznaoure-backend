from datetime import date
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_google_id(self, google_id: str) -> User | None:
        return self.db.query(User).filter(User.google_id == google_id).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

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

    def update(self, user: User, data: dict) -> User:
        for field, value in data.items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def link_google_id(self, user: User, google_id: str) -> User:
        user.google_id = google_id
        self.db.commit()
        self.db.refresh(user)
        return user

    @staticmethod
    def can_use_semantic_search(user: User) -> bool:
        if user.semantic_search_date != date.today():
            return True
        return user.semantic_search_count < settings.DAILY_SEMANTIC_SEARCH_LIMIT

    def increment_semantic_search_count(self, user: User) -> None:
        today = date.today()
        if user.semantic_search_date != today:
            user.semantic_search_count = 1
            user.semantic_search_date = today
        else:
            user.semantic_search_count += 1
        self.db.commit()

    @staticmethod
    def semantic_searches_remaining(user: User) -> int:
        if user.semantic_search_date != date.today():
            return settings.DAILY_SEMANTIC_SEARCH_LIMIT
        return max(0, settings.DAILY_SEMANTIC_SEARCH_LIMIT - user.semantic_search_count)