
from fastapi import FastAPI
import models
import database
from routers import blog, users, authentication
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(blog.router)
app.include_router(users.router)
app.include_router(authentication.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")