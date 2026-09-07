from fastapi import FastAPI
from pydantic import BaseModel
from database import SessionLocal
from models import Ticket as TicketModel
from sqlalchemy import select

app = FastAPI()

class Ticket(BaseModel):
    title: str
    description: str

@app.get("/")
def home():
    return {"message": "ResolveAI API is running"}

@app.post("/tickets")
def create_ticket(ticket: Ticket):
    db = SessionLocal()

    try:
        new_ticket = TicketModel(title = ticket.title, description = ticket.description)
        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)

        return new_ticket
    finally:
        db.close()


@app.get("/tickets")
def get_tickets():
    db = SessionLocal()

    try:
        result = db.execute(select(TicketModel))
        tickets = result.scalars().all()

        return tickets
    finally:
        db.close()
