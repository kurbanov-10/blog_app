from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import select, func

from schemas.post import BlogCreate, BlogOut, BlogUpdate
from schemas.users import UserOut
from database import get_db
from models import Blog
from dependencies import get_current_user

post_router = APIRouter(tags=["Post"], prefix='/api/post')


@post_router.post('/', response_model=BlogOut)
async def create_post(blog_in: BlogCreate, db: Session = Depends(get_db), user: UserOut = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=404, detail=f"{blog_in.user_id}-raqamli user mavjud emas")

    data = blog_in.model_dump()

    blog = Blog(**data)

    db.add(blog)
    await db.commit()
    await db.refresh(blog)

    return blog


@post_router.get('/', response_model=List[BlogOut])
async def get_posts(db=Depends(get_db)):
    stmt = select(Blog)
    result = await db.scalars(stmt)
    posts = result.all()
    return posts


@post_router.get('/')
async def get_posts_pagination(limit: int = 5, offset: int = 0, db: Session = Depends(get_db)):
    stmt = select(Blog).limit(limit).offset(offset)
    result = await db.scalars(stmt)
    posts = result.all()
    post_count = await db.scalar(select(func.count()).select_from(Blog))

    data = {"title": post_count,
            "content": posts,
            "limit": limit,
            "offset": offset}

    return data


@post_router.get('/{post_id}', response_model=BlogOut)
async def get_post_id(post_id: int, db=Depends(get_db)):
    stmt = select(Blog).where(Blog.id == post_id)
    post = await db.scalar(stmt)

    if not post:
        raise HTTPException(status_code=404, detail=f"{post_id}-raqamli post mavjud emas")

    return post


@post_router.put('/{post_id}', response_model=BlogOut)
async def update_post(post_id: int, post_in: BlogUpdate, db=Depends(get_db)):
    stmt = select(Blog).where(Blog.id == post_id)
    post: BlogOut = await db.scalar(stmt)

    if not post:
        raise HTTPException(status_code=404, detail=f"{post_id}-raqamli post mavjud emas")

    post.title = post_in.title
    post.content = post_in.content

    db.add(post)
    await db.commit()
    await db.refresh(post)

    return post


@post_router.delete('/{post_id}')
async def delete_post(post_id: int, db=Depends(get_db)):
    stmt = select(Blog).where(Blog.id == post_id)
    post = await db.scalar(stmt)

    if not post:
        raise HTTPException(status_code=404, detail=f"{post_id}-raqamli post mavjud emas")

    db.delete(post)
    await db.commit()

    return {"status": 204}
