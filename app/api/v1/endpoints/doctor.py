
from fastapi import APIRouter, Depends
from api.dependencies.auth import require_role

router = APIRouter(prefix="/doctor", tags=["Doctor"])

@router.get("/patients")
def list_patients(current_user=Depends(require_role("doctor"))):
    return {"message": f"Welcome Dr. {current_user['user_id']}, here’s the patient list."}
