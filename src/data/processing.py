import re
import string
import nltk
from nltk.corpus import stopwords
import unicodedata
import emoji

# Descargar recursos de NLTK (stopwords)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def clean_text(text):
    """
    Limpia un texto en español latinoamericano y separa emoticones usando la librería emoji.
    - Convierte a minúsculas.
    - Elimina URLs, menciones, puntuación, caracteres no ASCII, símbolos especiales.
    - Preserva acentos en español.
    - Elimina stopwords (español).
    - Extrae emoticones para análisis separado, excluyendo símbolos no deseados.
    - Elimina espacios adicionales.
    Args:
        text (str): Texto a limpiar.
    Returns:
        tuple: (texto_limpio: str, emoticones: str)
            - texto_limpio: Texto sin emoticones ni ruido.
            - emoticones: Emoticones expresivos extraídos, separados por espacios.
    """
    # Símbolos no deseados (copyright, marca registrada, etc.)
    unwanted_symbols = {'©', '®', '™'}

    # Extraer emoticones usando la librería emoji, excluyendo símbolos no deseados
    emoticons = [c for c in text if c in emoji.EMOJI_DATA and c not in unwanted_symbols]
    emoticons_str = ' '.join(emoticons) if emoticons else ''
    # Eliminar emoticones y símbolos no deseados del texto
    for char in emoticons + list(unwanted_symbols):
        text = text.replace(char, '')

    # Convertir a minúsculas
    text = text.lower()

    # Eliminar URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    # Eliminar menciones (@usuario)
    text = re.sub(r'@\w+', '', text)

    # Preservar acentos en español (evitar conversión agresiva a ASCII)
    text = unicodedata.normalize('NFC', text)

    # Eliminar puntuación
    text = re.sub(f'[{string.punctuation}]', '', text)

    # Eliminar caracteres no deseados, preservando letras, números y acentos
    text = re.sub(r'[^\w\sáéíóúñ]', '', text)

    # Eliminar espacios adicionales
    text = re.sub(r'\s+', ' ', text).strip()

    # Eliminar stopwords (español)
    stop_words = set(stopwords.words('spanish'))
    words = text.split()
    cleaned_words = [word for word in words if word not in stop_words]
    cleaned_text = ' '.join(cleaned_words)

    return cleaned_text, emoticons_str