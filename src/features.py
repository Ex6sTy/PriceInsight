import logging

import pandas as pd

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def add_mean_competitor_price(df: pd.DataFrame) -> pd.DataFrame:
    sum_by_product = df.groupby("product")["price"].transform("sum")
    count_by_product = df.groupby("product")["price"].transform("count")
    sum_by_product_company = df.groupby(["product", "company"])["price"].transform(
        "sum"
    )
    count_by_product_company = df.groupby(["product", "company"])["price"].transform(
        "count"
    )
    df["mean_competitor_price"] = (sum_by_product - sum_by_product_company) / (
        count_by_product - count_by_product_company
    )
    # Если NaN (нет конкурентов), подставим среднее по всему датасету
    mean_price = df["price"].mean()
    df["mean_competitor_price"] = df["mean_competitor_price"].fillna(mean_price)
    return df


if __name__ == "__main__":
    df = pd.read_csv("data/cleaned.csv")
    logger.info("Загружены очищенные данные.")
    df = add_mean_competitor_price(df)
    logger.info("Фича mean_competitor_price рассчитана.")
    print(df[["company", "product", "price", "mean_competitor_price"]].head(10))
    df.to_csv("data/features.csv", index=False)
    logger.info("Файл с фичами сохранён в data/features.csv")

    # (По желанию) Сохраняем в БД
    try:
        from src.db import write_to_db

        write_to_db(df, table_name="features")
        logger.info("Данные с фичами записаны в БД (таблица features).")
    except ImportError:
        logger.warning("write_to_db не найден, пропускаем запись в БД.")
