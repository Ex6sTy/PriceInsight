from src.db import get_engine, init_db


def test_init_db():
    engine = get_engine()
    assert engine is not None
    # Проверяем, что таблицы создаются без ошибки
    init_db()
