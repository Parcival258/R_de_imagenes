from fastapi import APIRouter, UploadFile, File
from app.servicios.servicio_ocr import ServicioOCR

router = APIRouter(prefix="/extraer", tags=["ocr"])

ocr = ServicioOCR()

@router.post("/")
async def extraer_informacion(archivo: UploadFile = File(...)):
    try:
        contenido = await archivo.read()
        resultado = ocr.extraer_texto(contenido)
        return {"texto": resultado, "exitoso": True}
    except ValueError as e:
        return {"exitoso": False, "error": str(e)}, 400
    except Exception as e:
        return {"exitoso": False, "error": f"Error inesperado: {str(e)}"}, 500
