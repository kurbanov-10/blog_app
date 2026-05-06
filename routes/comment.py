from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import select

from schemas.comment import CommentCreate, CommentOut, CommentUpdate

from database import get_db
from models import Blog, User, Comment

comment_router = APIRouter(tags=["Comment"], prefix='/api/comment')


@comment_router.post('/', response_model=CommentOut)
async def create_comment(comment_in: CommentCreate, db: Session = Depends(get_db)):
    stmt = select(User).where(User.id == comment_in.user_id)
    user = await db.scalar(stmt)

    if not user:
        raise HTTPException(status_code=404, detail=f"{comment_in.user_id}-raqamli user mavjud emas")

    stmt = select(Blog).where(Blog.id == comment_in.blog_id)
    blog = await db.scalar(stmt)

    if not blog:
        raise HTTPException(status_code=404, detail=f"{comment_in.blog_id}-raqamli post mavjud emas")

    comment = Comment(**comment_in.model_dump())

    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    return comment


@comment_router.get('/', response_model=List[CommentOut])
async def get_comments(db=Depends(get_db)):
    stmt = select(Comment)
    result = await db.scalars(stmt)
    comments = result.all()
    return comments


@comment_router.post('/comments/{comment_id}/', response_model=CommentOut)
async def update_comment(comment_id: int, comment_in: CommentUpdate, db=Depends(get_db)):
    stmt = select(Comment).where(Comment.id == comment_id)
    comment: CommentOut = await db.scalar(stmt)

    if not comment:
        raise HTTPException(status_code=404, detail=f"{comment_id}-raqamli comment mavjud emas")

    comment.commentary = comment_in.commentary
    comment.user_id = comment_in.user_id
    comment.blog_id = comment_in.blog_id

    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    return comment


@comment_router.delete('/{comment_id}/')
async def delete_coment(comment_id: int, db=Depends(get_db)):
    stmt = select(Comment).where(Comment.id == comment_id)
    comment = await db.scalar(stmt)

    if not comment:
        raise HTTPException(status_code=404, detail=f"{comment_id}-raqamli comment mavjud emas")

    db.delete(comment)
    await db.commit()

    return
