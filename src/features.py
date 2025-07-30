import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
import pandas as pd
from src.db import write_to_db


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

def add_mean_competitor_price(df: pd.DataFrame) -> pd.DataFrame:
    sum_by_product = df.groupby("product")["price"].transform("sum")
    count_by_product = df.groupby("product")["price"].transform("count")
    sum_by_product_company = df.groupby(["product", "company"])["price"].transform("sum")
    count_by_product_company = df.groupby(["product", "company"])["price"].transform("count")
    df["mean_competitor_price"] = (sum_by_product - sum_by_product_company) / (
        count_by_product - count_by_product_company
    )
    # Если NaN (нет конкурентов), подставим среднее по всему датасету
    mean_price = df["price"].mean()
    df["mean_competitor_price"] = df["mean_competitor_price"].fillna(mean_price)
    return df

def build_features(
    cleaned_path="data/cleaned.csv", features_path="data/features.csv", table_name="features"
):
    """
    Генерирует признаки для ML-модели, сохраняет в CSV и в базу данных.
    """
    df = pd.read_csv(cleaned_path)
    logger.info("Загружены очищенные данные.")
    df = add_mean_competitor_price(df)
    logger.info("Фича mean_competitor_price рассчитана.")
    logger.info("\n%s", df[["company", "product", "price", "mean_competitor_price"]].head(10))
    df.to_csv(features_path, index=False)
    logger.info(f"Файл с фичами сохранён в {features_path}")
    write_to_db(df, table_name=table_name)
    logger.info(f"Данные с фичами записаны в БД (таблица {table_name}).")

if __name__ == "__main__":
    build_features()
