import logging
from typing import Dict

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Проверка, что модель есть
import os
MODEL_PATH = "model.joblib"
if not os.path.exists(MODEL_PATH):
    logger.error(f"Файл модели не найден: {MODEL_PATH}")
    raise FileNotFoundError(f"Файл модели не найден: {MODEL_PATH}")

model = joblib.load(MODEL_PATH)

class PredictRequest(BaseModel):
    count: int
    add_cost: float
    mean_competitor_price: float

app = FastAPI(title="PriceInsight API", version="1.0.0")

@app.post("/predict/")
def predict_price(request: PredictRequest) -> Dict[str, float]:
    try:
        X = pd.DataFrame([request.model_dump()])
        price = model.predict(X)[0]
        logger.info(f"Prediction requested: {request.model_dump()} -> {price}")
        return {"predicted_price": round(float(price), 2)}
    except Exception as e:
        logger.error(f"Ошибка при предсказании: {e}")
        raise HTTPException(status_code=500, detail="Ошибка сервиса предсказаний")

@app.get("/health")
def health():
    return {"status": "ok"}

