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
        # Conectar a Supabase
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()

        # Consulta SQL para insertar datos
        query = """
            INSERT INTO embeddings (
                userId, teamId, simulationId, type, text, text_hash,
                embedding, emoticons, timestamp
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Preparar datos para inserción por lotes
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

        # Insertar datos por lotes
        execute_batch(cur, query, data_to_insert)

        # Confirmar la transacción
        conn.commit()

        # Contar registros guardados
        cur.execute("SELECT COUNT(*) FROM embeddings")
        count = cur.fetchone()[0]

        print(f"Se guardaron {len(data_to_insert)} registros en la tabla embeddings. Total registros: {count}")

        # Cerrar conexión
        cur.close()
        conn.close()

        return len(data_to_insert)

    except Exception as e:
        print(f"Error al guardar embeddings: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        raise e
    
"""
    Notas:
Usa psycopg2 para conectar a Supabase, cargando credenciales desde .env.
La función save_embeddings toma la salida de generate_embeddings (lista de diccionarios).
Inserta datos en la tabla embeddings usando execute_batch para eficiencia.
Almacena embedding como una lista (Supabase con PGVector lo maneja como VECTOR(384)).
Maneja errores y cierra conexiones correctamente.

"""