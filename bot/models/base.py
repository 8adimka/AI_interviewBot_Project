from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Создаем базовый класс для всех моделей
Base = declarative_base()

