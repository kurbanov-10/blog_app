from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from schemas import BlogCreate,BlogOut,BlogUpdate, BlogComment
from database import Base, get_db, engine
from models import Blog



Base.metadata.create_all(bind=engine)
api_router = APIRouter(prefix='/api/posts')


@api_router.post('/', response_model=BlogOut)
def create_post(post_in: BlogCreate, db = Depends(get_db)):
    post = Blog(
            author = post_in.author,
            title = post_in.title,
            content = post_in.content )
    
    db.add(post)
    db.commit()
    db.refresh(post)

    return  post


@api_router.get('/', response_model=List[BlogOut])
def get_posts(db = Depends(get_db)):
    stmt = select(Blog)
    posts = db.scalars(stmt).all()
    
    if not posts:
        raise HTTPException(status_code=404, detail="postlar mavjud emas")
    
    return posts


@api_router.get('/{post_id}', response_model=BlogOut)
def get_post_id(post_id: int, db = Depends(get_db)):
    stmt = select(Blog).where(Blog.id == post_id)
    post = db.scalar(stmt)

    if not post:
        raise HTTPException(status_code=404, detail=f"{post_id}-raqamli post mavjud emas")

    return post


@api_router.put('/{post_id}', response_model=BlogOut)
def update_post(post_id: int, post_in: BlogUpdate, db = Depends(get_db)):
    stmt = select(Blog).where(Blog.id == post_id)
    post: BlogOut = db.scalar(stmt)

    if not post:
        raise HTTPException(status_code=404, detail=f"{post_id}-raqamli post mavjud emas")

    post.author = post_in.author
    post.title = post_in.title
    post.content = post_in.content

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@api_router.delete('/{post_id}')
def delete_post(post_id: int, db = Depends(get_db)):
    stmt = select(Blog).where(Blog.id == post_id)
    post = db.scalar(stmt)

    if not post:
        raise HTTPException(status_code=404, detail=f"{post_id}-raqamli post mavjud emas")

    db.delete(post)
    db.commit()

    return {"status": 204}

@api_router.put('/{post_id/comment}')
def comment_post(post_id:int,post_in: BlogComment, db=Depends(get_db)):

    stmt = select(Blog).where(Blog.id == post_id)
    post = db.scalar(stmt)

    post.comment = post_in.comment

    db.add(post)
    db.commit()
    db.refresh(post)
    
    if not post:
        raise HTTPException(status_code=404, detail=f"{post_id}-raqamli post mavjud emas")


    return post