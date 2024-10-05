
from fastapi import FastAPI
from src.routes import Data, Questions_gen, show_databases, Dashboard
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(Data.post_router)
app.include_router(Questions_gen.question_router)
app.include_router(show_databases.app_router)
app.include_router(Dashboard.dash_app)

