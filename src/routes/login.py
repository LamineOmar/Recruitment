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
    **answers  # Collect all answer submissions
):
    logging.info("Début de la soumission des réponses.")
    logging.info(f"ID du candidat reçu : {candidat_id}")
    logging.info(f"Réponses reçues : {answers}")

    # Récupérer le candidat
    candidat = db.query(CandidatInfo).filter(CandidatInfo.id_candidatInfo == candidat_id).first()

    if not candidat:
        logging.error("Candidat non trouvé.")
        return templates.TemplateResponse("error.html", {"request": request, "error": "Candidat non trouvé."})
    
    # Enregistrer les réponses du candidat
    for key, value in answers.items():
        if key.startswith("answer_"):
            id_test = int(key.split("_")[1])  # Extraire l'id_test à partir du nom du champ
            logging.info(f"Enregistrement de la réponse : {value} pour le test ID : {id_test}")

            candidat_answer = CandidatAnswer(
                id_candidat=candidat.id_candidatInfo,  # Assuming this is the correct field for candidate ID
                id_test=id_test,
                candidat_answer=value
            )
            db.add(candidat_answer)
    
    try:
        db.commit()
        logging.info("Réponses enregistrées avec succès.")
    except Exception as e:
        logging.error(f"Erreur lors de l'enregistrement des réponses : {str(e)}")
        db.rollback()
        return templates.TemplateResponse("error.html", {"request": request, "error": "Erreur lors de l'enregistrement des réponses."})

    return templates.TemplateResponse("validate.html", {"request": request})