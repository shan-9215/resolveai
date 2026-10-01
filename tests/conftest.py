import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import get_db
from main import app
from models import Ticket as TicketModel


load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL or not TEST_DATABASE_URL.endswith("/resolveai_test"):
    raise RuntimeError("Tests must use the resolveai_test database")

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def clean_database():
    db = TestingSessionLocal()

    try:
        db.query(TicketModel).delete()
        db.commit()
    finally:
        db.close()


client = TestClient(app)