"""
Veritabanına İlk Açılış Test Verilerini (Seed) Doldurma Betiği
"""
from app.core.database import SessionLocal
from app.entities.models import User

def seed_data():
    db = SessionLocal()
    
    # Kullanıcı sayısını say (0 ise tamamen bomboş demektir)
    if db.query(User).count() == 0:
        print("[*] Veritabanı tamamen boş. Test kullanıcıları basılıyor...")
        
        admin = User(email="admin@sirket.com", password_hash="123456", role="admin")
        uye = User(email="uye@sirket.com", password_hash="123456", role="user")
        
        db.add(admin)
        db.add(uye)
        db.commit() # Verileri fiziken kaydet
        
        print("[+] Başarı: 'admin@sirket.com' (Yönetici) PostgreSQL tablona eklendi!")
        print("[+] Başarı: 'uye@sirket.com' (Üye) PostgreSQL tablona eklendi!")
    else:
        print("[-] PostgreSQL 'users' tablonuzda zaten veriler var. İşlem atlandı.")
        
    db.close()

if __name__ == "__main__":
    seed_data()
