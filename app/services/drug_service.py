from app.models.drug import Drug
from app.repositories.firebase_repo import (
    add_drug_for_user,
    get_user_drugs,
    get_user_drug_by_id,
    update_user_drug,
    delete_user_drug,
    record_drug_usage as record_drug_usage_repo,
    get_drug_usage_history as get_drug_usage_history_repo,
    get_all_drug_usage_for_user
)
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime

def add_drug_to_user(user_id: str, drug_data: Drug) -> dict:
    """Add a drug to user's drug list"""
    try:
        drug_dict = drug_data.dict()
        drug_id = add_drug_for_user(user_id, drug_dict)
        return {"drug_id": drug_id, "message": "Drug added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding drug: {str(e)}")

def get_user_drug_list(user_id: str) -> List[dict]:
    """Get all drugs for a user"""
    try:
        drugs = get_user_drugs(user_id)
        return drugs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching drugs: {str(e)}")

def get_specific_drug(user_id: str, drug_id: str) -> dict:
    """Get a specific drug for a user"""
    try:
        drug = get_user_drug_by_id(user_id, drug_id)
        if not drug:
            raise HTTPException(status_code=404, detail="Drug not found")
        return drug
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching drug: {str(e)}")

def update_drug_info(user_id: str, drug_id: str, drug_data: dict) -> dict:
    """Update a drug's information"""
    try:
        # Check if drug exists
        existing_drug = get_user_drug_by_id(user_id, drug_id)
        if not existing_drug:
            raise HTTPException(status_code=404, detail="Drug not found")
        
        # Update only provided fields
        update_data = {k: v for k, v in drug_data.items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        success = update_user_drug(user_id, drug_id, update_data)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update drug")
        
        # Get updated drug
        updated_drug = get_user_drug_by_id(user_id, drug_id)
        return updated_drug
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating drug: {str(e)}")

def delete_drug_info(user_id: str, drug_id: str) -> dict:
    """Delete a drug from user's list"""
    try:
        # Check if drug exists
        existing_drug = get_user_drug_by_id(user_id, drug_id)
        if not existing_drug:
            raise HTTPException(status_code=404, detail="Drug not found")
        
        success = delete_user_drug(user_id, drug_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete drug")
        
        return {"message": "Drug deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting drug: {str(e)}")

# Drug usage tracking functions
def record_drug_usage(user_id: str, drug_id: str, usage_data: dict) -> dict:
    """Record a drug usage for a user"""
    try:
        # Check if drug exists
        existing_drug = get_user_drug_by_id(user_id, drug_id)
        if not existing_drug:
            raise HTTPException(status_code=404, detail="Drug not found")
        
        # Set usage time if not provided
        if not usage_data.get("usage_time"):
            usage_data["usage_time"] = datetime.now()
        
        # Record usage
        usage_id = record_drug_usage_repo(user_id, drug_id, usage_data)
        
        return {
            "usage_id": usage_id,
            "drug_id": drug_id,
            "drug_name": existing_drug.get("name", "Unknown"),
            "message": "Drug usage recorded successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recording drug usage: {str(e)}")

def get_drug_usage_history(user_id: str, drug_id: str) -> List[dict]:
    """Get usage history for a specific drug"""
    try:
        # Check if drug exists
        existing_drug = get_user_drug_by_id(user_id, drug_id)
        if not existing_drug:
            raise HTTPException(status_code=404, detail="Drug not found")
        
        usage_history = get_drug_usage_history_repo(user_id, drug_id)
        return usage_history
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching drug usage history: {str(e)}")

def get_all_drug_usage(user_id: str) -> List[dict]:
    """Get all drug usage for a user"""
    try:
        all_usage = get_all_drug_usage_for_user(user_id)
        return all_usage
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all drug usage: {str(e)}") 