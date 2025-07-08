# (Lógica para cargar y procesar el PDF)
import PyPDF2
from fastapi import HTTPException

class PDFService:
    """
    Servicio para manejar operaciones relacionadas con archivos PDF.
    """
    def extract_text_from_pdf(self, file_path: str) -> str:
        """
        Extrae todo el texto de un archivo PDF.

        Args:
            file_path: La ruta al archivo PDF.

        Returns:
            Una cadena de texto con el contenido completo del PDF.
        
        Raises:
            HTTPException: Si el archivo no se encuentra o no se puede procesar.
        """
        try:
            with open(file_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                if not text:
                    raise HTTPException(status_code=500, detail="No se pudo extraer texto del PDF. El archivo podría estar vacío o ser una imagen.")

                return text
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail=f"Archivo PDF no encontrado en la ruta: {file_path}")
        except Exception as e:
            # Captura otras posibles excepciones de PyPDF2
            raise HTTPException(status_code=500, detail=f"Error al procesar el archivo PDF: {e}")

# Creamos una instancia del servicio para que sea fácil de importar y usar
pdf_service = PDFService()
