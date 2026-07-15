from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="Math Tutor AI")

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )

@app.get("/solve")
def solve(question: str):

    # Read Version 2 prompt
    with open("prompts/advanced_math_tutor.md", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # Replace placeholder with user's question
    prompt = system_prompt.replace("{question}", question)

    # Call Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return JSONResponse(
        {
            "answer": response.text
        }
    )