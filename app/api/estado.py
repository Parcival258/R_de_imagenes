from fastapi import APIRouter

router = APIRouter(prefix="/estado", tags=["estado"])

@router.get("/")
def estado():
    return {"estado": "ok", "mensaje": "Microservicio funcionando"}
