import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import SERVER_TIMESTAMP
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

cred_path = "yzta-grup165-firebase-adminsdk-fbsvc-b24c7f9b69.json"
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()
print(cred_path)  # Print the path to the credentials file for debugging