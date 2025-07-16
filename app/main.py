from fastapi import FastAPI
from app.api.v1.endpoints import auth

app = FastAPI()

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "API is running! Visit /docs for Swagger UI"}
