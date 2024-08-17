import os
from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

# Create a new APIRouter instance
post_router = APIRouter()

# Set up the static files directory
static_dir = os.path.abspath("static")
templates_dir = os.path.abspath("templates")

# Serve static files (CSS, JS, etc.)
post_router.mount("/static", StaticFiles(directory=static_dir), name="static")

# Set up Jinja2 templates directory
templates = Jinja2Templates(directory=templates_dir)

# Define a GET route to serve the form
@post_router.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
