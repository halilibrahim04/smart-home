from app.repositories.device_repository import DeviceRepository
from app.dtos.device_dto import DeviceCreateRequestDTO

class DeviceService:
    def __init__(self, repository: DeviceRepository):
        self.repo = repository

    def add_device(self, dto: DeviceCreateRequestDTO, owner_id: str):
        # Business Kuralları (Validasyon)
        if len(dto.name) < 3:
            return {"status_code": 400, "message": "Cihaz adı çok kısa. En az 3 harf olmalıdır."}
        
        valid_types = ["Security", "Climate", "Lighting", "Speaker", "Vacuum", "Switch"]
        if dto.device_type not in valid_types:
            return {"status_code": 400, "message": f"Belirtilen Tip Hatalı! (Şunlardan biri olmalı: {valid_types})"}

        device = self.repo.create(dto.name, dto.device_type, owner_id, home_id=dto.home_id)
        return {"status_code": 201, "data": device}

    def get_user_devices(self, user_id: str):
        devices = self.repo.get_all(user_id)
        return {"status_code": 200, "data": devices}

    def toggle_device(self, device_id: str, user_id: str):
        # 1. Cihazı bul ve güvenliğini sağla
        from app.entities.models import Device, DeviceLog
        device = self.repo.db.query(Device).filter(Device.id == device_id).first()
        
        if not device or str(device.owner_id) != user_id:
            return {"status_code": 403, "message": "Size ait olmayan bir cihaza müdahale edemezsiniz!"}
            
        # 2. Durumu Tersine Çevir
        new_status = "offline" if device.status == "online" else "online"
        updated_dev = self.repo.update_status(device_id, new_status)
        
        # 3. KAVRAM (EVENT SOURCING): Log (İz) Bırak!
        log = DeviceLog(
            device_id=device.id,
            action_type="POWER_TOGGLED",
            details={"action": f"Cihaz durumu değiştirildi: {new_status.upper()}", "triggered_by": "user_ui"}
        )
        self.repo.db.add(log)
        self.repo.db.commit()
        
        return {"status_code": 200, "data": updated_dev}

    def update_device_settings(self, device_id: str, settings: dict, user_id: str):
        from app.entities.models import Device, DeviceLog
        device = self.repo.db.query(Device).filter(Device.id == device_id).first()
        
        if not device or str(device.owner_id) != user_id:
            return {"status_code": 403, "message": "Size ait olmayan bir cihaza müdahale edemezsiniz!"}
            
        current_settings = device.settings or {}
        current_settings.update(settings)
        
        updated_dev = self.repo.update_settings(device_id, current_settings)
        
        log = DeviceLog(
            device_id=device.id,
            action_type="SETTINGS_CHANGED",
            details={"settings": current_settings, "triggered_by": "user_ui"}
        )
        self.repo.db.add(log)
        self.repo.db.commit()
        
        return {"status_code": 200, "data": updated_dev}
