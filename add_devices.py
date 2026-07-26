from app.core.database import SessionLocal
from app.entities.models import User, Device
import random

def seed_devices():
    db = SessionLocal()
    
    # Cihazların kimin üzerine ekleneceğini bul (Admin)
    admin = db.query(User).filter(User.email == "admin@sirket.com").first()
    
    if not admin:
        print("[-] Hata: 'admin@sirket.com' kullanıcısı bulunamadı!")
        db.close()
        return

    # Eklenecek örnek cihazlar
    devices_data = [
        {"name": "Ana Giriş Kamerası", "device_type": "Security"},
        {"name": "Salon Akıllı Termostatı", "device_type": "Climate"},
        {"name": "Mutfak Zemin Işıkları", "device_type": "Lighting"},
        {"name": "Arka Bahçe Harekete Duyarlı Kamera", "device_type": "Security"},
        {"name": "Ebeveyn Yatak Odası Kliması", "device_type": "Climate"}
    ]
    
    for dev in devices_data:
        fake_ip = f"192.168.1.{random.randint(20, 200)}"
        fake_mac = f"00:1B:44:11:3A:{random.randint(10, 99)}"
        new_device = Device(
            name=dev["name"], 
            device_type=dev["device_type"], 
            owner_id=admin.id,
            ip_address=fake_ip,
            mac_address=fake_mac,
            status=random.choice(["online", "online", "offline"]) # Bazen offline gelsin
        )
        db.add(new_device)
        print(f"[+] Veritabanına Eklendi: {dev['name']} ({fake_ip})")

    db.commit()
    print("\n🚀 Tüm harika cihazlar PostgreSQL'e kaydedildi! Tarayıcıda görebilirsin.")
    db.close()

if __name__ == "__main__":
    seed_devices()
