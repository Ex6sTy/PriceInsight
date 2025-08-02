import logging
import subprocess
import sys
import time
from datetime import datetime
import schedule

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

PYTHON = sys.executable  # Активный Python из venv

INPUT_PATH = "data/csv_data.csv"  # <- указываем только CSV!

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
    success = True
    try:
        run_step([PYTHON, "src/etl.py", "--input", INPUT_PATH], "Загрузка и обработка данных")
        run_step([PYTHON, "src/features.py"], "Генерация признаков")
        run_step([PYTHON, "src/train.py"], "Обучение модели")
        logger.info("Пайплайн обновлён успешно!")
    except Exception as e:
        logger.error(f"Пайплайн завершился с ошибкой: {e}")
        success = False
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    logger.info(f"Общее время выполнения: {duration:.2f} секунд.")
    if success:
        logger.info("Все этапы завершены без ошибок ✅")
    else:
        logger.info("Были ошибки при выполнении пайплайна ❌")

def schedule_mode(schedule_time="02:00"):
    logger.info(f"Переходим в режим расписания: запуск каждый день в {schedule_time}.")
    schedule.every().day.at(schedule_time).do(run_pipeline)
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Планировщик остановлен пользователем.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Автоматизация ML-пайплайна")
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Запускать по расписанию (ежедневно в 02:00)",
    )
    parser.add_argument(
        "--time",
        type=str,
        default="02:00",
        help="Время ежедневного запуска в формате HH:MM (по умолчанию 02:00)",
    )
    args = parser.parse_args()

    if args.schedule:
        schedule_mode(schedule_time=args.time)
    else:
        run_pipeline()
