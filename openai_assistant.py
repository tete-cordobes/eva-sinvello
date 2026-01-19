import os
from openai import OpenAI
from gspread_handler import save_to_sheet

# IMPORTANTE: Crea un Prompt en el Dashboard de OpenAI y pon el ID aquí
# El Prompt reemplaza al Assistant - configura las instrucciones de Eva ahí
PROMPT_ID = os.getenv("OPENAI_PROMPT_ID", "prompt_TU_PROMPT_ID_AQUI")

# NUNCA pongas la API key en el código - usa variables de entorno
client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_conversation():
    """
    Crea una nueva conversación usando la Conversations API.
    Reemplaza a create_thread() de la vieja Assistants API.
    """
    conversation = client_openai.conversations.create()
    return conversation.id


def ask_assistant(conversation_id, question):
    """
    Envía un mensaje y obtiene respuesta usando la nueva Responses API.
    Ya no necesita polling - es mucho más simple.
    """
    response = client_openai.responses.create(
        model="gpt-4o",  # o el modelo que prefieras
        instructions="Eres Eva, una asistente experta en depilación láser diodo para SinVello. "
                     "Responde de forma amable y profesional a preguntas sobre depilación láser.",
        input=[{"role": "user", "content": question}],
        conversation={"id": conversation_id},
        store=True,  # Guarda en la conversación para mantener contexto
    )

    # La respuesta viene directamente - sin polling!
    assistant_response = response.output_text

    save_to_sheet(conversation_id, question, assistant_response)
    return assistant_response


# Alias para mantener compatibilidad con el código existente
create_thread = create_conversation
