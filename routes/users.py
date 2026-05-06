import security
import time

from fastapi import HTTPException, Depends, BackgroundTasks, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm

from schemas.users import UserCreate, UserOut
from schemas.post import Token
from database import get_db
from models import User
from email_service import send_welcome_email


users_router = APIRouter(tags=["User"], prefix='/api/users')


@users_router.post('/', response_model=UserOut)
async def create_user(bg_tasks: BackgroundTasks, user_in: UserCreate, db: Session = Depends(get_db)):
    time.sleep(2)
    user = await db.scalar(select(User).where(User.username == user_in.username))
    if user:
        raise HTTPException(status_code=400, detail=f"{user_in.username} bunday foydalanuvchi mavjud")

    user_dict = user_in.model_dump()
    hashed_password = await security.get_password_hash(user_dict.pop("password"))

    user = User(**user_dict, hashed_password=hashed_password)

    db.add(user)
    await db.commit()
    await db.refresh(user)

    bg_tasks.add_task(send_welcome_email, f"{user.username}@gmail.com")

    return user


@users_router.post('/login/', response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.username == form.username))
    if not user:
        raise HTTPException(status_code=400, detail="bunday foydalanuvchi mavjud emas")

    if not security.verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="username yoki parol noto'g'ri")

    access_token = await security.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
