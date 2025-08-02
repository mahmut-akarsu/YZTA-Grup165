from fastapi import APIRouter
from app.services.gemini_service import get_drug_info

router = APIRouter()

@router.post("/drug-info")
def get_drug_information(drug_name: str):
    return {"drug_info": get_drug_info(drug_name)}
