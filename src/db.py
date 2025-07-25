import os
from sqlalchemy import Column, Integer, Float, String, Date, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    company = Column(String, nullable=False)
    product = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    add_cost = Column(Float, nullable=False)

class CompetitorPrice(Base):
    __tablename__ = 'competitors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    competitor_name = Column(String, nullable=False)
    product = Column(String, nullable=False)
    price = Column(Float, nullable=False)

class Prediction(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    company = Column(String, nullable=False)
    product = Column(String, nullable=False)
    predicted_price = Column(Float, nullable=False)
    model_version = Column(String, nullable=False)


def get_engine():
    """
    Создает и возвращает SQLAlchemy Engine.
    Берет строку подключения из переменной окружения DATABASE_URL.
    Для локальной разработки по умолчанию используется SQLite-файл `priceinsight.db`.
    """
    default_url = 'sqlite:///priceinsight.db'
    url = os.getenv('DATABASE_URL', default_url)
    engine = create_engine(url, echo=False)
    return engine


def init_db():
    """
    Создает все таблицы в базе данных, описанные в моделях.
    """
    engine = get_engine()
    Base.metadata.create_all(engine)
    return engine


def get_session():
    """
    Возвращает сессию SQLAlchemy для работы с ORM.
    """
    engine = get_engine()
    return sessionmaker(bind=engine)()