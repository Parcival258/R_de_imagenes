from fastapi import APIRouter, UploadFile, File
from app.servicios.servicio_ocr import ServicioOCR
from app.servicios.servicio_procesamiento import ServicioProcesamiento

router = APIRouter(prefix="/procesar", tags=["procesamiento"])

ocr = ServicioOCR()
procesador = ServicioProcesamiento()

@router.post("/")
async def procesar_comprobante(archivo: UploadFile = File(...)):
    contenido = await archivo.read()

    texto = ocr.extraer_texto(contenido)
    datos = procesador.procesar(texto)

    return {
        "tipo_comprobante": datos["tipo"],
        "texto_limpio": datos["texto_limpio"],
        "campos": datos["campos"]
    }
