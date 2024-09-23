from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.post("/send_email")
async def send_email(email: str = Form(...)):
    # Logic to send an email to the candidate
    send_acceptance_email(email)  # This function will handle email sending
    return RedirectResponse("/results", status_code=303)

def send_acceptance_email(email: str):
    # Placeholder function for sending email (use an email service or SMTP)
    print(f"Acceptance email sent to {email}")
