from fastapi import APIRouter, UploadFile, File, HTTPException
import easyocr
import numpy as np
from PIL import Image
import io

router = APIRouter(prefix="/ocr", tags=["OCR"])

# initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

@router.post("/recognize")
async def recognize_text(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")
    
    # Read the uploaded image file
    image_bytes = await file.read()
    
    # Open image and convert to RGB
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # Convert PIL image to NumPy array
    np_image = np.array(image)
    
    # Perform OCR
    result = reader.readtext(np_image, detail=0)
    text = " ".join(result)

    return {"recognized_text": text}
