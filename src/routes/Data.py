import os
from fastapi import APIRouter, Request, Form, File, UploadFile, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List

from helpers.config import get_settings, Settings
from controllers import DataController, BaseController
#import aiofiles
from models import ResponseSignal
import logging

# Create a new APIRouter instance
post_router = APIRouter()

# Set up the static files directory
templates_dir = os.path.abspath("templates")

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
    app_settings: Settings = Depends(get_settings)
):
    data_controller = DataController()
    
    # Assurez-vous que le répertoire existe
    upload_directory = "assets/files"
    os.makedirs(upload_directory, exist_ok=True)
    
    file_ids = []  # Liste pour stocker les IDs des fichiers traités

    for file in files:
        is_valid, result_signal = data_controller.validate_uploaded_file(file=file)
        is_valid_post, result_signal_post = data_controller.validate_uploaded_post(post=user_input)

        if not is_valid or not is_valid_post:
            return templates.TemplateResponse(
                "index.html",
                status_code=status.HTTP_400_BAD_REQUEST,
                context={
                    "request": request,  # Passez l'objet request au contexte
                    "signal": result_signal,
                    "signal_post":result_signal_post,
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
        "index.html",
        context={
            "request": request,  # Passez l'objet request au contexte
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "signal_post":ResponseSignal.POST_UPLOAD_SUCCESS.value,
            "file_ids": file_ids
        }
    )