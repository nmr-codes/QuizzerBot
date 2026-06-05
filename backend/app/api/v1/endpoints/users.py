from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserRead

router = APIRouter()


@router.post("/users", response_model=UserRead)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    existing = await repo.get_by_telegram_id(int(payload.telegram_id))
    if existing:
        # update fields
        return existing
    user = await repo.create({
        "telegram_id": int(payload.telegram_id),
        "username": payload.username,
        "first_name": payload.first_name,
        "last_name": payload.last_name,
    })
    if not user:
        raise HTTPException(status_code=500, detail="Failed to create user")
    return user


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    user = await repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
