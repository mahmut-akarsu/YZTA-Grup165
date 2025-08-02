from app.repositories.firebase_repo import (
    get_patient_drugs_for_doctor,
    get_patient_info_for_doctor,
    get_all_patients_for_doctor,
    get_drug_usage_history as get_drug_usage_history_repo,
    get_all_drug_usage_for_user
)
from fastapi import HTTPException, status
from typing import List, Optional

def get_patient_drugs(patient_id: str) -> List[dict]:
    """Get all drugs for a specific patient (for doctors)"""
    try:
        # First check if patient exists
        patient_info = get_patient_info_for_doctor(patient_id)
        if not patient_info:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Check if the user is actually a patient
        if patient_info.get("role_id", "").lower() != "patient":
            raise HTTPException(status_code=400, detail="User is not a patient")
        
        drugs = get_patient_drugs_for_doctor(patient_id)
        return {
            "patient_info": {
                "user_id": patient_info["user_id"],
                "name": patient_info["name"],
                "surname": patient_info["surname"],
                "email": patient_info["email"]
            },
            "drugs": drugs
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching patient drugs: {str(e)}")

def get_patient_info(patient_id: str) -> dict:
    """Get patient information (for doctors)"""
    try:
        patient_info = get_patient_info_for_doctor(patient_id)
        if not patient_info:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Check if the user is actually a patient
        if patient_info.get("role_id", "").lower() != "patient":
            raise HTTPException(status_code=400, detail="User is not a patient")
        
        return {
            "user_id": patient_info["user_id"],
            "name": patient_info["name"],
            "surname": patient_info["surname"],
            "email": patient_info["email"],
            "role_id": patient_info["role_id"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching patient info: {str(e)}")

def get_all_patients() -> List[dict]:
    """Get all patients (for doctors)"""
    try:
        patients = get_all_patients_for_doctor()
        return patients
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching patients: {str(e)}")

def check_doctor_permission(current_user: dict) -> bool:
    """Check if the current user is a doctor"""
    if current_user.get("role_id", "").lower() != "doctor":
        raise HTTPException(
            status_code=403, 
            detail="Access denied. Only doctors can access this endpoint."
        )
    return True

def get_patient_drug_usage(patient_id: str, drug_id: str) -> List[dict]:
    """Get drug usage history for a specific patient's drug (for doctors)"""
    try:
        # Check if patient exists
        patient_info = get_patient_info_for_doctor(patient_id)
        if not patient_info:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Check if the user is actually a patient
        if patient_info.get("role_id", "").lower() != "patient":
            raise HTTPException(status_code=400, detail="User is not a patient")
        
        usage_history = get_drug_usage_history_repo(patient_id, drug_id)
        return usage_history
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching patient drug usage: {str(e)}")

def get_patient_all_drug_usage(patient_id: str) -> List[dict]:
    """Get all drug usage for a specific patient (for doctors)"""
    try:
        # Check if patient exists
        patient_info = get_patient_info_for_doctor(patient_id)
        if not patient_info:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Check if the user is actually a patient
        if patient_info.get("role_id", "").lower() != "patient":
            raise HTTPException(status_code=400, detail="User is not a patient")
        
        all_usage = get_all_drug_usage_for_user(patient_id)
        return all_usage
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching patient all drug usage: {str(e)}") 