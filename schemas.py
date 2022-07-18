from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    description: str


class ShowBlog(Blog):
    title: str
    description: str

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUsers(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True



# class Login(BaseModel):
#     email: str
#     password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None