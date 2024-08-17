
from fastapi import FastAPI
from routes import post_description

app = FastAPI()

app.include_router(post_description.post_router)

