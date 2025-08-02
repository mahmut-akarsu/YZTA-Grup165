from app.models.drug import Drug, DrugCreate, DrugUpdate, DrugResponse
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

def add_drug_to_user(user_id: str, drug_data: DrugCreate) -> dict:
    """Add a drug to user's drug list"""
    try:
        print(f"=== ADD DRUG TO USER SERVICE DEBUG ===")
        print(f"User ID: {user_id}")
        print(f"Drug data: {drug_data.dict()}")
        
        # Check if drug with same name already exists
        drug_name = drug_data.name.strip()
        
        # Get existing drugs to check for duplicates
        existing_drugs = get_user_drug_list(user_id)
        for existing_drug in existing_drugs:
            if existing_drug.get("name", "").strip().lower() == drug_name.lower():
                print(f"Drug with name '{drug_name}' already exists")
                raise HTTPException(
                    status_code=400, 
                    detail=f"Drug with name '{drug_name}' already exists for this user"
                )
        
        drug_dict = drug_data.dict()
        drug_dict["user_id"] = user_id
        drug_dict["created_at"] = datetime.now()
        drug_dict["updated_at"] = datetime.now()
        
        drug_id = add_drug_for_user(user_id, drug_dict)
        
        # Return the created drug with all fields
        created_drug = get_user_drug_by_id(user_id, drug_id)
        print(f"Drug created successfully: {created_drug}")
        print(f"=== ADD DRUG TO USER SERVICE DEBUG END ===")
        return created_drug
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in add_drug_to_user: {str(e)}")
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
        
        # Add updated_at timestamp
        update_data["updated_at"] = datetime.now()
        
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

def mark_drug_as_taken(user_id: str, drug_id: str) -> dict:
    """Mark a drug as taken at current time"""
    try:
        # Check if drug exists
        existing_drug = get_user_drug_by_id(user_id, drug_id)
        if not existing_drug:
            raise HTTPException(status_code=404, detail="Drug not found")
        
        current_time = datetime.now()
        
        # Update last_used timestamp
        update_data = {
            "last_used": current_time,
            "updated_at": current_time
        }
        
        success = update_user_drug(user_id, drug_id, update_data)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update drug usage")
        
        # Also record detailed usage
        usage_data = {
            "usage_time": current_time,
            "notes": "Taken via web interface"
        }
        usage_id = record_drug_usage_repo(user_id, drug_id, usage_data)
        
        return {
            "message": "Drug marked as taken successfully",
            "drug_id": drug_id,
            "drug_name": existing_drug.get("name", "Unknown"),
            "taken_at": current_time.isoformat(),
            "usage_id": usage_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error marking drug as taken: {str(e)}")

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

def update_drug_status(user_id: str, drug_id: str, new_status: str) -> dict:
    """Update drug status (active, inactive)"""
    try:
        print(f"=== UPDATE DRUG STATUS DEBUG ===")
        print(f"User ID: {user_id}")
        print(f"Drug ID: {drug_id}")
        print(f"New Status: {new_status}")
        
        # Check if drug exists
        existing_drug = get_user_drug_by_id(user_id, drug_id)
        if not existing_drug:
            raise HTTPException(status_code=404, detail="Drug not found")
        
        # Validate status
        valid_statuses = ["active", "inactive"]
        if new_status.lower() not in valid_statuses:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid status. Must be one of: {valid_statuses}"
            )
        
        # Update status
        update_data = {
            "status": new_status.lower(),
            "updated_at": datetime.now()
        }
        
        success = update_user_drug(user_id, drug_id, update_data)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update drug status")
        
        # Get updated drug
        updated_drug = get_user_drug_by_id(user_id, drug_id)
        
        print(f"Drug status updated successfully")
        print(f"=== UPDATE DRUG STATUS DEBUG END ===")
        
        return {
            "message": f"Drug status updated to {new_status}",
            "drug_id": drug_id,
            "drug_name": updated_drug.get("name", "Unknown"),
            "old_status": existing_drug.get("status", "unknown"),
            "new_status": new_status.lower(),
            "updated_drug": updated_drug
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in update_drug_status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating drug status: {str(e)}") 