import os
import subprocess
import sys

import pandas as pd

from src.features import add_mean_competitor_price


def test_add_mean_competitor_price():
    df = pd.DataFrame(
        {
            "company": ["A", "B", "A", "B"],
            "product": ["X", "X", "Y", "Y"],
            "price": [100, 200, 300, 400],
            "count": [10, 20, 30, 40],
            "add_cost": [1, 2, 3, 4],
        }
    )
    out = add_mean_competitor_price(df)
    assert "mean_competitor_price" in out.columns


def test_features_main_block(tmp_path):
    # Создать data/ и cleaned.csv внутри tmp_path
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    cleaned_path = data_dir / "cleaned.csv"
    df = pd.DataFrame(
        {
            "company": ["A", "B"],
            "product": ["X", "X"],
            "price": [100, 200],
            "count": [10, 20],
            "add_cost": [1, 2],
        }
    )
    df.to_csv(cleaned_path, index=False)

    features_py = os.path.abspath("src/features.py")
    result = subprocess.run(
        [sys.executable, features_py],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    print(result.stderr)
    assert result.returncode == 0
    assert (data_dir / "features.csv").exists()
