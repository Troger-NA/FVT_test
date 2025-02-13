from prompts.base_prompt import CRYPTO_PROMPT

def get_training_routine_prompt():
    """Prompt para generar rutinas de entrenamiento."""
    return f"""
{CRYPTO_PROMPT}

El usuario está solicitando una rutina de entrenamiento.  
Proporciona un **plan estructurado** según su nivel (principiante, intermedio o avanzado).  
Incluye ejercicios, repeticiones y tiempos de descanso.  
Si el usuario menciona un objetivo (fuerza, resistencia, pérdida de peso), adapta la rutina a ese enfoque.  
Sé **breve y claro** en la respuesta.  
"""
