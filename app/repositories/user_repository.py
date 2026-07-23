import time
from app.entities.user import UserEntity

class UserRepository:
    """
    KAVRAM #42: Repository - Sadece ve sadece veritabanıyla (PostgreSQL) konuşur.
    """
    def __init__(self):
        # Gerçek dünyada burada "psycopg2" veya "SQLAlchemy" ile 
        # DB connection URI'si (Host, Port, DB_Name) kullanılarak bağlantı (session) açılır.
        pass

    def find_user_by_email(self, email: str) -> UserEntity:
        """
        Gerçek SQL Sorgusu Karşılığı:
        SELECT * FROM users WHERE email = 'email';
        """
        # (SİMÜLASYON) PostgreSQL veritabanımızdaki 2 adet kayıtlı gerçek satır:
        mock_database_table = [
            UserEntity(user_id="U01", email="admin@sirket.com", hashed_password="hashed_123", role="admin"),
            UserEntity(user_id="U02", email="uye@sirket.com", hashed_password="hashed_123", role="user")
        ]
        
        # Ağ gecikmesi simülasyonu
        time.sleep(0.1) 
        
        for record in mock_database_table:
            if record.email == email:
                return record
                
        return None  # Veritabanında kayıt yoksa None döner
