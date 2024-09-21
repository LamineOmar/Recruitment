import google.generativeai as genai
import re, os
import json
from src.helpers.config import get_settings
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from src.controllers import DataController

from sqlalchemy.orm import Session
from src.database.schema import JobDescription, Test, CandidatInfo, CandidatAnswer
from src.database.database import SessionLocal, engine
from src.database import crud, models


models.Base.metadata.create_all(bind=engine)

# Dependency pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


question_router = APIRouter()

# Set up Jinja2 templates directory
templates_dir = os.path.abspath("src/templates")
templates = Jinja2Templates(directory=templates_dir)

# Default job description
job_description = "data scientist"




@question_router.post("/create_questions", response_class=HTMLResponse)
async def generate_q(
    request: Request,
    db: Session = Depends(get_db)                 
):
    # Instantiate DataController
    data_controller = DataController()
    job_description, job_description_id =crud.crud.get_last_job_description(db)
    
    # Configure Google Generative AI with the API key from settings
    genai.configure(api_key=get_settings().GEMINI_API_KEY)

    # Initialize the generative model
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    # Get the prompt for generation and format it with the job description
    prompt = data_controller.get_prompt().format(job_description=job_description)

    # Generate content using the model
    response = model.generate_content(prompt)

    if response and response.parts:
        generated_json = "".join([part.text for part in response.parts])

        # Remove the markdown block markers (```json and ```).
        cleaned_json = re.sub(r'```json|```', '', generated_json)
        try:
            # Parse the cleaned JSON into a dictionary
            questions_data = json.loads(cleaned_json)
            
            # Iterate over the generated questions and save them in the database
            for question_data in questions_data:
                # Extract question, options, and answer
                question_text = question_data["question"]
                options = question_data["options"]
                answer = question_data["answer"]

                # Create Test schema object
                test_info = Test(
                    question=question_text,
                    option=str(options),
                    answer=answer,
                    job_description_id=job_description_id
                )

                # Save the question in the database
                crud.crud.save_Test_info(db, test_info)

            # Render the template with the generated JSON
            return templates.TemplateResponse("validate.html", {"request": request})

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return templates.TemplateResponse("error.html", {"request": request, "error": "Failed to parse the generated questions."})

    else:
        print("No response or empty parts from the model")
        return templates.TemplateResponse("error.html", {"request": request, "error": "No response from the model."})
    