from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    commentary: str = Field(max_length=200)
    user_id: int
    blog_id: int


class CommentCreate(CommentBase):
    pass


class CommentOut(CommentBase):
    id: int = Field(ge=1)


class CommentUpdate(CommentBase):
    commentary: str = Field(max_length=200)
    user_id: int
    blog_id: int
