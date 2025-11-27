import re

# ==========================================
# 🔥 Conversor de fechas a ISO (YYYY-MM-DD)
# ==========================================
def convertir_a_fecha_iso(texto_fecha: str):
    meses = {
        "enero": "01", "febrero": "02", "marzo": "03",
        "abril": "04", "mayo": "05", "junio": "06",
        "julio": "07", "agosto": "08", "septiembre": "09",
        "octubre": "10", "noviembre": "11", "diciembre": "12",
        "ene": "01", "feb": "02", "mar": "03", "abr": "04",
        "may": "05", "jun": "06", "jul": "07", "ago": "08",
        "sep": "09", "oct": "10", "nov": "11", "dic": "12"
    }

    texto_fecha = texto_fecha.lower().strip()
    partes = texto_fecha.split()

    # Formato NEQUI: 20 de noviembre de 2025
    if "de" in partes:
        dia = partes[0]
        mes = meses.get(partes[2], "01")
        anio = partes[-1]
        return f"{anio}-{mes}-{dia.zfill(2)}"

    # Formato corto: 18 nov 2025
    if len(partes) == 3:
        dia, mes_txt, anio = partes
        mes = meses.get(mes_txt, "01")
        return f"{anio}-{mes}-{dia.zfill(2)}"

    return texto_fecha


# ==========================================
# 🔥 SERVICIO PRINCIPAL
# ==========================================
class ServicioProcesamiento:
    def limpiar_texto(self, texto: str):
        texto = texto.replace("\n", " ").lower()
        texto = re.sub(r"\s+", " ", texto)
        return texto.strip()

    def detectar_tipo(self, texto_limpio: str):
        # Bancolombia
        if "transferencia exitosa" in texto_limpio:
            return "bancolombia"
        if "comprobante no" in texto_limpio:
            return "bancolombia"
        if "producto destino" in texto_limpio:
            return "bancolombia"

        # Nequi
        if "nequi" in texto_limpio:
            return "nequi"
        if "envío realizado" in texto_limpio:
            return "nequi"
        if "detalle del movimiento" in texto_limpio:
            return "nequi"

        # Otros
        if "daviplata" in texto_limpio or "davivienda" in texto_limpio:
            return "daviplata"
        if "bbva" in texto_limpio:
            return "bbva"
        if "efectivo" in texto_limpio:
            return "efectivo"

        return "desconocido"

    def extraer_campos(self, texto_limpio: str):
        campos = {}

        # 1) VALOR
        valor = re.search(
            r"\$\s*([0-9]{1,3}(?:[.,]\d{3})+|\d+)",
            texto_limpio
        )
        if valor:
            campos["valor"] = valor.group(1)

        # 2) FECHA (Nequi y Bancolombia)
        fecha_larga = re.search(
            r"(\d{1,2}\s+de\s+[a-záéíóúñ]+(?:\s+de)?\s+\d{4})",
            texto_limpio
        )
        if fecha_larga:
            campos["fecha"] = convertir_a_fecha_iso(fecha_larga.group(1))
        else:
            fecha_corta = re.search(
                r"(\d{1,2}\s+[a-zA-Z]{3,}\s+\d{4})",
                texto_limpio
            )
            if fecha_corta:
                campos["fecha"] = convertir_a_fecha_iso(fecha_corta.group(1))

        # 3) ID TRANSACCIÓN (solo Bancolombia)
        transaccion = re.search(
            r"(?:comprobante no\.?|id transacci[oó]n)\s*[:\-]?\s*(\w+)",
            texto_limpio
        )
        if transaccion:
            campos["id_transaccion"] = transaccion.group(1)

        # 4) REFERENCIA (Nequi)
        referencia = re.search(
            r"referencia\s*([a-zA-Z0-9]+)",
            texto_limpio
        )
        if referencia:
            campos["referencia"] = referencia.group(1)

        return campos

    def procesar(self, texto: str):
        texto_limpio = self.limpiar_texto(texto)
        tipo = self.detectar_tipo(texto_limpio)
        campos = self.extraer_campos(texto_limpio)

        return {
            "tipo": tipo,
            "texto_limpio": texto_limpio,
            "campos": campos
        }
