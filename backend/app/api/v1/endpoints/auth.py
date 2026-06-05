from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, verify_refresh_token
from app.core.dependencies import get_db
from app.repositories.user_repo import UserRepository
from app.schemas.auth import TokenRequest, Token, RefreshRequest, TokenPair

router = APIRouter()


@router.post("/auth/token-admin", response_model=Token)
async def get_admin_token(payload: TokenRequest):
    if payload.admin_secret != settings.admin_secret:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": "admin"})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/auth/telegram", response_model=Token)
async def telegram_auth(payload: TokenRequest, db: AsyncSession = Depends(get_db)):
    if not payload.telegram_id:
        raise HTTPException(status_code=400, detail="telegram_id required")
    repo = UserRepository(db)
    user = await repo.get_by_telegram_id(int(payload.telegram_id))
    if not user:
        # create lightweight user
        user = await repo.create({
            "telegram_id": int(payload.telegram_id),
            "referral_code": "ref-" + str(payload.telegram_id),
        })
    access = create_access_token({"sub": str(user.id)})
    refresh = create_refresh_token({"sub": str(user.id)})
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}



@router.post("/refresh", response_model=Token)
async def refresh_token(payload: RefreshRequest):
    try:
        payload_data = verify_refresh_token(payload.refresh_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user_id = payload_data.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    access = create_access_token({"sub": str(user_id)})
    return {"access_token": access, "token_type": "bearer"}
