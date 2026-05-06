from pydantic import BaseModel, Field


class BlogBase(BaseModel):
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
