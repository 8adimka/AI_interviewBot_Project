import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bot.models.base import Base
from bot.config import Config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    engine = create_engine(Config.DATABASE_URL, echo=False, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
    logger.info("База данных успешно подключена.")
except Exception as e:
    logger.error(f"Ошибка подключения к БД: {e}")
    raise

def get_db():
    """Создает и управляет сессией базы данных."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()  # Откатываем транзакцию в случае ошибки
        logger.error(f"Ошибка работы с БД: {e}")
        raise
    finally:
        db.close()

def init_db():
    """Инициализирует базу данных и создает таблицы."""
    logger.info("Инициализация базы данных...")
    Base.metadata.create_all(bind=engine)
    logger.info("База данных готова.")
