from pydantic import BaseModel, Field


class BlogBase(BaseModel):
    author: str = Field(max_length=100)
    title: str = Field(max_length=100)
    content: str = Field(max_length=200)

class BlogCreate(BlogBase):
    pass

class BlogOut(BlogBase):
    id: int = Field(ge=1)
    comment: str = Field(max_length=200)

class BlogUpdate(BlogBase):
    content: str = Field(max_length=200)
    title: str = Field(max_length=200)
    
class BlogComment(BlogBase):
    comment: str = Field(max_length=200)