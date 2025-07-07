from fastapi import APIRouter, HTTPException, Response, Depends, status
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
import logging
from ..database import get_db
from typing import List, Optional

logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[schemas.postResponse]
)
def get_posts(
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    logging.info("Data fetched")
    posts = (
        db.query(models.Post)
        .filter(models.Post.owner_id == current_user.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )  # use %20 to use spaces in URLs, particularly useful in search operations
    return posts


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.postResponse,
)
def create_posts(
    payload: schemas.postCreate,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user),
):
    new_post = models.Post(owner_id=current_user.id, **payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    # cursor.execute(
    #     "INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *",
    #     (payload.title, payload.content, payload.published),
    # )
    # response = cursor.fetchone()
    # conn.commit()


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.postResponse
)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cursor.fetchone()
    if not post:
        logging.warning("post with id not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    if post.owner_id != current_user.id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Access"
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user),
):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post: models.Post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    if post.owner_id != current_user.id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Cannot perform said action"
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.postResponse
)
def update_post(
    id: int,
    payload: schemas.postCreate,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()

    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
    if current_user.id != existing_post.owner_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have the authority to modify this post",
        )

    post_query.update(
        {
            getattr(models.Post, key): value
            for key, value in payload.model_dump().items()
        },
        synchronize_session=False,
    )

    db.commit()

    return post_query.first()
