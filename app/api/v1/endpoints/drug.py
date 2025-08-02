from fastapi import APIRouter, Depends, HTTPException
from app.models.drug import Drug
from app.services.drug_service import (
    add_drug_to_user,
    get_user_drug_list,
    get_specific_drug,
    update_drug_info,
    delete_drug_info,
    record_drug_usage,
    get_drug_usage_history,
    get_all_drug_usage
)
from app.models.drug import DrugUsage
from app.services.auth_service import get_current_user
from typing import List

router = APIRouter(prefix="/drugs", tags=["Drugs"])

@router.post("/", response_model=dict)
def add_drug(
    drug: Drug,
    current_user=Depends(get_current_user)
):
    """Add a drug to user's drug list"""
    return add_drug_to_user(current_user["user_id"], drug)

@router.get("/", response_model=List[dict])
def get_drugs(current_user=Depends(get_current_user)):
    """Get all drugs for the current user"""
    return get_user_drug_list(current_user["user_id"])

@router.get("/{drug_id}", response_model=dict)
def get_drug(drug_id: str, current_user=Depends(get_current_user)):
    """Get a specific drug by ID"""
    return get_specific_drug(current_user["user_id"], drug_id)

@router.put("/{drug_id}", response_model=dict)
def update_drug(
    drug_id: str,
    drug: Drug,
    current_user=Depends(get_current_user)
):
    """Update a drug's information"""
    drug_dict = drug.dict()
    return update_drug_info(current_user["user_id"], drug_id, drug_dict)

@router.delete("/{drug_id}")
def delete_drug(drug_id: str, current_user=Depends(get_current_user)):
    """Delete a drug from user's list"""
    return delete_drug_info(current_user["user_id"], drug_id)

# Drug usage tracking endpoints
@router.post("/{drug_id}/usage", response_model=dict)
def record_drug_usage_endpoint(
    drug_id: str,
    usage: DrugUsage,
    current_user=Depends(get_current_user)
):
    """Record a drug usage"""
    usage_data = usage.dict()
    return record_drug_usage(current_user["user_id"], drug_id, usage_data)

@router.get("/{drug_id}/usage", response_model=List[dict])
def get_drug_usage_history_endpoint(drug_id: str, current_user=Depends(get_current_user)):
    """Get usage history for a specific drug"""
    return get_drug_usage_history(current_user["user_id"], drug_id)

@router.get("/usage/all", response_model=List[dict])
def get_all_drug_usage_endpoint(current_user=Depends(get_current_user)):
    """Get all drug usage for the current user"""
    return get_all_drug_usage(current_user["user_id"])



