import os
from sqlalchemy import Column, Date, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv


load_dotenv()

Base = declarative_base()

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=True)
    company = Column(String, nullable=False)
    product = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    add_cost = Column(Float, nullable=False)

class Feature(Base):
    __tablename__ = "features"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=True)
    company = Column(String, nullable=False)
    product = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    add_cost = Column(Float, nullable=False)
    mean_competitor_price = Column(Float, nullable=False)

class CompetitorPrice(Base):
    __tablename__ = "competitors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=True)
    competitor_name = Column(String, nullable=False)
    product = Column(String, nullable=False)
    price = Column(Float, nullable=False)

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=True)
    company = Column(String, nullable=False)
    product = Column(String, nullable=False)
    predicted_price = Column(Float, nullable=False)
    model_version = Column(String, nullable=False)

def get_engine():
    """
    Создает и возвращает SQLAlchemy Engine.
    Берет строку подключения из переменной окружения DATABASE_URL.
    Требует обязательной переменной среды!
    """
    url = os.getenv("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL не задан в переменных среды! См. .env.example")
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

def write_to_db(df, table_name="sales"):
    """
    Записывает DataFrame в указанную таблицу (по умолчанию 'sales').
    Если таблица существует — пересоздает ('replace').
    """
    engine = get_engine()
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)
