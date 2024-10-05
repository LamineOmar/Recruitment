from fastapi import APIRouter, Depends, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from src.database import crud, models
from src.database.database import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

# Create a new APIRouter instance
dash_app = APIRouter()

# Dependency pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory="src/templates")

@dash_app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    jobId:int= Query(default=0),
    db: Session = Depends(get_db)
    ):
    job_descs = crud.crud.get_job_description_info(db)
    num_job_desc = len(job_descs)
    
    candidatInfo = crud.crud.get_candidat_info_with_job_description_of_job_x(db,jobId)
    num_candidat=len(candidatInfo)
    
    Table_title="Candidates for All Jobs"
    element="ALL"
    if jobId != 0:
        element = jobId
        Table_title= f'Candidates for the job "{db.query(models.JobDescription.job_name).filter(models.JobDescription.job_description_id == jobId).scalar()}"'
    
    return templates.TemplateResponse("dashboard.html", 
                                      {
                                        "request": request,
                                        "num_job_desc": num_job_desc,
                                        "job_descs": job_descs,
                                        "num_candidat":num_candidat,
                                        "element":element,
                                        "Table_title":Table_title,
                                        "candidatInfo": candidatInfo
                                        })
