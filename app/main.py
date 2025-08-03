from fastapi import FastAPI
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import drug 
from app.api.v1.endpoints import doctor ,  ocr
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import gemini  # Geçici olarak devre dışı

app = FastAPI()

app.include_router(auth.router)
app.include_router(drug.router) 
app.include_router(doctor.router)
app.include_router(ocr.router)
app.include_router(gemini.router, prefix="/gemini", tags=["gemini"])  # Geçici olarak devre dışı

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Veya ["*"] geliştirme için
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API is running! Visit /docs for Swagger UI"}
