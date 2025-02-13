from prompts.base_prompt import CRYPTO_PROMPT

def get_technique_correction_prompt():
    """Prompt para detectar dolor y corregir técnica."""
    return f"""
{CRYPTO_PROMPT}

El usuario ha mencionado **dolor o molestias** al entrenar.  
- **Si el dolor es leve o indica mala postura**, sugiere **correcciones de técnica** y ajustes en la ejecución del ejercicio.  
- **Si el dolor es intenso o persistente**, recomienda **detener el ejercicio y consultar a un profesional**.  
Sé **claro y responsable** en la respuesta.  
"""
