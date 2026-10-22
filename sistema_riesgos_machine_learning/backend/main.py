from pathlib import Path
from typing import Literal
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "model" / "random_forest.joblib"
app = FastAPI(title="Clasificador de Riesgo de Activos", version="1.0.0",
              description="Prototipo académico con datos sintéticos; no sustituye una evaluación formal.")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=False,
    allow_methods=["*"], allow_headers=["*"]
)
model = None

class AssetInput(BaseModel):
    asset_type: Literal["Base de datos", "Servidor", "Aplicación", "Equipo", "Documento", "Red"]
    confidentiality: int = Field(ge=1, le=5, description="1=baja, 5=muy alta")
    integrity: int = Field(ge=1, le=5)
    availability: int = Field(ge=1, le=5)
    threat_exposure: int = Field(ge=1, le=5)
    vulnerability_count: int = Field(ge=0, le=8)
    control_maturity: int = Field(ge=1, le=5, description="1=incipiente, 5=robusta")
    internet_exposed: bool
    personal_data: bool
    backup_quality: int = Field(ge=1, le=5)

@app.on_event("startup")
def load_model():
    global model
    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)

@app.get("/api/health")
def health():
    return {"status": "ok", "model_loaded": model is not None,
            "data_notice": "Prototipo académico entrenado con datos sintéticos."}

@app.post("/api/predict")
def predict(asset: AssetInput):
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible. Ejecuta primero src/train_model.py.")
    try:
        row = pd.DataFrame([{
            **asset.model_dump(),
            "internet_exposed": int(asset.internet_exposed),
            "personal_data": int(asset.personal_data)
        }])
        prediction = str(model.predict(row)[0])
        probabilities = model.predict_proba(row)[0]
        classes = model.named_steps["classifier"].classes_
        scores = {str(c): round(float(p), 4) for c, p in zip(classes, probabilities)}
        return {
            "predicted_risk": prediction,
            "class_probabilities": scores,
            "notice": "Estimación experimental basada en datos sintéticos; requiere validación con datos reales."
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"No se pudo procesar la entrada: {exc}")
