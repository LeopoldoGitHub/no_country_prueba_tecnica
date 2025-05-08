from src.data.processing import clean_text

# Texto de prueba con varios emoticones
text = "¡Hola! Código en inglés: bug fix 😊🥳🚀☕. Texto con © y @usuario https://ejemplo.com #ExtraSpaces"
cleaned_text, emoticons = clean_text(text)
print(f"Texto original: {text}")
print(f"Texto limpio: {cleaned_text}")
print(f"Emoticones: {emoticons}")