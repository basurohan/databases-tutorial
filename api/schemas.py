from pydantic import BaseModel


class Article(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class ArticleDTO(BaseModel):
    id: int
    title: str
    description: str