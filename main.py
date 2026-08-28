from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "ResolveAI API is running"}