from pydantic import BaseModel, Field

class UserBase(BaseModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)


class UserCreate(UserBase):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=100)

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
    
class Token(BaseModel):
    access_token: str
    token_type: str