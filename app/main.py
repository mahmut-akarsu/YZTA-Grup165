from fastapi import FastAPI
from app.api.v1.endpoints import auth, drug, doctor, ocr, gemini

app = FastAPI()

app.include_router(auth.router)
app.include_router(drug.router)
app.include_router(doctor.router)
app.include_router(ocr.router)
app.include_router(gemini.router, prefix="/gemini", tags=["gemini"])

@app.get("/")
def read_root():
    return {"message": "API is running! Visit /docs for Swagger UI"}
