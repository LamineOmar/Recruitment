
from fastapi import FastAPI
from routes import Data
from fastapi.staticfiles import StaticFiles

app = FastAPI()


# Serve static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(Data.post_router)

