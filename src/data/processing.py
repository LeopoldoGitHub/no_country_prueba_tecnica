import re
import string
import nltk
from nltk.corpus import stopwords
import unicodedata
import emoji
from transformers import pipeline
import langdetect

# Descargar recursos de NLTK (stopwords)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Inicializar el pipeline de traducción (inglés a español)
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-es")

# Términos de IT en inglés que no se traducen
IT_TERMS = {
    'bug', 'fix', 'asap', 'code', 'coding', 'debug', 'feature', 'api',
    'backend', 'frontend', 'deploy', 'commit', 'merge', 'pull', 'push',
    'repository', 'repo', 'branch', 'version', 'release', 'patch'
}

def clean_text(text):
    """
    Limpia un texto, traduciendo inglés a español y separando emoticones.
    - Detecta el idioma y traduce inglés a español, preservando términos de IT.
    - Convierte a minúsculas.
    - Elimina URLs, menciones, puntuación, símbolos especiales.
    - Preserva acentos en español.
    - Elimina stopwords (español).
    - Extrae emoticones, excluyendo símbolos no deseados.
    - Elimina espacios adicionales.
    Args:
        text (str): Texto a limpiar.
    Returns:
        tuple: (texto_limpio: str, emoticones: str)
            - texto_limpio: Texto en español sin emoticones ni ruido.
            - emoticones: Emoticones expresivos extraídos.
    """
    # Símbolos no deseados
    unwanted_symbols = {'©', '®', '™'}

    # Extraer emoticones
    emoticons = [c for c in text if c in emoji.EMOJI_DATA and c not in unwanted_symbols]
    emoticons_str = ' '.join(emoticons) if emoticons else ''
    for char in emoticons + list(unwanted_symbols):
        text = text.replace(char, '')

    # Detectar idioma
    try:
        lang = langdetect.detect(text)
    except:
        lang = 'es'  # Asumir español si la detección falla

    # Traducir si es inglés, preservando términos de IT
    if lang == 'en':
        # Proteger términos de IT
        for term in IT_TERMS:
            text = text.replace(term, f'__{term}__')
        # Traducir
        translated = translator(text)[0]['translation_text']
        # Restaurar términos de IT
        for term in IT_TERMS:
            translated = translated.replace(f'__{term}__', term)
        # Estandarizar traducciones específicas
        translated = translated.replace('necesidad', 'necesitar')
        translated = translated.replace('tan pronto como sea posible', 'asap')
        translated = translated.replace('lo antes posible', 'asap')
        text = translated

    # Convertir a minúsculas
    text = text.lower()

    # Eliminar URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    # Eliminar menciones (@usuario)
    text = re.sub(r'@\w+', '', text)

    # Preservar acentos en español
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
    cleaned_words = [word for word in words if word not in stop_words or word in IT_TERMS]
    cleaned_text = ' '.join(cleaned_words)

    return cleaned_text, emoticons_str

"""Instalamos langdetect para detectar el idioma del texto (pip install langdetect).
Usamos transformers con el modelo Helsinki-NLP/opus-mt-en-es para traducir inglés a español.
Definimos IT_TERMS para preservar términos como "bug", "fix", "ASAP" sin traducirlos.
Proteger términos de IT con marcadores (__term__) antes de traducir y restaurarlos después.
Aseguramos que los términos de IT no se eliminen como stopwords.
El resto del script (emoticones, URLs, menciones, acentos) permanece igual."""