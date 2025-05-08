import psycopg2
from psycopg2.extras import execute_batch
from dotenv import load_dotenv
import os

load_dotenv()

def save_embeddings(embeddings_data):
    """
    Guarda una lista de embeddings y metadatos en la tabla 'embeddings' de Supabase.
    Args:
        embeddings_data (list): Lista de diccionarios con userId, teamId, simulationId,
                            type, text, cleaned_text, text_hash, embedding, emoticons, timestamp.
    Returns:
        int: Número de registros guardados.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()

        query = """
            INSERT INTO embeddings (
                userId, teamId, simulationId, type, text, text_hash,
                embedding, emoticons, timestamp
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        data_to_insert = [
            (
                data['userId'],
                data['teamId'],
                data['simulationId'],
                data['type'],
                data['text'],
                data['text_hash'],
                data['embedding'],
                data['emoticons'],
                data['timestamp']
            )
            for data in embeddings_data
        ]

        execute_batch(cur, query, data_to_insert)
        conn.commit()

        cur.execute("SELECT COUNT(*) FROM embeddings")
        count = cur.fetchone()[0]
        print(f"Se guardaron {len(data_to_insert)} registros en la tabla embeddings. Total registros: {count}")

        cur.close()
        conn.close()
        return len(data_to_insert)

    except Exception as e:
        print(f"Error al guardar embeddings: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        raise e

def check_duplicate(text_hash):
    """
    Verifica si un texto ya existe en la tabla 'embeddings' por su hash.
    Args:
        text_hash (str): Hash MD5 del texto limpio.
    Returns:
        dict or None: Registro existente si se encuentra, None si no.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()

        query = "SELECT * FROM embeddings WHERE text_hash = %s"
        cur.execute(query, (text_hash,))
        result = cur.fetchone()

        if result:
            columns = [desc[0] for desc in cur.description]
            result_dict = dict(zip(columns, result))
        else:
            result_dict = None

        cur.close()
        conn.close()
        return result_dict

    except Exception as e:
        print(f"Error al verificar duplicado: {e}")
        if 'conn' in locals():
            conn.close()
        raise e
    
"""
    Notas:
Usa psycopg2 para conectar a Supabase, cargando credenciales desde .env.
La función save_embeddings toma la salida de generate_embeddings (lista de diccionarios).
Inserta datos en la tabla embeddings usando execute_batch para eficiencia.
Almacena embedding como una lista (Supabase con PGVector lo maneja como VECTOR(384)).
Maneja errores y cierra conexiones correctamente.
Añadimos check_duplicate(text_hash) para buscar un registro en la tabla embeddings por su text_hash.
Devuelve un diccionario con el registro existente (si hay coincidencia) o None si no hay duplicados.

"""