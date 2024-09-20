from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from src.database.database import SessionLocal, engine
from src.database.schema import JobDescription, Test, CandidatInfo, CandidatAnswer
from src.database import crud, models

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

models.Base.metadata.create_all(bind=engine)

app_router = APIRouter()

# Dependency pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app_router.get("/show_job_descriptions")
async def handle_form(
    db: Session = Depends(get_db)
):
    result = crud.crud.get_job_description_info(db)
    return {"Received jobs": result}

@app_router.get("/show_tests")
async def handle_form(
    db: Session = Depends(get_db)
):
    result = crud.crud.get_Tests_info(db)
    return {"Received tests": result}