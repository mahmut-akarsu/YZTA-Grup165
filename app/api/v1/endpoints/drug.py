from fastapi import APIRouter, Depends, HTTPException
from app.models.drug import Drug, DrugCreate, DrugUpdate, DrugResponse, DrugUsage
from app.services.drug_service import (
    add_drug_to_user,
    get_user_drug_list,
    get_specific_drug,
    update_drug_info,
    delete_drug_info,
    record_drug_usage,
    get_drug_usage_history,
    get_all_drug_usage,
    mark_drug_as_taken
)
from app.services.auth_service import get_current_user
from typing import List

router = APIRouter(prefix="/drugs", tags=["Drugs"])

@router.post("/", response_model=dict)
def add_drug(
    drug: DrugCreate,
    current_user=Depends(get_current_user)
):
    """Add a drug to user's drug list"""
    try:
        result = add_drug_to_user(current_user["user_id"], drug)
        print(f"=== ADD DRUG DEBUG ===")
        print(f"User ID: {current_user['user_id']}")
        print(f"Drug data: {drug.dict()}")
        print(f"Result: {result}")
        print(f"=== ADD DRUG DEBUG END ===")
        return result
    except Exception as e:
        print(f"Error in add_drug: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding drug: {str(e)}")

@router.get("/test")
def test_drugs_endpoint(current_user=Depends(get_current_user)):
    """Test endpoint to check if drugs endpoint is working"""
    return {
        "message": "Drugs endpoint is working",
        "user_id": current_user["user_id"],
        "user_email": current_user.get("email", "Unknown"),
        "timestamp": "2024-01-15T12:00:00Z"
    }

@router.get("/search/{drug_name}")
def search_drug_by_name(drug_name: str, current_user=Depends(get_current_user)):
    """Search for a drug by name"""
    try:
        print(f"=== SEARCH DRUG DEBUG ===")
        print(f"Searching for drug: {drug_name}")
        print(f"User ID: {current_user['user_id']}")
        
        # Get all drugs for the user
        all_drugs = get_user_drug_list(current_user["user_id"])
        
        # Search for drugs with matching name (case-insensitive)
        matching_drugs = []
        for drug in all_drugs:
            if drug_name.lower() in drug.get("name", "").lower():
                matching_drugs.append(drug)
        
        print(f"Found {len(matching_drugs)} matching drugs")
        print(f"=== SEARCH DRUG DEBUG END ===")
        
        return {
            "search_term": drug_name,
            "total_found": len(matching_drugs),
            "drugs": matching_drugs
        }
        
    except Exception as e:
        print(f"Error in search_drug_by_name: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error searching for drug: {str(e)}")

@router.get("/check-name/{drug_name}")
def check_drug_name_exists(drug_name: str, current_user=Depends(get_current_user)):
    """Check if a drug with the given name already exists"""
    try:
        print(f"=== CHECK DRUG NAME DEBUG ===")
        print(f"Checking drug name: {drug_name}")
        print(f"User ID: {current_user['user_id']}")
        
        # Get all drugs for the user
        all_drugs = get_user_drug_list(current_user["user_id"])
        
        # Check for exact match (case-insensitive)
        existing_drug = None
        for drug in all_drugs:
            if drug.get("name", "").strip().lower() == drug_name.strip().lower():
                existing_drug = drug
                break
        
        print(f"Drug exists: {existing_drug is not None}")
        print(f"=== CHECK DRUG NAME DEBUG END ===")
        
        return {
            "drug_name": drug_name,
            "exists": existing_drug is not None,
            "existing_drug": existing_drug
        }
        
    except Exception as e:
        print(f"Error in check_drug_name_exists: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error checking drug name: {str(e)}")

@router.get("/", response_model=List[dict])
def get_drugs(current_user=Depends(get_current_user)):
    """
    Get all drugs for the current user
    
    Returns:
    - drug_id: Unique identifier for the drug
    - name: Drug name
    - frequency_per_day: How many times per day
    - quantity_per_dose: How many pills per dose
    - meal_relation: NO_FOOD or WITH_FOOD
    - duration_days: How many days to take
    - last_used: When it was last taken
    - created_at: When it was added
    - updated_at: When it was last updated
    """
    try:
        drugs = get_user_drug_list(current_user["user_id"])
        print(f"=== GET DRUGS DEBUG ===")
        print(f"User ID: {current_user['user_id']}")
        print(f"Found {len(drugs)} drugs")
        for drug in drugs:
            print(f"Drug: {drug.get('name', 'Unknown')} - ID: {drug.get('drug_id', 'No ID')}")
        print(f"=== GET DRUGS DEBUG END ===")
        return drugs
    except Exception as e:
        print(f"Error in get_drugs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching drugs: {str(e)}")

@router.get("/{drug_id}", response_model=dict)
def get_drug(drug_id: str, current_user=Depends(get_current_user)):
    """Get a specific drug by ID"""
    try:
        drug = get_specific_drug(current_user["user_id"], drug_id)
        if not drug:
            raise HTTPException(status_code=404, detail="Drug not found")
        return drug
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_drug: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching drug: {str(e)}")

@router.put("/{drug_id}", response_model=dict)
def update_drug(
    drug_id: str,
    drug: DrugUpdate,
    current_user=Depends(get_current_user)
):
    """Update a drug's information"""
    try:
        drug_dict = drug.dict(exclude_unset=True)
        return update_drug_info(current_user["user_id"], drug_id, drug_dict)
    except Exception as e:
        print(f"Error in update_drug: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating drug: {str(e)}")

@router.delete("/{drug_id}")
def delete_drug(drug_id: str, current_user=Depends(get_current_user)):
    """Delete a drug from user's list"""
    return delete_drug_info(current_user["user_id"], drug_id)

@router.post("/{drug_id}/take")
def take_drug(drug_id: str, current_user=Depends(get_current_user)):
    """Mark a drug as taken (used) at current time"""
    return mark_drug_as_taken(current_user["user_id"], drug_id)

@router.get("/{drug_id}/last-used")
def get_last_used(drug_id: str, current_user=Depends(get_current_user)):
    """Get when the drug was last used"""
    drug = get_specific_drug(current_user["user_id"], drug_id)
    return {
        "drug_id": drug_id,
        "drug_name": drug.get("name", "Unknown"),
        "last_used": drug.get("last_used"),
        "message": "Last used time retrieved successfully"
    }

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



