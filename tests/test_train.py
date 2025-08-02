import pandas as pd

from src.train import main


def test_train_main(tmp_path, monkeypatch):
    # Генерируем минимальный features.csv
    df = pd.DataFrame(
        {
            "count": [1, 2, 3, 4],
            "add_cost": [10, 20, 30, 40],
            "mean_competitor_price": [100, 200, 300, 400],
            "price": [150, 250, 350, 450],
        }
    )
    path = tmp_path / "features.csv"
    df.to_csv(path, index=False)
    # Подменяем пути
    monkeypatch.setattr("src.train.main", lambda *a, **k: main(features_path=str(path)))
    main(
        features_path=str(path),
        model_path=str(tmp_path / "model.joblib"),
        metrics_path=str(tmp_path / "metrics.txt"),
    )
    # Проверяем что файл с моделью появился
    assert (tmp_path / "model.joblib").exists()
