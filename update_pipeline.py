import logging
import subprocess
import sys
import time
from datetime import datetime

import schedule

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

PYTHON = sys.executable  # всегда активный python в venv


def run_step(cmd, step_name):
    try:
        logger.info(f"Запуск этапа: {step_name}")
        subprocess.run(cmd, check=True)
        logger.info(f"Этап '{step_name}' завершён успешно.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Ошибка на этапе '{step_name}': {e}")
        raise


def run_pipeline():
    start_time = datetime.now()
    logger.info(f"Запуск пайплайна ({start_time.strftime('%Y-%m-%d %H:%M:%S')})")
    try:
        run_step(
            [PYTHON, "src/etl.py", "--input", "data/csv_data.csv"],
            "Загрузка и обработка данных",
        )
        run_step([PYTHON, "src/features.py"], "Генерация признаков")
        run_step([PYTHON, "src/train.py"], "Обучение модели")
        logger.info("Пайплайн обновлён успешно!")
    except Exception as e:
        logger.error(f"Пайплайн завершился с ошибкой: {e}")
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    logger.info(f"Общее время выполнения: {duration:.2f} секунд.")


def schedule_mode():
    logger.info("Переходим в режим расписания: запуск каждый день в 02:00.")
    schedule.every().day.at("02:00").do(run_pipeline)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Автоматизация ML-пайплайна")
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Запускать по расписанию (ежедневно в 02:00)",
    )
    args = parser.parse_args()

    if args.schedule:
        schedule_mode()
    else:
        run_pipeline()
