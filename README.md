No Country - Prueba Técnica: Generación y Guardado de Embeddings

Contexto

No Country es una plataforma que valida el comportamiento del talento digital a través de simulaciones laborales colaborativas. El Squad de Datos transforma interacciones en evidencia estructurada para perfiles y dashboards. Esta prueba técnica implementa la Funcionalidad 1: Generación y Guardado de Embeddings, priorizando una base sólida para análisis semántico y consultas RAG.

Justificación de la Elección

Elegí la Funcionalidad 1 porque es fundamental para el análisis semántico y las consultas RAG, herramientas clave para entender patrones de comportamiento y generar insights personalizados. Implementarla primero garantiza un sistema sólido que procese textos de manera eficiente, genere embeddings y elimine duplicados, mejorando la validación de talento. Además, decidí priorizar esta funcionalidad sobre el análisis de sentimiento y tópicos para asegurar una base confiable antes de agregar procesos más avanzados.

Stack Utilizado

Lenguaje: Python
Framework: FastAPI (para el endpoint)
LLM/Embeddings: sentence-transformers/all-MiniLM-L6-v2 (generación de embeddings de 384 dimensiones)
Almacenamiento Vectorial: Supabase PGVector
Base de Datos: Supabase PostgreSQL
Control de Versiones: GitHub
Librerías Adicionales: pandas, nltk, transformers, psycopg2, supabase, emoji, langdetect, sentencepiece, sacremoses

Implementación

La solución procesa textos de interacciones, genera embeddings, los almacena en Supabase, y ofrece un endpoint para verificar duplicados. Se implementó limpieza de texto para mejorar la calidad de los embeddings.
1. Estructura del Proyecto
no_country_prueba_tecnica/
├── src/
│   ├── data/
│   │   └── processing.py      # Limpieza de texto y traducción
│   ├── db/
│   │   └── connect.py        # Conexión y guardado en Supabase
│   ├── embeddings/
│   │   └── generate.py       # Generación de embeddings
├── sample_data.csv           # 100 registros de prueba
├── test_generate_embeddings.py # Script para procesar y guardar embeddings
├── main.py                   # API FastAPI con endpoint /check_embedding
├── requirements.txt          # Dependencias
├── .env                     # Credenciales de Supabase
└── .gitignore               # Ignorar .env y archivos temporales

2. Limpieza de Texto

Módulo: src/data/processing.py
Procesos:
Detecta idioma con langdetect.
Traduce textos en inglés a español usando Helsinki-NLP/opus-mt-en-es, preservando términos de IT (por ejemplo, "bug", "fix", "ASAP").
Convierte a minúsculas, elimina URLs, menciones (@usuario), puntuación, y stopwords (español).
Extrae emoticones con emoji para análisis futuro.
Genera cleaned_text (no almacenado) y text_hash (MD5) para identificar duplicados.


Ejemplo:
Entrada: "Need to fix bugs ASAP @devteam https://example.com"
Salida: cleaned_text: "necesitar fix bugs asap", emoticons: ""



3. Generación y Guardado de Embeddings

Módulo: src/embeddings/generate.py
Proceso:
Lee sample_data.csv (100 registros con userId, teamId, simulationId, type, text, timestamp).
Limpia cada texto y genera embeddings con sentence-transformers/all-MiniLM-L6-v2.
Almacena en Supabase (src/db/connect.py) en la tabla embeddings con columnas: id, userId, teamId, simulationId, type, text, text_hash, embedding, emoticons, timestamp.


Script de Prueba: test_generate_embeddings.py
Procesa los 100 registros y guarda los embeddings.
Muestra los primeros 5 registros (para no saturar la consola).



4. Endpoint para Evitar Duplicación

Módulo: main.py
Endpoint: POST /check_embedding
Recibe un JSON con text (por ejemplo, {"text": "Need to fix bugs ASAP"}).
Limpia el texto, calcula su text_hash, y genera su embedding.
Consulta Supabase para verificar si existe un registro con el mismo text_hash.
Respuesta:
Si es duplicado: {"status": "duplicate", "cleaned_text": "...", "existing_record": {...}}
Si es nuevo: {"status": "new", "cleaned_text": "...", "text_hash": "..."}




Prueba: Usar Swagger UI (http://127.0.0.1:8000/docs) para enviar textos y verificar duplicados.

5. Datos de Prueba

Archivo: sample_data.csv
Contiene 100 registros con:
6 usuarios (user123, user456, etc.) en 3 equipos (teamA, teamB, teamC).
Tipos: chat, feedback, reunion.
Textos en español e inglés, con emoticones, menciones, y URLs.
Timestamps del 1 al 5 de mayo de 2025.



6. Buenas Prácticas

Limpieza de Datos: Traducción estandarizada, eliminación de ruido (URLs, menciones), preservación de acentos y términos técnicos.
Modularidad: Código organizado en módulos (processing, generate, connect) para reusabilidad.
Manejo de Errores: Try-except en scripts para capturar fallos (por ejemplo, conexión a Supabase).
Documentación: Docstrings en funciones y comentarios claros.
Control de Versiones: Commits descriptivos en GitHub.
Seguridad: Credenciales en .env, ignoradas en .gitignore.

Instrucciones para Ejecutar

Clona el repositorio:git clone https://github.com/tu-usuario/no_country_prueba_tecnica.git
cd no_country_prueba_tecnica


Crea un entorno virtual e instala dependencias:python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt


Configura Supabase:
Crea un proyecto en Supabase y habilita PGVector.
Crea la tabla embeddings con las columnas mencionadas.
Añade las credenciales (SUPABASE_URL, SUPABASE_KEY) en .env.


Procesa los datos:python test_generate_embeddings.py


Genera y guarda 100 embeddings en Supabase.


Inicia el servidor FastAPI:uvicorn main:app --reload


Accede a http://127.0.0.1:8000/docs para probar el endpoint.



Resultados

Se procesaron 100 registros de sample_data.csv.
Los embeddings se generaron y guardaron en la tabla embeddings de Supabase.
El endpoint /check_embedding detecta duplicados correctamente, retornando el registro existente o confirmando textos nuevos.
Los textos en inglés se traducen a español (por ejemplo, "Need to fix bugs ASAP" → "necesitar fix bugs asap").
Los emoticones se extraen y almacenan (por ejemplo, "😊 🥳").

Limitaciones y Mejoras Futuras

Limitaciones:
El texto limpio (cleaned_text) no se almacena en Supabase, solo se usa para generar text_hash y embedding.
La traducción puede variar ligeramente para términos técnicos.


Mejoras:
Añadir cleaned_text como columna en embeddings.
Implementar análisis de sentimiento para complementar los embeddings.
Optimizar el rendimiento para datasets más grandes.



Conclusión
La Funcionalidad 1 proporciona una base sólida para análisis semántico en No Country, con un pipeline completo para limpiar textos, generar embeddings, y evitar duplicados. La solución es escalable, cumple con las buenas prácticas, y está lista para integrarse con análisis futuros, como la Funcionalidad 2 (análisis de sentimiento y tópicos).
