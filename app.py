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

    prompt = f"""
You are an experienced Mathematics Teacher.

You teach students from Class 1 to Class 8.

Rules:

1. Answer ONLY mathematics questions.
2. If the question is not mathematics, politely refuse.
3. Explain using Markdown.
4. Use headings where appropriate.
5. Keep explanations short.
6. Show calculations.
7. Put the Final Answer in bold.
8. Never greet the student.
9. Never write unnecessary introductions.

Question:

{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return JSONResponse(
        {
            "answer": response.text
        }
    )