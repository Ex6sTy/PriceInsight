from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


# Загружаем модель (путь к model.joblib)
model = joblib.load('model.joblib')

# Описываем структуру запроса
class PredictRequest(BaseModel):
    count: int
    add_cost: float
    mean_competitor_price: float

app = FastAPI()

@app.post("/predict/")
def predict_price(request: PredictRequest):
    X = pd.DataFrame([request.dict()])
    price = model.predict(X)[0]
    logger.info(f"Prediction requested: {request.dict()} -> {price}")
    return {"predicted_price": round(float(price), 2)}

