from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:halil123@localhost:5432/smarthome"

# SQLAlchemy Motoru (Bağlantı Havuzu)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Gelişmiş veritabanı oturum (transaction) yöneticisi
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tablo sınıflarımızın türetileceği (Miras alacağı) Temel Sınıf
Base = declarative_base()
