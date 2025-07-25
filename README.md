# PriceInsight

Приложение для прогнозирования цен на основе исторических данных продаж, затрат на продвижение и цен конкурентов.

## Структура проекта

- `data/` — директория для хранения исходных CSV-файлов и дампов базы.
- `src/` — исходники проекта:
  - `etl.py` — загрузка и первичная обработка данных.
  - `features.py` — генерация признаков.
  - `train.py` — обучение и валидация модели.
  - `api.py` — REST API для получения прогнозов.
  - `db.py` — взаимодействие с базой данных.
- `tests/` — тесты проекта.
- `requirements.txt` — зависимости Python.

## Установка

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/your-org/PriceInsight.git
   cd PriceInsight
   
2. Создать виртуальное окружение и установить зависимости:
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt\

