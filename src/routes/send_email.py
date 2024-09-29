from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = FastAPI()

# Configuration du serveur SMTP (utilisez vos informations)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "votre.email@gmail.com"  # Remplacez par votre adresse email
SENDER_PASSWORD = "votre_mot_de_passe"  # Remplacez par votre mot de passe ou mot de passe d'application


@app.post("/send_email")
async def send_email(email: str = Form(...)):
    # Envoi d'un email d'acceptation au candidat
    send_acceptance_email(email)
    return RedirectResponse("/results", status_code=303)


def send_acceptance_email(email: str):
    try:
        # Créer un message MIME
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = email
        message["Subject"] = "Félicitations! Vous êtes accepté(e)"

        # Corps de l'email
        body = """
        Cher candidat(e),

        Félicitations ! Nous sommes ravis de vous informer que vous avez été sélectionné(e) pour la prochaine étape de notre processus de recrutement.

        Nous vous remercions pour l'intérêt que vous portez à notre entreprise et pour le temps que vous avez consacré à notre processus de recrutement.

        Cordialement,
        L'équipe de recrutement
        """
        message.attach(MIMEText(body, "plain"))

        # Connexion au serveur SMTP et envoi de l'email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Activer TLS pour sécuriser la connexion
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, email, message.as_string())
        server.quit()

        print(f"Acceptance email sent to {email}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")

