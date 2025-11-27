from fastapi import APIRouter, UploadFile, File
from app.servicios.servicio_ocr import ServicioOCR
from app.servicios.servicio_procesamiento import ServicioProcesamiento

router = APIRouter(prefix="/procesar", tags=["procesamiento"])

ocr = ServicioOCR()
procesador = ServicioProcesamiento()

@router.post("/")
async def procesar_comprobante(archivo: UploadFile = File(...)):
    try:
        contenido = await archivo.read()
        
        texto = ocr.extraer_texto(contenido)
        datos = procesador.procesar(texto)
        
        return {
            "exitoso": True,
            "tipo_comprobante": datos["tipo"],
            "texto_limpio": datos["texto_limpio"],
            "campos": datos["campos"]
        }
    except ValueError as e:
        return {"exitoso": False, "error": str(e)}, 400
    except Exception as e:
        return {"exitoso": False, "error": f"Error al procesar el comprobante: {str(e)}"}, 500
