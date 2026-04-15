from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import mapped_column,Mapped,relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(length=50), unique=True)
    first_name: Mapped[str] = mapped_column(String(length=100))
    last_name: Mapped[str] = mapped_column(String(length=100))
    hashed_password: Mapped[str] = mapped_column(String(length=200))
    blogs: Mapped['Blog'] = relationship(back_populates='user',
                                         cascade='all, delete-orphan')

    
class Blog(Base):
    __tablename__='Blogs'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # author: Mapped[str] = mapped_column(String(length=100), nullable=True, default="")
    title: Mapped[str]= mapped_column(String(length=200))
    content: Mapped[str]= mapped_column(String(length=200))
    # comment: Mapped[str] = mapped_column(String(length=200),default="")
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped[User] = relationship(back_populates='blogs')
    
