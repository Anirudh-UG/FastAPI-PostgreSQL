from fastapi import FastAPI
from app import models
from .database import engine
from .routers import post, users, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
