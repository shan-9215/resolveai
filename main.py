from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import SessionLocal
from models import Ticket as TicketModel
from sqlalchemy import select
from typing import Literal

app = FastAPI()

class Ticket(BaseModel):
    title: str
    description: str

class TicketUpdate(BaseModel):
    status: Literal["open", "in_progress", "closed"]

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

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    db = SessionLocal()

    try:
        ticket = db.get(TicketModel, ticket_id)
        if ticket is None:
            raise HTTPException(status_code=404, detail= "Ticket not found")
        return ticket
    finally:
        db.close()

@app.patch("/tickets/{ticket_id}")
def update_ticket(ticket_id: int, ticket_update: TicketUpdate):
    db = SessionLocal()

    try:
        ticket = db.get(TicketModel, ticket_id)

        if ticket is None:
            raise HTTPException(status_code=404, detail= "Ticket not found")
        ticket.status = ticket_update.status

        db.commit()
        db.refresh(ticket)

        return ticket
    finally:
        db.close()