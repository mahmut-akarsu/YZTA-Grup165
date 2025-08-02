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
    mark_drug_as_taken,
    update_drug_status
)
from app.services.auth_service import get_current_user
from typing import List
from app.models.drug import DrugStatusUpdate

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

@router.get("/test/patient-drugs-example")
def test_patient_drugs_example(current_user=Depends(get_current_user)):
    """Test endpoint to show example patient drugs response"""
    return {
        "message": "Example patient drugs response",
        "example_response": {
            "patient_info": {
                "user_id": "AB123456",
                "name": "Ahmet",
                "surname": "Yılmaz",
                "email": "ahmet@example.com",
                "birth_date": "1990-05-15",
                "full_name": "Ahmet Yılmaz"
            },
            "total_drugs": 3,
            "drugs": [
                {
                    "drug_id": "DRUG_A1B2C3D4",
                    "name": "Parol",
                    "frequency_per_day": 3,
                    "quantity_per_dose": 1,
                    "meal_relation": "NO_FOOD",
                    "duration_days": 7,
                    "last_used": "2024-01-15T14:30:00.000Z",
                    "created_at": "2024-01-15T10:00:00.000Z"
                },
                {
                    "drug_id": "DRUG_E5F6G7H8",
                    "name": "Aspirin",
                    "frequency_per_day": 2,
                    "quantity_per_dose": 1,
                    "meal_relation": "WITH_FOOD",
                    "duration_days": 10,
                    "last_used": None,
                    "created_at": "2024-01-15T11:00:00.000Z"
                }
            ]
        }
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

@router.put("/{drug_id}/status")
def update_drug_status_endpoint(
    drug_id: str, 
    status_update: DrugStatusUpdate,
    current_user=Depends(get_current_user)
):
    """Update drug status (active, inactive, completed)"""
    try:
        return update_drug_status(current_user["user_id"], drug_id, status_update.status)
    except Exception as e:
        print(f"Error in update_drug_status_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating drug status: {str(e)}")

@router.get("/active")
def get_active_drugs(current_user=Depends(get_current_user)):
    """Get only active drugs for the current user"""
    try:
        all_drugs = get_user_drug_list(current_user["user_id"])
        active_drugs = [drug for drug in all_drugs if drug.get("status", "active") == "active"]
        
        return {
            "user_id": current_user["user_id"],
            "total_active_drugs": len(active_drugs),
            "active_drugs": active_drugs
        }
    except Exception as e:
        print(f"Error in get_active_drugs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching active drugs: {str(e)}")

@router.get("/inactive")
def get_inactive_drugs(current_user=Depends(get_current_user)):
    """Get only inactive drugs for the current user"""
    try:
        all_drugs = get_user_drug_list(current_user["user_id"])
        inactive_drugs = [drug for drug in all_drugs if drug.get("status") == "inactive"]
        
        return {
            "user_id": current_user["user_id"],
            "total_inactive_drugs": len(inactive_drugs),
            "inactive_drugs": inactive_drugs
        }
    except Exception as e:
        print(f"Error in get_inactive_drugs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching inactive drugs: {str(e)}")

@router.get("/{drug_id}/status")
def get_drug_status(drug_id: str, current_user=Depends(get_current_user)):
    """Get current drug status"""
    try:
        drug = get_specific_drug(current_user["user_id"], drug_id)
        if not drug:
            raise HTTPException(status_code=404, detail="Drug not found")
        
        return {
            "drug_id": drug_id,
            "drug_name": drug.get("name", "Unknown"),
            "status": drug.get("status", "unknown"),
            "last_used": drug.get("last_used"),
            "created_at": drug.get("created_at"),
            "updated_at": drug.get("updated_at")
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_drug_status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching drug status: {str(e)}")

@router.get("/patient/{patient_id}/all-drugs")
def get_patient_all_drugs(patient_id: str, current_user=Depends(get_current_user)):
    """Get all drugs for a specific patient (for doctors)"""
    try:
        # Check if current user is a doctor
        if current_user.get("role_id", "").lower() != "doctor":
            raise HTTPException(
                status_code=403,
                detail="Access denied. Only doctors can view patient drugs."
            )
        
        print(f"=== GET PATIENT DRUGS DEBUG ===")
        print(f"Doctor ID: {current_user['user_id']}")
        print(f"Patient ID: {patient_id}")
        
        # Get patient's drugs
        patient_drugs = get_user_drug_list(patient_id)
        
        # Get patient info
        from app.repositories.firebase_repo import get_user_by_id
        patient_info = get_user_by_id(patient_id)
        
        if not patient_info:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        print(f"Found {len(patient_drugs)} drugs for patient")
        print(f"=== GET PATIENT DRUGS DEBUG END ===")
        
        return {
            "patient_info": {
                "user_id": patient_info.get("user_id"),
                "name": patient_info.get("name"),
                "surname": patient_info.get("surname"),
                "email": patient_info.get("email"),
                "birth_date": patient_info.get("birth_date"),
                "full_name": f"{patient_info.get('name', '')} {patient_info.get('surname', '')}"
            },
            "total_drugs": len(patient_drugs),
            "drugs": patient_drugs
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_patient_all_drugs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching patient drugs: {str(e)}")

@router.get("/my-all-drugs")
def get_my_all_drugs(current_user=Depends(get_current_user)):
    """Get all drugs for the current user (patient or doctor)"""
    try:
        print(f"=== GET MY ALL DRUGS DEBUG ===")
        print(f"User ID: {current_user['user_id']}")
        print(f"User Role: {current_user.get('role_id')}")
        
        # Get user's drugs
        user_drugs = get_user_drug_list(current_user["user_id"])
        
        # Calculate some statistics
        total_drugs = len(user_drugs)
        active_drugs = [drug for drug in user_drugs if drug.get("last_used") is None]
        used_drugs = [drug for drug in user_drugs if drug.get("last_used") is not None]
        
        print(f"Total drugs: {total_drugs}")
        print(f"Active drugs: {len(active_drugs)}")
        print(f"Used drugs: {len(used_drugs)}")
        print(f"=== GET MY ALL DRUGS DEBUG END ===")
        
        return {
            "user_info": {
                "user_id": current_user.get("user_id"),
                "name": current_user.get("name"),
                "surname": current_user.get("surname"),
                "role_id": current_user.get("role_id"),
                "full_name": f"{current_user.get('name', '')} {current_user.get('surname', '')}"
            },
            "statistics": {
                "total_drugs": total_drugs,
                "active_drugs": len(active_drugs),
                "used_drugs": len(used_drugs)
            },
            "drugs": user_drugs
        }
        
    except Exception as e:
        print(f"Error in get_my_all_drugs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching drugs: {str(e)}")

@router.get("/patient/{patient_id}/drugs-summary")
def get_patient_drugs_summary(patient_id: str, current_user=Depends(get_current_user)):
    """Get a summary of patient's drugs (for doctors)"""
    try:
        # Check if current user is a doctor
        if current_user.get("role_id", "").lower() != "doctor":
            raise HTTPException(
                status_code=403,
                detail="Access denied. Only doctors can view patient drug summaries."
            )
        
        print(f"=== GET PATIENT DRUGS SUMMARY DEBUG ===")
        print(f"Doctor ID: {current_user['user_id']}")
        print(f"Patient ID: {patient_id}")
        
        # Get patient's drugs
        patient_drugs = get_user_drug_list(patient_id)
        
        # Get patient info
        from app.repositories.firebase_repo import get_user_by_id
        patient_info = get_user_by_id(patient_id)
        
        if not patient_info:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Calculate statistics
        total_drugs = len(patient_drugs)
        active_drugs = [drug for drug in patient_drugs if drug.get("last_used") is None]
        used_drugs = [drug for drug in patient_drugs if drug.get("last_used") is not None]
        
        # Group drugs by meal relation
        no_food_drugs = [drug for drug in patient_drugs if drug.get("meal_relation") == "NO_FOOD"]
        with_food_drugs = [drug for drug in patient_drugs if drug.get("meal_relation") == "WITH_FOOD"]
        
        print(f"Found {total_drugs} drugs for patient")
        print(f"=== GET PATIENT DRUGS SUMMARY DEBUG END ===")
        
        return {
            "patient_info": {
                "user_id": patient_info.get("user_id"),
                "name": patient_info.get("name"),
                "surname": patient_info.get("surname"),
                "full_name": f"{patient_info.get('name', '')} {patient_info.get('surname', '')}",
                "birth_date": patient_info.get("birth_date")
            },
            "summary": {
                "total_drugs": total_drugs,
                "active_drugs": len(active_drugs),
                "used_drugs": len(used_drugs),
                "no_food_drugs": len(no_food_drugs),
                "with_food_drugs": len(with_food_drugs)
            },
            "drugs": patient_drugs
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_patient_drugs_summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching patient drug summary: {str(e)}")

@router.get("/test/status-examples")
def test_drug_status_examples(current_user=Depends(get_current_user)):
    """Test endpoint to show drug status examples"""
    return {
        "message": "Drug status examples",
        "status_types": {
            "active": "İlaç aktif olarak kullanılıyor",
            "inactive": "İlaç geçici olarak durduruldu"
        },
        "example_requests": {
            "update_status": {
                "method": "PUT",
                "endpoint": "/drugs/{drug_id}/status",
                "body": {
                    "status": "inactive"
                }
            }
        },
        "example_responses": {
            "update_status": {
                "message": "Drug status updated to inactive",
                "drug_id": "DRUG_A1B2C3D4",
                "drug_name": "Parol",
                "old_status": "active",
                "new_status": "inactive",
                "updated_drug": {...}
            }
        }
    }

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



