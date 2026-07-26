from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class DeviceCreateRequestDTO(BaseModel):
    """
    KAVRAM #37: Pydantic DTO
    Frontend'den gelen cihaz verilerini (Name, Type) otomatik denetler (Validasyon).
    """
    name: str
    device_type: str
    home_id: str # Mekansız cihaz olamaz. Zorunlu (Required) kılındı.

class DeviceResponseDTO(BaseModel):
    """
    Backend'den Frontend'e Dönen Veri Tipi.
    Config -> from_attributes = True özelliği, SQLAlchemy (ORM) Objesini doğrudan JSON'a çevirmeyi sağlar.
    """
    id: UUID
    name: str
    device_type: str
    status: str
    mac_address: Optional[str] = None
    ip_address: Optional[str] = None
    home_id: Optional[UUID] = None
    settings: dict = {}
    
    class Config:
        from_attributes = True

class DeviceSettingsUpdateDTO(BaseModel):
    settings: dict
