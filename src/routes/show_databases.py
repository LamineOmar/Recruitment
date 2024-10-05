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

@app_router.get("/show_candinfo")
async def handle_form(
    db: Session = Depends(get_db)
):
    result = crud.crud.get_candinfo_info(db)
    return {"Received tests": result}

@app_router.get("/table-columns/{table_name}")
async def get_table_columns(table_name: str, db: Session = Depends(get_db)):
    try:
        # Step 2: Reflect the table schema
        models.Base.metadata.reflect(bind=engine, only=[table_name])
        table = models.Base.metadata.tables.get(table_name)

        if table is None:
            return {"error": "Table not found"}

        # Extract column names
        columns = [column.name for column in table.columns]
        return {"columns": columns}

    except Exception as e:
        return {"error": str(e)}