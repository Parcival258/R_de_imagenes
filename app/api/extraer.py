from fastapi import APIRouter, UploadFile, File
from app.servicios.servicio_ocr import ServicioOCR

router = APIRouter(prefix="/extraer", tags=["ocr"])

ocr = ServicioOCR()

@router.post("/")
async def extraer_informacion(archivo: UploadFile = File(...)):
    contenido = await archivo.read()
    resultado = ocr.extraer_texto(contenido)
    return {"texto": resultado}
