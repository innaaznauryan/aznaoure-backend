import os
from fastapi import Depends, HTTPException, status

from app.auth.dependencies import get_current_user
from app.models.user import User

ADMIN_EMAIL = os.environ["ADMIN_EMAIL"]


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.email != ADMIN_EMAIL:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "admin_only"},
        )
    return current_user