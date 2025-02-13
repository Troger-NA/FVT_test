from prompts.base_prompt import CRYPTO_PROMPT

def get_general_prompt():
    """Prompt para información general sobre FVT Training."""
    general_data = """
    ¡Bienvenido a FVT Training! 💪🔥  
    Somos un grupo de entrenamiento dirigido por Franco Vali, con sedes al aire libre y modalidad online.  
    Ofrecemos entrenamientos funcionales para mejorar fuerza, resistencia y movilidad.  

    ¿Necesitas una rutina, consejos o ayuda con tu técnica? Pregunta y estaré encantado de ayudarte. 🚀🏋️‍♂️  
    """

    return f"""
{CRYPTO_PROMPT}

El usuario está preguntando sobre FVT Training.  
Responde de manera **clara y concisa**, explicando qué es FVT y cómo puede ayudarlo:  
{general_data}
"""
