from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.data.processing import clean_text
from src.db.connect import check_duplicate
import hashlib

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/check_embedding")
async def check_embedding(input: TextInput):
    """
    Verifica si un texto ya existe en la tabla embeddings comparando su hash.
    Args:
        input (TextInput): Objeto con el texto a verificar.
    Returns:
        dict: Estado (duplicado o no) y datos del registro si existe.
    """
    try:
        # Limpiar el texto
        cleaned_text, _ = clean_text(input.text)
        # Generar hash del texto limpio
        text_hash = hashlib.md5(cleaned_text.encode('utf-8')).hexdigest()
        # Verificar duplicado en la base de datos
        existing_record = check_duplicate(text_hash)

        if existing_record:
            return {
                "status": "duplicate",
                "cleaned_text": cleaned_text,
                "existing_record": existing_record
            }
        else:
            return {
                "status": "new",
                "cleaned_text": cleaned_text,
                "text_hash": text_hash
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    
"""
    Notas:
Usa FastAPI para crear el endpoint /check_embedding.
Limpia el texto con clean_text (traduciendo inglés a español si es necesario).
Calcula el hash MD5 del texto limpio.
Usa check_duplicate para buscar el hash en la tabla embeddings.
Devuelve un JSON con el estado ("duplicate" o "new") y los datos relevantes.

"""