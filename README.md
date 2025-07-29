# PriceInsight

## Описание

**PriceInsight** — сервис для прогнозирования цен на основе анализа исторических данных, объёма продаж, затрат на продвижение и цен конкурентов.

## Структура проекта

- `src/etl.py` — загрузка и очистка данных (csv/xlsx → cleaned.csv)
- `src/features.py` — генерация фичи mean_competitor_price (cleaned.csv → features.csv)
- `src/train.py` — обучение модели и сохранение (model.joblib)
- `src/api.py` — REST API (FastAPI) для получения предсказаний по новым данным
- `tests/` — автоматические тесты (pytest)
- `data/` — входные и промежуточные файлы данных

## Быстрый старт

### Установка зависимостей

```bash
python -m venv .venv
.venv\Scripts\activate         # Windows
# или
source .venv/bin/activate     # Linux/Mac
```

```bash
pip install -r requirements.txt
```
Запуск пайплайна
Загрузка и обработка данных

```bash
python src/etl.py --input data/csv_data.csv
```

### Генерация признаков

```bash
python src/features.py
```

### Обучение модели

```bash
python src/train.py
```

### Запуск API

```bash
uvicorn src.api:app --reload
Перейти на http://127.0.0.1:8000/docs для теста.
```

### Запуск автотестов
```bash
pytest
```

### Логирование
Все запросы к API логируются в консоль (с параметрами и результатом).

