import pandas as pd

from src.etl import load_data, main


def test_load_data(tmp_path):
    file = tmp_path / "test.csv"
    file.write_text("price,count,add_cost,company,product\n10,1,2,A,X\n20,2,4,B,Y")
    df = load_data(str(file))
    assert not df.empty
    assert list(df.columns) == ["price", "count", "add_cost", "company", "product"]


def test_main(monkeypatch, tmp_path):
    # Создадим тестовый файл
    file = tmp_path / "test.csv"
    file.write_text("price,count,add_cost,company,product\n10,1,2,A,X\n20,2,4,B,Y")
    # Мокаем write_to_db, чтобы не писать реально в БД
    monkeypatch.setattr("src.db.write_to_db", lambda df, table_name=None: None)
    # Мокаем сохранение в CSV
    monkeypatch.setattr(pd.DataFrame, "to_csv", lambda self, path, index: None)
    main(str(file))
