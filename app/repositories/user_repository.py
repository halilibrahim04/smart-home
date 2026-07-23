from app.core.database import SessionLocal
from app.entities.models import User

class UserRepository:
    """
    KAVRAM #42: Gerçek PostgreSQL ile İletişim (SQLAlchemy ORM)
    Artık simülasyon bitti, tüm gücümüzle Native DB'ye bağlanıyoruz!
    """
    def __init__(self):
        # SQLAlchemy Veritabanı Oturumunu (Transaction Session) Aç
        self.db = SessionLocal()

    def find_user_by_email(self, email: str) -> User | None:
        """
        Arka planda dönen sihirli SQL Kodu: 
        SELECT * FROM users WHERE email = '...' LIMIT 1;
        """
        user = self.db.query(User).filter(User.email == email).first()
        return user
        
    def __del__(self):
        # İstek bitince bağlantıyı havuza (Sisteme) iade et
        self.db.close()
