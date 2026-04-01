from pydantic import BaseModel, Field

class UserBase(BaseModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)


class UserCreate(UserBase):
    pass


class UserOut(UserBase):
    id: int



class BlogBase(BaseModel):
    # author: str = Field(max_length=100)
    title: str = Field(max_length=100)
    content: str = Field(max_length=200)
    user_id: int

class BlogCreate(BlogBase):
    pass

class BlogOut(BlogBase):
    id: int = Field(ge=1)

class BlogUpdate(BlogBase):
    content: str = Field(max_length=200)
    title: str = Field(max_length=200)
    
# class BlogComment(BlogBase):
#     comment: str = Field(max_length=200)