from fastapi import FastAPI, Depends, HTTPException
from typing import Optional, List

from sqlalchemy.orm import Session
from starlette import status

from api import models
from api.database import SessionLocal
from api import schemas

app = FastAPI()

data = [
    {'title': 'First title'},
    {'title': 'Second title'},
    {'title': 'Third title'}
]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/articles', response_model=List[schemas.Article])
async def get_articles(skip: Optional[int] = 0, limit: Optional[int] = 20, db: Session = Depends(get_db)):
    all_articles = db.query(models.Article).all()
    return all_articles[skip:skip+limit]


@app.get('/article/{article_id}', status_code=status.HTTP_200_OK, response_model=schemas.Article)
async def get_article(article_id: int, db: Session = Depends(get_db)):
    # my_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    my_article = db.query(models.Article).get(article_id)
    if my_article:
        return my_article
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The article does not exists')


@app.post('/article', status_code=status.HTTP_201_CREATED, response_model=schemas.ArticleDTO)
async def add_article(article: schemas.Article, db: Session = Depends(get_db)):
    new_article = models.Article(title=article.title, description=article.description)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


@app.put('/article/{article_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_article(article_id: int, article: schemas.Article, db: Session = Depends(get_db)):
    existing_article = db.query(models.Article).filter(models.Article.id == article_id)
    if not existing_article.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The article does not exists')
    existing_article.update({
        'title': article.title,
        'description': article.description
    })
    db.commit()
    return {'message': 'Article updated'}


@app.delete('/article/{article_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deleted_article(article_id: int, db: Session = Depends(get_db)):
    existing_article = db.query(models.Article).filter(models.Article.id == article_id)
    if not existing_article.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The article does not exists')
    existing_article.delete(synchronize_session=False)
    db.commit()
    return {'message': 'Article deleted'}
