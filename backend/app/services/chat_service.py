# (Lógica de negocio del chat, comunicación con OpenAI)
from openai import OpenAI
from fastapi import HTTPException
from app.core.config import settings

class ChatService:
    """
    Servicio para manejar la lógica de la conversación con la IA.
    """
    def __init__(self):
        # Inicializa el cliente de OpenAI con la API Key de la configuración.
        # Si la clave no está presente, fallará al iniciar, lo cual es bueno
        # para detectar errores de configuración temprano.
        try:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        except Exception as e:
            # Esto ayuda a dar un error más claro si la API Key no está configurada.
            raise RuntimeError(f"No se pudo inicializar el cliente de OpenAI. ¿Configuraste la OPENAI_API_KEY? Error: {e}")

    def send_message_stream(self, user_message: str, pdf_context: str):
        """
        Envía un mensaje a OpenAI y devuelve la respuesta como un stream (generador).

        Args:
            user_message: El mensaje enviado por el usuario.
            pdf_context: El texto extraído del PDF que sirve como contexto.

        Yields:
            str: Fragmentos (chunks) de la respuesta de la IA.
        """
        system_prompt = f"""
        Eres un asistente experto y servicial. Tu tarea es responder preguntas basándote únicamente
        en el siguiente contexto extraído de un documento PDF. Sé conciso y preciso.
        Si la respuesta no se encuentra en el contexto, di amablemente que no puedes responder
        con la información proporcionada. No inventes información.

        Contexto del PDF:
        ---
        {pdf_context}
        ---
        """

        try:
            # Realiza la llamada a la API de OpenAI con streaming habilitado
            stream = self.client.chat.completions.create(
                model="gpt-4",  # Puedes cambiar el modelo si lo deseas (ej. "gpt-3.5-turbo")
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                stream=True,  # ¡Esto es clave para el streaming!
            )
            
            # Itera sobre los fragmentos del stream y los devuelve uno por uno
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content is not None:
                    yield content

        except Exception as e:
            print(f"Error al comunicarse con la API de OpenAI: {e}")
            raise HTTPException(status_code=500, detail="Error al procesar la solicitud con la IA.")

# Creamos una instancia única del servicio
chat_service = ChatService()