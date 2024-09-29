from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from database.models import CandidatInfo

app = FastAPI()

# Configuration du serveur SMTP (utilisez vos informations)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "votre.email@gmail.com"  # Remplacez par votre adresse email
SENDER_PASSWORD = "votre_mot_de_passe"  # Remplacez par votre mot de passe ou mot de passe d'application


@app.post("/send_email")
async def send_email(email: str = Form(...)):
    # Récupérer les informations du candidat depuis la "base de données"
    candidat_info = CandidatInfo.get(email)
    
    if candidat_info:
        # Envoyer un e-mail d'acceptation avec le test_password
        send_acceptance_email(candidat_info.email, candidat_info.test_password)
        return RedirectResponse("/results", status_code=303)
    else:
        return {"error": "Candidat non trouvé"}

# Fonction pour envoyer l'e-mail
def send_acceptance_email(email: str, test_password: str):
    # Contenu de l'e-mail
    message = f"""
    Bonjour,

    Nous sommes heureux de vous informer que votre candidature a été acceptée.
    
    Veuillez utiliser le mot de passe suivant pour passer le test : {test_password}

    Cordialement,
    L'équipe de recrutement
    """

    # Configuration SMTP (remplacer par vos informations)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "votre.email@gmail.com"  # Remplacer par votre e-mail
    smtp_password = "votre_mot_de_passe"  # Remplacer par votre mot de passe

    # Création du message
    msg = MIMEText(message)
    msg['Subject'] = "Candidature acceptée"
    msg['From'] = smtp_user
    msg['To'] = email

    # Connexion au serveur SMTP et envoi de l'e-mail
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, email, msg.as_string())

    print(f"Acceptance email sent to {email}")