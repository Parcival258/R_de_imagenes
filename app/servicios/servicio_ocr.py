import easyocr
import numpy as np
from PIL import Image
import io

class ServicioOCR:
    def __init__(self):
        self.reader = easyocr.Reader(['es'], gpu=False)

    def extraer_texto(self, imagen_bytes: bytes) -> str:
        try:
            img = Image.open(io.BytesIO(imagen_bytes)).convert("RGB")
            img_np = np.array(img)
            result = self.reader.readtext(img_np, detail=0, paragraph=True)
            return " ".join(result).lower()
        except Exception as e:
            raise ValueError(f"Error al extraer texto de la imagen: {str(e)}")