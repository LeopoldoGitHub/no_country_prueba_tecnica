from src.embeddings.generate import generate_embeddings
from src.db.connect import save_embeddings

# Ruta al archivo CSV
data_path = 'sample_data.csv'

try:
    # Generar embeddings
    results = generate_embeddings(data_path)
    for result in results:
        print(f"userId: {result['userId']}")
        print(f"Texto original: {result['text']}")
        print(f"Texto limpio: {result['cleaned_text']}")
        print(f"Emoticones: {result['emoticons']}")
        print(f"Embedding (primeros 5 valores): {result['embedding'][:5]}")
        print(f"Hash: {result['text_hash']}")
        print("---")

    # Guardar embeddings en Supabase
    saved_count = save_embeddings(results)
    print(f"Total registros guardados: {saved_count}")

except Exception as e:
    print(f"Error: {e}")