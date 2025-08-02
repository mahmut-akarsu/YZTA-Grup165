
from fastapi import APIRouter, Depends, HTTPException
from app.services.doctor_service import (
    get_patient_drugs,
    get_patient_info,
    get_all_patients,
    check_doctor_permission,
    get_patient_drug_usage,
    get_patient_all_drug_usage
)
from app.services.auth_service import get_current_user
from typing import List

router = APIRouter(prefix="/doctor", tags=["Doctor"])

@router.get("/patients", response_model=List[dict])
def list_patients(current_user=Depends(get_current_user)):
    """Get all patients (for doctors only)"""
    check_doctor_permission(current_user)
    return get_all_patients()

@router.get("/patients/{patient_id}", response_model=dict)
def get_patient_information(patient_id: str, current_user=Depends(get_current_user)):
    """Get specific patient information (for doctors only)"""
    check_doctor_permission(current_user)
    return get_patient_info(patient_id)

@router.get("/patients/{patient_id}/drugs", response_model=dict)
def get_patient_drugs_endpoint(patient_id: str, current_user=Depends(get_current_user)):
    """Get all drugs for a specific patient (for doctors only)"""
    check_doctor_permission(current_user)
    return get_patient_drugs(patient_id)

@router.get("/patients/{patient_id}/drugs/{drug_id}/usage", response_model=List[dict])
def get_patient_drug_usage_endpoint(patient_id: str, drug_id: str, current_user=Depends(get_current_user)):
    """Get drug usage history for a specific patient's drug (for doctors only)"""
    check_doctor_permission(current_user)
    return get_patient_drug_usage(patient_id, drug_id)

@router.get("/patients/{patient_id}/drugs/usage/all", response_model=List[dict])
def get_patient_all_drug_usage_endpoint(patient_id: str, current_user=Depends(get_current_user)):
    """Get all drug usage for a specific patient (for doctors only)"""
    check_doctor_permission(current_user)
    return get_patient_all_drug_usage(patient_id)


