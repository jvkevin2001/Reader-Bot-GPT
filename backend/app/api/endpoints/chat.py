# (Endpoint /chat y /health)
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from app.models.schemas import ChatRequest
from app.services.chat_service import chat_service, ChatService

# El router nos permite agrupar rutas y luego incluirlas en la app principal.
router = APIRouter()

@router.post("/chat")
async def chat_endpoint(request: Request, chat_request: ChatRequest):
    """
    Endpoint para recibir mensajes de chat y devolver una respuesta en streaming.
    
    Utiliza Server-Sent Events (SSE) para enviar la respuesta de la IA en tiempo real.
    """
    # Obtenemos el contexto del PDF que cargamos al iniciar la aplicación.
    # `request.app.state.pdf_context` es la forma de acceder a variables
    # del ciclo de vida de la aplicación en FastAPI.
    pdf_context = request.app.state.pdf_context

    # Llamamos al servicio de chat, que nos devuelve un generador (stream).
    response_generator = chat_service.send_message_stream(
        user_message=chat_request.message,
        pdf_context=pdf_context
    )
    
    # StreamingResponse es la magia de FastAPI para manejar respuestas en tiempo real.
    # Envuelve nuestro generador y lo envía al cliente fragmento por fragmento.
    return StreamingResponse(response_generator, media_type="text/event-stream")

