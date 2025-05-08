import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM embeddings LIMIT 1")
    print("Conexión exitosa, tabla embeddings encontrada!")
    conn.close()
except Exception as e:
    print(f"Error de conexión: {e}")