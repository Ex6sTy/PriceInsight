import os
import sys
import pandas as pd
from src.db import write_to_db


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def load_data(input_path: str):
    """Загружает данные из csv или xlsx"""
    if input_path.endswith(".xlsx"):
        df = pd.read_excel(input_path)
    else:
        df = pd.read_csv(input_path)
    print("First 5 rows:")
    print(df.head())
    print("\nMissing values per column:")
    print(df.isnull().sum())
    return df


def main(input_path: str):
    df = load_data(input_path)

    print("\nNumeric columns stats:")
    print(df.describe())

    # Преобразуем price, count, add_cost в числа (если вдруг строка)
    for col in ["price", "count", "add_cost"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.to_csv("data/cleaned.csv", index=False)
    print("\nДанные сохранены в data/cleaned.csv")

    # Записываем данные в БД
    write_to_db(df, table_name="sales")
    print("Данные записаны в БД")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Load and display data")
    parser.add_argument(
        "--input", required=True, help="Путь к файлу данных (csv или xlsx)"
    )
    args = parser.parse_args()
    main(args.input)
