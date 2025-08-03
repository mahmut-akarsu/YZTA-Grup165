import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import SERVER_TIMESTAMP
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()  # Load environment variables from .env file

# Build a robust path to the credentials file
# This ensures the file is found regardless of the script's working directory
cred_path = Path(__file__).resolve().parent.parent.parent / "ilacasistan-yzta-firebase-adminsdk-fbsvc-3c1051b4c4.json"

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()
print(f"Firebase credentials loaded from: {cred_path}")  # Print the path to the credentials file for debugging
