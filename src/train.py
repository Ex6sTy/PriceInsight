import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib
import numpy as np


def main():
    # 1. Загружаем фичи
    df = pd.read_csv('data/features.csv')

    # 2. Выделяем признаки и целевую переменную
    features = ['count', 'add_cost', 'mean_competitor_price']
    X = df[features]
    y = df['price']

    # 3. Делим на train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 4. Обучаем модель
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 5. Предсказываем и оцениваем RMSE
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"RMSE на тестовой выборке: {rmse:.2f}")

    # 6. Сохраняем модель
    joblib.dump(model, 'model.joblib')
    print("Модель сохранена в model.joblib")


if __name__ == '__main__':
    main()
