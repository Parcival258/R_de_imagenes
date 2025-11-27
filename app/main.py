from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.estado import router as estado_router
from app.api.extraer import router as extraer_router
from app.api.procesar import router as procesar_router

app = FastAPI(title="Microservicio IA - Comprobantes")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------------

app.include_router(estado_router)
app.include_router(extraer_router)
app.include_router(procesar_router)
