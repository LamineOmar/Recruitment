import os
from fastapi import APIRouter, Request, Form, File, UploadFile, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List

from src.helpers.config import get_settings, Settings
from src.controllers import DataController
from sqlalchemy.orm import Session
from src.database.schema import JobDescription, Test, CandidatInfo, CandidatAnswer
from src.database.database import SessionLocal, engine
from src.database import crud, models
#import aiofiles
from src.models import ResponseSignal


models.Base.metadata.create_all(bind=engine)

# Create a new APIRouter instance
post_router = APIRouter()

# Dependency pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Set up the static files directory
templates_dir = os.path.abspath("src/templates")

# Set up Jinja2 templates directory
templates = Jinja2Templates(directory=templates_dir)

# Define a GET route to serve the form
@post_router.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@post_router.post("/submit", response_class=JSONResponse)
async def submit_form(
    request: Request,
    user_input: str = Form(...),
    files: List[UploadFile] = File(...),
    app_settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db)
):
    data_controller = DataController()
    
    job_description_obj = JobDescription(job_description=user_input)
    crud.crud.save_job_description(db, job_description_obj)
    # result = crud.crud.get_job_description_info(db)
    # result = [job.job_description for job in result]
    # Assurez-vous que le répertoire existe
    upload_directory = "assets/files"
    os.makedirs(upload_directory, exist_ok=True)
    
    file_ids = []  # Liste pour stocker les IDs des fichiers traités

    for file in files:
        is_valid, result_signal = data_controller.validate_uploaded_file(file=file)
        is_valid_post, result_signal_post = data_controller.validate_uploaded_post(post=user_input)

        if not is_valid or not is_valid_post:
            dont_show_button=1
            if not is_valid:
                message = result_signal
            else:
                message = result_signal_post
            
            return templates.TemplateResponse(
                "index2.html",
                status_code=status.HTTP_400_BAD_REQUEST,
                context={
                    "request": request,  # Passez l'objet request au contexte
                    "signal": message,
                    "dont_show_button":dont_show_button,
                    "file_ids": file_ids
                }
            )
        # Générer le chemin du fichier et l'ID unique
        file_path, file_id = data_controller.generate_unique_filepath(orig_file_name=file.filename)

        # Enregistrer le fichier
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        file_post = os.path.join(
            data_controller.files_dir,
            "post_description.txt"
         )
        with open(file_post, 'w', encoding='utf-8') as fichier:
            # Écrire le texte dans le fichier
            fichier.write(user_input)
            
        # Ajouter l'ID du fichier à la liste
        file_ids.append(file_id)

    return templates.TemplateResponse(
        "index2.html",
        context={
            "request": request,  # Passez l'objet request au contexte
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "signal_post":ResponseSignal.POST_UPLOAD_SUCCESS.value,
            "file_ids": file_id,
        }
    )