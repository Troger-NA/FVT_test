from prompts.base_prompt import CRYPTO_PROMPT

def get_exercise_instructions_prompt():
    """Prompt para explicar cómo realizar ejercicios."""
    return f"""
{CRYPTO_PROMPT}

El usuario ha solicitado instrucciones sobre un ejercicio.  
Explica **cómo realizarlo correctamente**, detallando postura, movimientos y músculos trabajados.  
Si es necesario, menciona errores comunes y cómo evitarlos.  
Usa un tono **claro y directo**.  
"""
