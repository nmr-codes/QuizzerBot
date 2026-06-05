from fastapi import Depends, HTTPException, status

from app.core.dependencies import get_current_user


def require_admin(user=Depends(get_current_user)):
    if not getattr(user, "is_admin", False) and not getattr(user, "is_owner", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return user


def require_roles(*roles: str):
    def _checker(user=Depends(get_current_user)):
        # simple role check using boolean flags on user model
        for r in roles:
            if getattr(user, r, False):
                return user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")

    return _checker
