from app.core.firebase import db

def get_user_by_email(email: str):
    users = db.collection("users").where("email", "==", email).stream()
    for u in users:
        user = u.to_dict()
        user["user_id"] = u.id
        return user
    return None

def create_user(user_data: dict) -> str:
    user_ref = db.collection("users").add(user_data)
    return user_ref[1].id  # Firebase auto-ID

