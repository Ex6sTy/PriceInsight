import pandas as pd
from src.train import main as train_main

def test_train_pipeline(tmp_path):
    # Копируем features.csv в tmp_path (или делаем небольшой df)
    df = pd.DataFrame({
        'count': [10, 20],
        'add_cost': [100, 200],
        'mean_competitor_price': [50000, 60000],
        'price': [55000, 62000],
    })
    test_file = tmp_path / "features.csv"
    df.to_csv(test_file, index=False)

    # Переопределим путь к features.csv (переопределить код, если нужно)
    # Например, модифицировать train.py под путь из параметра (не критично для демонстрации)
