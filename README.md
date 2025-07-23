# FastAPI Drug System Documentation

This documentation provides a comprehensive overview of the FastAPI Drug System project, including its structure, setup, and usage.

## 1. Project Structure

The project is organized into the following directory structure:

```
fastapi_drug_system/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── auth.py
│   │           ├── ocr.py
│   │           └── user.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   │   ├── user.py
│   ├── schemas/
│   │   └── user.py
│   ├── services/
│   │   └── user_service.py
│   ├── utils/
│   │   └── firebase.py (TBD)
│   └── main.py
├── .env
└── requirements.txt
```

## 2. ⚙️ Setup Instructions

Follow these steps to set up the project environment:

### 2.1. Create and Activate Environment

First, create a virtual environment:

```bash
python -m venv drug_project
```

Then, activate it:

```bash
.\drug_project\Scripts\activate
```

### 2.2. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```


## 3. 🚀 Running the Server

To run the FastAPI development server, use the following command:

```bash
uvicorn app.main:app --reload
```

You can access the API documentation at `http://127.0.0.1:8000/docs`.

## 4. 🔐 Authentication & Roles

The application uses role-based authentication.

### 4.1. Register

To create a new user, send a POST request to `/auth/register`. You can assign a role of "doctor" or "patient".

```http
POST /auth/register
Content-Type: application/json

{
  "email": "example@gmail.com",
  "password": "yourpassword",
  "role": "doctor" 
}
```

### 4.2. Login

To authenticate, send a POST request to `/auth/login`. This will return a JWT token for accessing protected endpoints.

Roles are managed within the user model and enforced at the route level using dependencies.

## 5. 🧾 OCR Endpoint

### 5.1. /ocr/recognize

This endpoint allows you to upload an image of a pillbox and returns the recognized text.

To use this endpoint, send a POST request with the image file.

```http
POST /ocr/recognize
Content-Type: multipart/form-data
```

**Form field:** `file` = image (jpg/png)

**Example Response:**

```json
{
  "recognized_text": "ASPIRINA"
}
```

**Notes:**
*   This feature is powered by EasyOCR.
*   It accepts common image formats like .jpg and .png.
*   Images are automatically converted to an RGB NumPy array for processing.

## 6. 🔐 Firebase Setup (To Be Completed)

The following steps are for future integration with Firebase:

1.  Create a project in the Firebase console.
2.  Download the `firebase_credentials.json` file and place it in the project's root directory.
3.  Add the following line to your `.env` file:

```ini
FIREBASE_CREDENTIALS=./firebase_credentials.json
```
