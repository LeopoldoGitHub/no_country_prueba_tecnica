import pandas as pd
from sentence_transformers import SentenceTransformer
from src.data.processing import clean_text
import hashlib

def generate_embeddings(data_path):
    """
    Genera embeddings para textos en un archivo CSV y asocia metadatos.
    Args:
        data_path (str): Ruta al archivo CSV con columnas:
                        userId, teamId, simulationId, type, text, timestamp.
    Returns:
        list: Lista de diccionarios con metadatos, texto limpio, hash, embedding y emoticones.
    """
    # Cargar el modelo sentence-transformers
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Leer el archivo CSV
    df = pd.read_csv(data_path)

    # Verificar columnas requeridas
    required_columns = ['userId', 'teamId', 'simulationId', 'type', 'text', 'timestamp']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"El CSV debe contener las columnas: {required_columns}")

    results = []
    for _, row in df.iterrows():
        # Limpiar el texto y extraer emoticones
        cleaned_text, emoticons = clean_text(row['text'])

        # Generar hash del texto limpio para detección de duplicados
        text_hash = hashlib.md5(cleaned_text.encode('utf-8')).hexdigest()

        # Generar embedding
        embedding = model.encode(cleaned_text, convert_to_numpy=True).tolist()

        # Crear diccionario con metadatos
        result = {
            'userId': row['userId'],
            'teamId': row['teamId'],
            'simulationId': row['simulationId'],
            'type': row['type'],
            'text': row['text'],
            'cleaned_text': cleaned_text,
            'text_hash': text_hash,
            'embedding': embedding,
            'emoticons': emoticons,
            'timestamp': row['timestamp']
        }
        results.append(result)

    return results
"""Notas:
Usa el modelo all-MiniLM-L6-v2 de sentence-transformers, que genera embeddings de 384 dimensiones, ideal para textos cortos.
La función clean_text de src/data/processing.py limpia el texto y extrae emoticones.
Genera un hash MD5 (text_hash) del texto limpio para detectar duplicados en el futuro (para el endpoint /check_embedding).
Espera un CSV con columnas: userId, teamId, simulationId, type, text, timestamp.
Devuelve una lista de diccionarios con metadatos, texto limpio, hash, embedding, y emoticones."""