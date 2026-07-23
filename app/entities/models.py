import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID # Native Postgres tipleri (Kurumsal Kalite)
from sqlalchemy.orm import relationship

from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    # Otomatik artan zayıf id'ler yerine siber güvenli UUID (V4) kullanımı
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user") # 'admin' veya 'user'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 1'den Çoğa İlişkiler (One-to-Many Relationships)
    homes = relationship("Home", back_populates="owner", cascade="all, delete-orphan")
    devices = relationship("Device", back_populates="owner", cascade="all, delete-orphan")


class Home(Base):
    """
    Onaylanan tasarım gereği: Her kullanıcının birden fazla lokasyonu
    (Örn: Yazlık Ev, Merkez Ofis) olabilir konsepti.
    """
    __tablename__ = "homes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    location_city = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="homes")
    devices = relationship("Device", back_populates="home")


class Device(Base):
    __tablename__ = "devices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    home_id = Column(UUID(as_uuid=True), ForeignKey("homes.id", ondelete="SET NULL"), nullable=True)
    
    name = Column(String, nullable=False)
    device_type = Column(String, nullable=False) # Security, Climate, Lighting
    mac_address = Column(String, unique=True)
    ip_address = Column(String)
    status = Column(String, default="offline")
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="devices")
    home = relationship("Home", back_populates="devices")
    logs = relationship("DeviceLog", back_populates="device", cascade="all, delete-orphan")


class DeviceLog(Base):
    """
    Ekstrem Veri Modelleme: Cihaz hareketlerini MySQL mantığı gibi sütunlara bölmek
    yerine PostgreSQL'in inanılmaz hızlı 'JSONB' kolon teknolojisiyle tuttuk.
    """
    __tablename__ = "device_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id", ondelete="CASCADE"), nullable=False)
    action_type = Column(String, nullable=False)
    details = Column(JSONB) # Modern NoSQL ve SQL Karşımı Esneklik
    created_at = Column(DateTime, default=datetime.utcnow)

    device = relationship("Device", back_populates="logs")
