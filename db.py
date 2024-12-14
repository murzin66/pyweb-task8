from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL для подключения к базе данных SQLite
DATABASE_URL = "sqlite:///./terms.db"

# Создание движка для подключения к базе данных
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создание базы для определения классов моделей
Base = declarative_base()

# Сессия для общения с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Модель термина, которая будет использоваться для сохранения данных в базе
class TermModel(Base):
    __tablename__ = "terms"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, unique=True, index=True)
    definition = Column(String)
    priority = Column(Integer)


# Функция для инициализации базы данных (создание таблиц)
def init_db():
    # Создание всех таблиц в базе данных
    Base.metadata.create_all(bind=engine)


# Функция для получения сессии для работы с базой данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
