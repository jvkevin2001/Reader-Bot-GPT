# (Punto de entrada de la aplicación FastAPI)
# backend/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware # 1. Importar el middleware de CORS
from app.api.endpoints import chat
from app.services.pdf_service import pdf_service
from pydantic import BaseModel

# --- Lógica del ciclo de vida (sin cambios) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando la aplicación...")
    pdf_path = "data/Accessible_Travel_Guide_Partial.pdf" 
    print(f"Cargando contexto desde: {pdf_path}")
    app.state.pdf_context = pdf_service.extract_text_from_pdf(pdf_path)
    print("Contexto del PDF cargado exitosamente.")
    yield
    print("Cerrando la aplicación...")
    app.state.pdf_context = None

# --- Creación de la instancia de la aplicación ---
app = FastAPI(
    title="Chatbot PDF Reader API",
    description="API para interactuar con un chatbot que lee documentos PDF.",
    version="0.1.0",
    lifespan=lifespan
)

# --- 2. CONFIGURACIÓN DE CORS ---
# Orígenes permitidos (la URL de tu frontend de React)
origins = [
    "http://localhost:5173",
    # Puedes añadir más orígenes si es necesario, como la URL de producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Permite los orígenes en la lista `origins`
    allow_credentials=True,
    allow_methods=["*"],        # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],        # Permite todos los encabezados
)

# --- Endpoints (sin cambios) ---
class HealthStatus(BaseModel):
    status: str

@app.get("/health", response_model=HealthStatus, tags=["Monitoring"])
def health_check():
    return {"status": "ok"}

app.include_router(chat.router, prefix="/api", tags=["Chat"])
