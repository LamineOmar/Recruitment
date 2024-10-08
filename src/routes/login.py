from fastapi import FastAPI, APIRouter, HTTPException,Form, Depends
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from src.database.database import SessionLocal, engine
from src.database.models import CandidatInfo,Test,CandidatAnswer
from src.database.schema import CandidatAnswer
from sqlalchemy.orm import Session
import ast
import logging
from sqlalchemy import update
from typing import Dict
from src.database import crud, models


# Dépendance pour la session de la base de données
def get_db():
    db = SessionLocal()
    print("db done")
    try:
        yield db
        print("db done done")

    finally:
        db.close()
        print("db closed")

login_app = APIRouter()

logging.basicConfig(level=logging.INFO)  

# Configuration du moteur de templates
templates = Jinja2Templates(directory="src/templates")  # Assurez-vous que ce répertoire contient votre fichier login.html
# Route pour la page login
@login_app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    try:
        # Vérifiez si le fichier existe et est lisible
        print("Accès à la page de login")
        return templates.TemplateResponse("login.html", {"request": request})
    except Exception as e:
        # Capturez toute erreur et affichez-la dans les logs
        print(f"Erreur lors du rendu de la page login : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors du chargement de la page de login.")


@login_app.post("/login")
async def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    # Recherche du candidat dans la base de données par email
    candidat = db.query(CandidatInfo).filter(CandidatInfo.email == email).first()
    
    # Si le candidat n'existe pas ou que le mot de passe ne correspond pas
    if not candidat or candidat.test_password != password:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    return RedirectResponse(url=f"/questions/{candidat.id_candidatInfo}", status_code=303)

def extract_options(option_string):
    # Convertir la chaîne en liste Python
    try:
        # On utilise ast.literal_eval pour éviter les risques d'évaluation de code non sécurisé
        options = ast.literal_eval(option_string)
        return options
    except (ValueError, SyntaxError) as e:
        print(f"Error parsing options: {e}")
        return []


@login_app.get("/questions/{candidat_id}", response_class=HTMLResponse)
async def display_questions(candidat_id: int, request: Request, db: Session = Depends(get_db)):
    # Récupérer les informations du candidat
    candidat = db.query(CandidatInfo).filter(CandidatInfo.id_candidatInfo == candidat_id).first()

    if not candidat:
        return templates.TemplateResponse("error.html", {"request": request, "error": "Candidat non trouvé."})
    
    # Récupérer les questions liées à la job_description du candidat
    tests = db.query(Test).filter(Test.job_description_id == candidat.job_description_id).all()

    # Extraire les options pour chaque test
    for test in tests:
        test.options = extract_options(test.option)

    # Afficher les questions sous forme de formulaire
    return templates.TemplateResponse("questions.html", {"request": request, "tests": tests, "candidat_id": candidat_id})



@login_app.post("/submit_answers", response_class=HTMLResponse)
async def submit_answers(
    request: Request,
    db: Session = Depends(get_db),
    candidat_id: int = Form(...),
):
    # Récupérer le candidat
    candidat = db.query(models.CandidatInfo).filter(models.CandidatInfo.id_candidatInfo == candidat_id).first()

    if not candidat:
        logging.error("Candidat non trouvé.")
        return templates.TemplateResponse("error.html", {"request": request, "error": "Candidat non trouvé."})
    
    # Récupérer les données du formulaire
    form_data = await request.form()
    
    # Enregistrer les réponses du candidat
    Score = 0
    for key, value in form_data.items():
        if key.startswith('answer_'):
            question_id = key.split('answer_')[1]
            answer_reel = db.query(models.Test.answer).filter(models.Test.id_test == question_id).first()

            # Check if answer_reel is not None and compare with the value
            if answer_reel and str(answer_reel.answer) == value:
                Score += 1

    # Update the candidate's score
    stmt = update(models.CandidatInfo).where(models.CandidatInfo.id_candidatInfo == candidat_id).values(score=Score)
    db.execute(stmt)
    db.commit()
    
    logging.info("Réponses enregistrées avec succès.")
    return templates.TemplateResponse("validate.html", {"request": request})