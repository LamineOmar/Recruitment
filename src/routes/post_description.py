import os
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from controllers import Clean

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


@post_router.post("/submit", response_class=HTMLResponse)
async def submit_form(request: Request, user_input: str = Form(...)):
    clean = Clean()
    user_input = clean.clean_text(user_input)
    return templates.TemplateResponse("index.html", {"request": request, "user_input": user_input})