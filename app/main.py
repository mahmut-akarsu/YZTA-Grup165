from fastapi import FastAPI
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import drug 
from app.api.v1.endpoints import doctor

app = FastAPI()

app.include_router(auth.router)
app.include_router(drug.router) 
app.include_router(doctor.router)

@app.get("/")
def read_root():
    return {"message": "API is running! Visit /docs for Swagger UI"}
