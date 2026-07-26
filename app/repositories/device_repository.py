from sqlalchemy.orm import Session
from app.entities.models import Device

class DeviceRepository:
    """
    Sadece ve Sadece Veritabanından Cihaz (GET/POST) okur yazar.
    Dependency Injection ile 'Session' alır.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, user_id: str):
        # Sadece oturum açan kişinin (owner) cihazlarını PostgreSQL'den getirir
        return self.db.query(Device).filter(Device.owner_id == user_id).all()

    def create(self, name: str, device_type: str, owner_id: str, home_id: str = None) -> Device:
        # Eğlenceli bir simülasyon: Sahte IP/MAC ata
        import random
        fake_ip = f"192.168.1.{random.randint(20, 200)}"
        fake_mac = f"00:1B:44:11:3A:{random.randint(10, 99)}"
        
        new_device = Device(
            name=name, 
            device_type=device_type, 
            owner_id=owner_id,
            home_id=home_id if home_id else None,
            ip_address=fake_ip,
            mac_address=fake_mac,
            status="online"
        )
        self.db.add(new_device)
        self.db.commit()
        self.db.refresh(new_device) # PK/UUID'nin dolması için tazele
        
        return new_device

    def update_status(self, device_id: str, new_status: str):
        device = self.db.query(Device).filter(Device.id == device_id).first()
        if device:
            device.status = new_status
            self.db.commit()
            self.db.refresh(device)
        return device

    def update_settings(self, device_id: str, new_settings: dict):
        device = self.db.query(Device).filter(Device.id == device_id).first()
        if device:
            device.settings = new_settings
            self.db.commit()
            self.db.refresh(device)
        return device
