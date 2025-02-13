from prompts.base_prompt import CRYPTO_PROMPT

def get_motivation_prompt():
    """Prompt para mensajes de motivación y consejos."""
    return f"""
{CRYPTO_PROMPT}

El usuario necesita motivación o consejos para mejorar su rendimiento.  
Proporciona un mensaje **breve, motivador y enfocado en el progreso personal**.  
Si aplica, incluye **consejos prácticos sobre disciplina, constancia y mentalidad positiva**.  
"""
