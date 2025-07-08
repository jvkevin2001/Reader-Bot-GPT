# (Modelos Pydantic para request/response)
from pydantic import BaseModel

class ChatRequest(BaseModel):
    """
    Modelo para la solicitud de chat que envía el frontend.
    Define la estructura esperada del JSON en el cuerpo de la petición POST.
    """
    message: str
    conversation_id: str | None = None # Opcional, para futuras mejoras