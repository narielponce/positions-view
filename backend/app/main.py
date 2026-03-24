import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api import planos_router, puntos_router
from app.config import settings

app = FastAPI(title=settings.APP_NAME, redirect_slashes=False)

app.mount("/api/uploads", StaticFiles(directory="/app/uploads"), name="uploads")

UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.include_router(planos_router)
app.include_router(puntos_router)


@app.get("/uploads/{filename}")
async def get_upload(filename: str):
    filepath = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(404, "Archivo no encontrado")
    return FileResponse(filepath)


@app.post("/planos/{plano_id}/imagen")
async def upload_imagen(plano_id: int, file: UploadFile = File(...)):
    from app.database import SessionLocal
    from app.models import Plano
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Solo se permiten archivos de imagen")
    
    db = SessionLocal()
    try:
        plano = db.query(Plano).filter(Plano.id == plano_id).first()
        if not plano:
            raise HTTPException(404, "Plano no encontrado")
        
        ext = file.filename.split(".")[-1] if "." in file.filename else "png"
        filename = f"plano_{plano_id}.{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        
        with open(filepath, "wb") as f:
            content = await file.read()
            f.write(content)
        
        plano.imagen_url = f"/uploads/{filename}"
        db.commit()
        
        return {"imagen_url": plano.imagen_url}
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}
