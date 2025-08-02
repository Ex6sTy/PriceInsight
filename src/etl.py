import os
import sys
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from src.db import write_to_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

def load_data(input_path: str) -> pd.DataFrame:
    """Загружает данные из CSV или XLSX файла"""
    if not os.path.exists(input_path):
        logger.error(f"Файл не найден: {input_path}")
        raise FileNotFoundError(f"Файл не найден: {input_path}")
    if input_path.endswith(".xlsx"):
        df = pd.read_excel(input_path)
    else:
        df = pd.read_csv(input_path)
    logger.info("First 5 rows:\n%s", df.head())
    logger.info("Missing values per column:\n%s", df.isnull().sum())
    return df

def main(input_path: str, cleaned_path="data/cleaned.csv"):
    df = load_data(input_path)
    logger.info("Numeric columns stats:\n%s", df.describe())

    # Преобразуем price, count, add_cost в числа (если вдруг строка)
    for col in ["price", "count", "add_cost"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.to_csv(cleaned_path, index=False)
    logger.info(f"Данные сохранены в {cleaned_path}")

    # Записываем данные в БД
    write_to_db(df, table_name="sales")
    logger.info("Данные записаны в таблицу sales в БД")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Load and display data")
    parser.add_argument(
        "--input", required=True, help="Путь к файлу данных (csv или xlsx)"
    )
    args = parser.parse_args()
    main(args.input)
