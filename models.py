from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import mapped_column,Mapped
from database import Base
    
class Blog(Base):
    __tablename__='Blogs'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author: Mapped[str]= mapped_column(String(length=100))
    title: Mapped[str]= mapped_column(String(length=200))
    content: Mapped[str]= mapped_column(String(length=200))
    comment: Mapped[str] = mapped_column(String(length=200),default="")