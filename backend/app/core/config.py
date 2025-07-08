# (Gestión de variables de entorno, como la API Key)
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Carga las variables de entorno desde un archivo .env
# Esto es útil para el desarrollo local.
load_dotenv()

class Settings(BaseSettings):
    """
    Clase para gestionar la configuración de la aplicación.
    Lee las variables de entorno. Pydantic se encarga de la validación.
    """
    # OPENAI_API_KEY es la variable que buscará en el entorno o en el archivo .env
    OPENAI_API_KEY: str

    class Config:
        # Esto permite que Pydantic lea desde un archivo .env si está presente
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Creamos una instancia de la configuración que será importada
# por otros módulos de la aplicación.
settings = Settings()
