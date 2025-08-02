import random
import string
from app.core.firebase import db
from app.models.user import UserRegister, UserOut
from app.models.drug import Drug
import uuid
from typing import List, Optional
from datetime import datetime

def generate_basic_user_id(role: str) -> str:
    if role.lower() == "doctor":
        letters = "DR"
    else:
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    numbers = ''.join(random.choices(string.digits, k=6))
    return letters + numbers

def create_user(user_data: dict) -> str:
    role = user_data.get("role_id", "")
    user_id = generate_basic_user_id(role)
    user_data["user_id"] = user_id
    db.collection("users").document(user_id).set(user_data)
    return user_id

def get_user_by_id(user_id: str) -> dict | None:
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

def get_user_by_email(email: str) -> dict | None:
    users_ref = db.collection("users")
    query = users_ref.where("email", "==", email).limit(1).stream()
    for doc in query:
        return doc.to_dict()
    return None

def add_drug_for_patient(drug_data: dict) -> str:
    drug_id = str(uuid.uuid4())
    drug_data["drug_id"] = drug_id
    db.collection("drugs").document(drug_id).set(drug_data)
    return drug_id

# User drugs subcollection functions
def add_drug_for_user(user_id: str, drug_data: dict) -> str:
    """Add a drug to user's drugs subcollection"""
    drug_id = str(uuid.uuid4())
    drug_data["drug_id"] = drug_id
    
    # Add drug to user's drugs subcollection
    db.collection("users").document(user_id).collection("drugs").document(drug_id).set(drug_data)
    return drug_id

def get_user_drugs(user_id: str) -> List[dict]:
    """Get all drugs for a specific user"""
    drugs = []
    drugs_ref = db.collection("users").document(user_id).collection("drugs")
    docs = drugs_ref.stream()
    
    for doc in docs:
        drug_data = doc.to_dict()
        drug_data["drug_id"] = doc.id
        drugs.append(drug_data)
    
    return drugs

def get_user_drug_by_id(user_id: str, drug_id: str) -> Optional[dict]:
    """Get a specific drug for a user"""
    doc_ref = db.collection("users").document(user_id).collection("drugs").document(drug_id)
    doc = doc_ref.get()
    
    if doc.exists:
        drug_data = doc.to_dict()
        drug_data["drug_id"] = doc.id
        return drug_data
    return None

def update_user_drug(user_id: str, drug_id: str, drug_data: dict) -> bool:
    """Update a drug for a user"""
    try:
        doc_ref = db.collection("users").document(user_id).collection("drugs").document(drug_id)
        doc_ref.update(drug_data)
        return True
    except Exception as e:
        print(f"Error updating drug: {e}")
        return False

def delete_user_drug(user_id: str, drug_id: str) -> bool:
    """Delete a drug from user's subcollection"""
    try:
        doc_ref = db.collection("users").document(user_id).collection("drugs").document(drug_id)
        doc_ref.delete()
        return True
    except Exception as e:
        print(f"Error deleting drug: {e}")
        return False

# Drug usage tracking functions
def record_drug_usage(user_id: str, drug_id: str, usage_data: dict) -> str:
    """Record a drug usage for a user"""
    usage_id = str(uuid.uuid4())
    usage_time = datetime.now()
    usage_data["usage_id"] = usage_id
    usage_data["usage_time"] = usage_time
    
    print(f"=== DRUG USAGE DEBUG ===")
    print(f"Recording usage for user: {user_id}, drug: {drug_id}")
    print(f"Usage time: {usage_time}")
    print(f"Usage data: {usage_data}")
    
    # Add usage record to user's drug usage subcollection
    db.collection("users").document(user_id).collection("drugs").document(drug_id).collection("usage").document(usage_id).set(usage_data)
    
    # Update last_used timestamp in drug document
    drug_ref = db.collection("users").document(user_id).collection("drugs").document(drug_id)
    drug_ref.update({"last_used": usage_time})
    
    print(f"Usage record created with ID: {usage_id}")
    print(f"=== DRUG USAGE DEBUG END ===")
    
    return usage_id

def get_drug_usage_history(user_id: str, drug_id: str) -> List[dict]:
    """Get usage history for a specific drug"""
    usage_records = []
    usage_ref = db.collection("users").document(user_id).collection("drugs").document(drug_id).collection("usage")
    docs = usage_ref.stream()
    
    for doc in docs:
        usage_data = doc.to_dict()
        usage_data["usage_id"] = doc.id
        usage_records.append(usage_data)
    
    return usage_records

def get_all_drug_usage_for_user(user_id: str) -> List[dict]:
    """Get all drug usage for a user"""
    all_usage = []
    drugs_ref = db.collection("users").document(user_id).collection("drugs")
    drug_docs = drugs_ref.stream()
    
    for drug_doc in drug_docs:
        drug_data = drug_doc.to_dict()
        usage_ref = drug_doc.reference.collection("usage")
        usage_docs = usage_ref.stream()
        
        for usage_doc in usage_docs:
            usage_data = usage_doc.to_dict()
            usage_data["usage_id"] = usage_doc.id
            usage_data["drug_id"] = drug_doc.id
            usage_data["drug_name"] = drug_data.get("name", "Unknown")
            all_usage.append(usage_data)
    
    return all_usage

def update_drug_last_used(user_id: str, drug_id: str) -> bool:
    """Update last_used timestamp for a drug"""
    try:
        drug_ref = db.collection("users").document(user_id).collection("drugs").document(drug_id)
        drug_ref.update({"last_used": datetime.now()})
        return True
    except Exception as e:
        print(f"Error updating last_used: {e}")
        return False

# Drug summary functions
def update_drug_summary(user_id: str, drug_id: str, usage_time: datetime) -> bool:
    """Update drug summary statistics"""
    try:
        print(f"=== SUMMARY UPDATE DEBUG ===")
        print(f"Updating summary for user: {user_id}, drug: {drug_id}")
        print(f"Usage time: {usage_time}")
        
        drug_ref = db.collection("users").document(user_id).collection("drugs").document(drug_id)
        
        # Get current summary
        doc = drug_ref.get()
        if doc.exists:
            current_data = doc.to_dict()
            print(f"Current data: {current_data}")
            
            # Update summary
            total_count = current_data.get("total_usage_count", 0) + 1
            first_used = current_data.get("first_used", usage_time)
            
            # Calculate average interval if we have previous usage
            avg_interval = None
            if current_data.get("last_used"):
                time_diff = (usage_time - current_data["last_used"]).total_seconds() / 3600
                current_avg = current_data.get("average_interval_hours", time_diff)
                avg_interval = ((current_avg * (total_count - 1)) + time_diff) / total_count
                print(f"Time diff: {time_diff} hours")
                print(f"Current avg: {current_avg}")
                print(f"New avg: {avg_interval}")
            
            # Update summary
            summary_update = {
                "total_usage_count": total_count,
                "last_used": usage_time,
                "first_used": first_used,
                "average_interval_hours": avg_interval
            }
            
            print(f"Summary update: {summary_update}")
            drug_ref.update(summary_update)
        else:
            # First usage
            first_usage_update = {
                "total_usage_count": 1,
                "last_used": usage_time,
                "first_used": usage_time,
                "average_interval_hours": None
            }
            print(f"First usage update: {first_usage_update}")
            drug_ref.update(first_usage_update)
        
        print(f"=== SUMMARY UPDATE DEBUG END ===")
        return True
    except Exception as e:
        print(f"Error updating drug summary: {e}")
        return False

def get_drug_summary(user_id: str, drug_id: str) -> Optional[dict]:
    """Get drug summary statistics"""
    try:
        print(f"=== GET SUMMARY DEBUG ===")
        print(f"Getting summary for user: {user_id}, drug: {drug_id}")
        
        doc_ref = db.collection("users").document(user_id).collection("drugs").document(drug_id)
        doc = doc_ref.get()
        
        if doc.exists:
            data = doc.to_dict()
            print(f"Raw data from Firebase: {data}")
            
            summary = {
                "total_usage_count": data.get("total_usage_count", 0),
                "last_used": data.get("last_used"),
                "first_used": data.get("first_used"),
                "average_interval_hours": data.get("average_interval_hours"),
                "recent_usage_count": data.get("recent_usage_count", 0)
            }
            print(f"Processed summary: {summary}")
            print(f"=== GET SUMMARY DEBUG END ===")
            return summary
        else:
            print(f"Document does not exist!")
            print(f"=== GET SUMMARY DEBUG END ===")
        return None
    except Exception as e:
        print(f"Error getting drug summary: {e}")
        return None

def cleanup_old_usage_records(user_id: str, drug_id: str, keep_last: int = 30) -> bool:
    """Keep only the last N usage records and delete older ones"""
    try:
        usage_ref = db.collection("users").document(user_id).collection("drugs").document(drug_id).collection("usage")
        
        # Get all usage records ordered by time
        docs = usage_ref.order_by("usage_time", direction="DESCENDING").stream()
        usage_records = []
        
        for doc in docs:
            usage_records.append((doc.id, doc.to_dict()))
        
        # Keep only the last N records
        if len(usage_records) > keep_last:
            records_to_delete = usage_records[keep_last:]
            
            # Delete old records
            for record_id, _ in records_to_delete:
                usage_ref.document(record_id).delete()
            
            # Update recent count
            drug_ref = db.collection("users").document(user_id).collection("drugs").document(drug_id)
            drug_ref.update({"recent_usage_count": keep_last})
        
        return True
    except Exception as e:
        print(f"Error cleaning up old usage records: {e}")
        return False

# Doctor functions for viewing patient drugs
def get_patient_drugs_for_doctor(patient_id: str) -> List[dict]:
    """Get all drugs for a specific patient (for doctors)"""
    drugs = []
    drugs_ref = db.collection("users").document(patient_id).collection("drugs")
    docs = drugs_ref.stream()
    
    for doc in docs:
        drug_data = doc.to_dict()
        drug_data["drug_id"] = doc.id
        drugs.append(drug_data)
    
    return drugs

def get_patient_info_for_doctor(patient_id: str) -> Optional[dict]:
    """Get patient information (for doctors)"""
    doc_ref = db.collection("users").document(patient_id)
    doc = doc_ref.get()
    
    if doc.exists:
        patient_data = doc.to_dict()
        patient_data["user_id"] = doc.id
        return patient_data
    return None

def get_all_patients_for_doctor() -> List[dict]:
    """Get all patients (for doctors)"""
    patients = []
    users_ref = db.collection("users")
    docs = users_ref.stream()
    
    for doc in docs:
        user_data = doc.to_dict()
        user_data["user_id"] = doc.id
        # Only return patients (not doctors)
        if user_data.get("role_id", "").lower() == "patient":
            patients.append(user_data)
    
    return patients





