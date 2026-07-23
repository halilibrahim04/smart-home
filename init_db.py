"""
Veritabanı Tablolarını Gerçekten (Fiziksel Olarak) Oluşturma Betiği
Kullanımı: python init_db.py
"""

from app.core.database import engine, Base

# Tabloların engine'e bind edilmesi için sınıfların import edilmiş olması şarttır!
from app.entities.models import User, Home, Device, DeviceLog

def create_physical_tables():
    try:
        print("[*] SQLAlchemy Modelleri PostgreSQL sunucusuna aktarılıyor (Migration)...")
        # create_all metodu, tablolar DB'de yoksa yepyeni olarak yaratır.
        Base.metadata.create_all(bind=engine)
        print("[+] BAŞARILI! Tablolar veritabanına sorunsuz şekilde çizildi.")
        print("    Artık pgAdmin veya DBeaver'dan ER diyagramınızı görebilirsiniz.")
    except Exception as e:
        print("\n[!] HATA OLUŞTU!")
        print("Lütfen 'app/core/database.py' içindeki şifre ve DB adını KENDİ YEREL POSTGRESQL bilgilerinle güncellediğinden emin ol!")
        print("Detay:", e)

if __name__ == "__main__":
    create_physical_tables()
