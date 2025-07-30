import logging
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

def main(
    features_path="data/features.csv",
    model_path="model.joblib",
    metrics_path="metrics.txt",
):
    try:
        logger.info("Загрузка признаков из %s", features_path)
        df = pd.read_csv(features_path)

        features = ["count", "add_cost", "mean_competitor_price"]
        X = df[features]
        y = df["price"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = LinearRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        logger.info(f"RMSE на тестовой выборке: {rmse:.2f}")

        joblib.dump(model, model_path)
        logger.info("Модель сохранена в %s", model_path)

        with open(metrics_path, "w") as f:
            f.write(f"Test RMSE: {rmse:.2f}\n")
            f.write(f"Train size: {len(X_train)}, Test size: {len(X_test)}\n")
        logger.info("Метрика сохранена в %s", metrics_path)

    except Exception as e:
        logger.error(f"Ошибка при обучении модели: {e}", exc_info=True)

if __name__ == "__main__":
    main()
