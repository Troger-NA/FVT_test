import re
import cohere
from flask import Flask, request, jsonify
from textblob import TextBlob
from transformers import pipeline
from prompts.general import get_general_prompt
from prompts.training_routines import get_training_routine_prompt
from prompts.exercise_instructions import get_exercise_instructions_prompt
from prompts.technique_correction import get_technique_correction_prompt
from prompts.motivation import get_motivation_prompt

# Configuración del bot
COHERE_API_KEY = "9foAkbHGuvD7YosI0ujg65fhdUoxur4c8DIZ4FDK"
co = cohere.Client(COHERE_API_KEY)

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 5000))
# Cargar modelo de análisis de sentimiento con BERT
classifier = pipeline("text-classification", model="distilbert-base-uncased", return_all_scores=True)

# Configuración de tokens por categoría
TOPIC_MAX_TOKENS = {
    "training_routines": 200,  
    "exercise_instructions": 200,  
    "technique_correction": 150,  
    "motivation": 100,  
    "general": 100  
}

# Palabras clave para detectar el tópico
keywords = {
    "general": [
        r"qué es FVT", r"cómo funciona FVT", r"quién dirige FVT", r"qué significa FVT",
        r"dónde están ubicados", r"cuánto cuesta FVT", r"qué ofrece FVT", r"cómo unirse a FVT",
        r"qué tipo de entrenamiento hacen", r"FVT es online", r"hay clases en vivo",
        r"qué incluye la membresía", r"qué beneficios tiene FVT", r"qué modalidad de entrenamiento tienen"
    ],
    "training_routines": [
        r"rutina", r"plan de entrenamiento", r"qué ejercicios hacer", r"entrenamiento para",
        r"programa de entrenamiento", r"rutina para fuerza", r"rutina para perder peso",
        r"rutina para ganar músculo", r"entrenamiento funcional", r"cuántos días entrenar",
        r"rutina para principiantes", r"entrenamiento avanzado", r"mejor rutina para quemar grasa",
        r"ejercicios para fortalecer el core", r"rutina con pesas", r"rutina sin equipo",
        r"rutina para resistencia", r"rutina HIIT", r"entrenamiento de circuito", r"rutina semanal"
    ],
    "exercise_instructions": [
        r"cómo hacer", r"instrucciones de", r"ejecución correcta de", r"forma correcta de",
        r"cómo se hace un", r"explicación de", r"tutorial de", r"técnica para",
        r"cómo mejorar mi postura en", r"cómo evitar lesiones haciendo", r"errores comunes en",
        r"cuántas repeticiones hacer de", r"respiración en", r"ejercicio para piernas",
        r"cómo activar el core", r"forma correcta de hacer sentadillas", r"postura correcta en peso muerto"
    ],
    "technique_correction": [
        r"siento dolor", r"me duele", r"ejercicio me molesta", r"cómo evitar lesiones",
        r"me duele la espalda al hacer", r"molestia en las rodillas", r"cómo corregir la postura en",
        r"me lastimé entrenando", r"qué hacer si siento dolor en", r"ejercicios peligrosos",
        r"cómo evitar el dolor de espalda", r"postura correcta en ejercicios", r"lesión por mala técnica",
        r"tengo dolor en el hombro", r"qué hacer si siento molestias al entrenar"
    ],
    "motivation": [
        r"necesito motivación", r"estoy desmotivado", r"cómo mejorar", r"quiero progresar",
        r"me cuesta entrenar", r"no veo resultados", r"quiero ser más constante",
        r"cómo mantener la disciplina", r"consejos para entrenar mejor", r"mentalidad en el gimnasio",
        r"quiero ser más fuerte", r"cómo no rendirse", r"motivación para entrenar",
        r"frases motivacionales", r"cómo encontrar disciplina", r"cómo superar mis límites"
    ]
}

# Detección contextual para mejorar la clasificación
context_keywords = {
    "training_routines": [
        "entrenamiento", "rutina", "plan", "ejercicios", "circuito", "workout", "programa",
        "entrenamiento en casa", "ejercicio semanal", "entrenamiento personalizado",
        "cuántas veces entrenar", "cuántos días a la semana", "sesión de entrenamiento",
        "series y repeticiones", "frecuencia de entrenamiento"
    ],
    "exercise_instructions": [
        "cómo hacer", "ejecución", "postura", "forma correcta", "técnica de ejercicio",
        "movimiento correcto", "instrucciones detalladas", "paso a paso", "respiración",
        "activación muscular", "alineación del cuerpo", "movimiento seguro"
    ],
    "technique_correction": [
        "dolor", "lesión", "molestia", "mala postura", "corregir técnica",
        "problema en articulaciones", "sobrecarga", "postura incorrecta", "prevención de lesiones",
        "riesgo de lesión", "alineación de la columna", "sobreesfuerzo", "fatiga muscular"
    ],
    "motivation": [
        "disciplina", "constancia", "motivación", "superación", "hábitos",
        "fuerza mental", "compromiso", "hábitos saludables", "determinación",
        "superar barreras", "rendimiento óptimo", "actitud positiva", "mentalidad ganadora"
    ]
}

# Detectar la emoción del mensaje
def detect_emotion(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    bert_scores = classifier(text)[0]

    bert_positive = next((score for score in bert_scores if score['label'] == 'LABEL_1'), {'score': 0.0})['score']
    bert_negative = next((score for score in bert_scores if score['label'] == 'LABEL_0'), {'score': 0.0})['score']

    if polarity > 0.1 or bert_positive > 0.6:
        return "positivo"
    elif polarity < -0.1 or bert_negative > 0.6:
        return "negativo"
    else:
        return "neutral"

# Detectar el tópico del mensaje
def detect_topic(user_message):
    user_message_lower = user_message.lower()

    # Buscar coincidencias con regex
    for category, patterns in keywords.items():
        for pattern in patterns:
            if re.search(pattern, user_message_lower):
                return category

    # Detección contextual como fallback
    for category, keywords_list in context_keywords.items():
        if any(keyword in user_message_lower for keyword in keywords_list):
            return category

    return "general"

# Obtener el prompt según el tema detectado
def get_prompt_by_topic(topic):
    if topic == "training_routines":
        return get_training_routine_prompt()
    elif topic == "exercise_instructions":
        return get_exercise_instructions_prompt()
    elif topic == "technique_correction":
        return get_technique_correction_prompt()
    elif topic == "motivation":
        return get_motivation_prompt()
    return get_general_prompt()

# Truncar respuesta a la última oración completa
def truncate_to_complete_sentence(text, max_length):
    """Trunca el texto a la oración completa más cercana dentro del límite."""
    if len(text) <= max_length:
        return text

    truncated_text = text[:max_length]

    # Buscar la última oración completa (termina en ".", "!", "?")
    match = re.search(r'([.!?])[^.!?]*$', truncated_text)
    if match:
        return truncated_text[:match.end()].strip()

    # Si no hay puntuación clara, devolver el texto truncado pero evitando cortar la última palabra
    words = truncated_text.split()
    if len(words) > 1:
        return " ".join(words[:-1]) + "..."

    return truncated_text.strip()

# Generar respuesta con Cohere
def generate_response(user_message):
    topic = detect_topic(user_message)
    emotion = detect_emotion(user_message)
    prompt = get_prompt_by_topic(topic)

    full_prompt = f"""
{prompt}

Mensaje del usuario: {user_message}
Emoción detectada: {emotion}
Respuesta del asistente:
"""

    response = co.generate(
        model="command-xlarge-nightly",
        prompt=full_prompt,
        max_tokens=TOPIC_MAX_TOKENS.get(topic, 100),
        temperature=0.4
    )

    response_text = response.generations[0].text.strip()
    return truncate_to_complete_sentence(response_text, max_length=TOPIC_MAX_TOKENS.get(topic, 400))

# Endpoint para manejar mensajes en el chat

