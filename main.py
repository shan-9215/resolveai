from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Ticket(BaseModel):
    title: str
    description: str

@app.get("/")
def home():
    return {"message": "ResolveAI API is running"}

@app.post("/tickets")
def create_ticket(ticket: Ticket):
    return ticket