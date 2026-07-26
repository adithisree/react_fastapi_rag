from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag_chain import ask_question

app = FastAPI(title="Document QA API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    answer: str
    


@app.get("/")
def home():
    return {"message": "Document QA API is running."}


@app.post("/api/ask", response_model=QuestionResponse)
def ask(request: QuestionRequest):
    answer=ask_question(request.question)

    return QuestionResponse(
        answer=answer,
       
       
    )