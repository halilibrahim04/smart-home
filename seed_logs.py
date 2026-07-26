from app.core.database import SessionLocal
from app.entities.models import Device, DeviceLog
import random

def seed_logs():
    db = SessionLocal()
    devices = db.query(Device).all()
    
    if not devices:
        print("Hata: Sistemde cihaz yok. Log eklenecek hedef cihaz bulunamadı!")
        return

    # Random cihazlar seçip test logları basıyoruz
    sample_device = devices[0]
    
    logs_to_insert = [
        DeviceLog(device_id=sample_device.id, action_type="CONNECTION_LOST", details={"error": "timeout", "ping": "999ms"}),
        DeviceLog(device_id=sample_device.id, action_type="UNAUTHORIZED_ACCESS", details={"ip": f"45.22.19.{random.randint(1,250)}", "attempt": 3}),
        DeviceLog(device_id=sample_device.id, action_type="FIRMWARE_UPDATE", details={"version": "v2.1", "status": "success"})
    ]
    
    db.add_all(logs_to_insert)
    db.commit()
    print("[+] Şık JSONB test güvenlik logları başarıyla eklendi!")
    db.close()

if __name__ == "__main__":
    seed_logs()
