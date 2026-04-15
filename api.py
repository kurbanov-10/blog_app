import security
import jwt

from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select  
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from schemas import BlogCreate,BlogOut,BlogUpdate, UserCreate, UserOut, Token, CommentCreate, CommentOut, CommentUpdate
from database import Base, get_db, engine
from models import Blog,User, Comment



Base.metadata.create_all(bind=engine)
api_router = APIRouter(prefix='/api/posts')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token yaroqsiz yoki muddati tugagan"
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = db.scalar(select(User).where(User.id == int(user_id)))
    if user is None:
        raise credentials_exception

    return user

@api_router.post('/users', response_model=UserOut)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == user_in.username))
    if user:
        raise HTTPException(status_code=400, detail=f"{user_in.username} bunday foydalanuvchi mavjud")

    user_dict = user_in.model_dump()
    hashed_password = security.get_password_hash(user_dict.pop("password"))
    
    user = User(**user_dict, hashed_password=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@api_router.post('/users/login', response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == form.username))
    if not user:
        raise HTTPException(status_code=400, detail="bunday foydalanuvchi mavjud emas")

    if not security.verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="username yoki parol noto'g'ri")

    access_token = security.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.post('/', response_model=BlogOut)
def create_post(blog_in: BlogCreate, db: Session = Depends(get_db)):
    stmt = select(User).where(User.id == blog_in.user_id)
    user = db.scalar(stmt)

    if not user:
        raise HTTPException(status_code=404, detail=f"{blog_in.user_id}-raqamli user mavjud emas")

    blog = Blog(**blog_in.model_dump())

    db.add(blog)
    db.commit()
    db.refresh(blog)

    return blog


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

@api_router.post('/comments', response_model=CommentOut)
def create_comment(comment_in: CommentCreate, db: Session = Depends(get_db)):
    stmt = select(User).where(User.id == comment_in.user_id)
    user = db.scalar(stmt)

    if not user:
        raise HTTPException(status_code=404, detail=f"{comment_in.user_id}-raqamli user mavjud emas")

    stmt = select(Blog).where(Blog.id == comment_in.blog_id)
    blog = db.scalar(stmt)

    if not blog:
        raise HTTPException(status_code=404, detail=f"{comment_in.blog_id}-raqamli post mavjud emas")

    comment = Comment(**comment_in.model_dump())

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment

@api_router.get('/comments', response_model=List[CommentOut])
def get_comments(db = Depends(get_db)):
    stmt = select(Comment)
    comments = db.scalars(stmt).all()
    
    if not comments:
        raise HTTPException(status_code=404, detail="commentlar mavjud emas")
    
    return comments

@api_router.post('/comments/{comment_id}', response_model=CommentOut)
def update_comment(comment_id: int, comment_in: CommentUpdate, db = Depends(get_db)):
    stmt = select(Comment).where(Comment.id == comment_id)
    comment: CommentOut = db.scalar(stmt)

    if not comment:
        raise HTTPException(status_code=404, detail=f"{comment_id}-raqamli comment mavjud emas")

    comment.commentary = comment_in.commentary
    comment.user_id = comment_in.user_id
    comment.blog_id = comment_in.blog_id

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment

@api_router.delete('/{comment_id}')
def delete_post(comment_id: int, db = Depends(get_db)):
    stmt = select(Comment).where(Comment.id == comment_id)
    comment = db.scalar(stmt)

    if not comment:
        raise HTTPException(status_code=404, detail=f"{comment_id}-raqamli comment mavjud emas")

    db.delete(comment)
    db.commit()

    return