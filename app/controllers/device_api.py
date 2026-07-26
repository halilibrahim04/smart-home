from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.dtos.device_dto import DeviceCreateRequestDTO, DeviceResponseDTO, DeviceSettingsUpdateDTO
from app.repositories.device_repository import DeviceRepository
from app.services.device_service import DeviceService
from app.core.auth_utils import decode_jwt

router = APIRouter(prefix="/api/devices", tags=["Devices"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user_id(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Eksik veya sahte Bearer Token. Güvenlik İhlali!")
    
    token = authorization.split(" ")[1]
    payload = decode_jwt(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Oturum süresi dolmuş veya şifre bozuk!")
    
    return payload["user_id"] # JWT Payload içindeki sub nesnesini direkt aldık

@router.post("", status_code=201)
def api_create_device(
    dto: DeviceCreateRequestDTO, 
    db: Session = Depends(get_db), 
    user_id: str = Depends(get_current_user_id)
):
    repo = DeviceRepository(db)
    service = DeviceService(repo)
    result = service.add_device(dto, user_id)
    
    if result["status_code"] != 201:
        raise HTTPException(status_code=result["status_code"], detail=result["message"])
        
    return {"data": result["data"]}

@router.get("", response_model=List[DeviceResponseDTO])
def api_fetch_devices(
    db: Session = Depends(get_db), 
    user_id: str = Depends(get_current_user_id)
):
    repo = DeviceRepository(db)
    service = DeviceService(repo)
    result = service.get_user_devices(user_id)
    return result["data"]

# KAVRAM: Güvenlik Loglarının Ucu Cihazlara Aittir (Nested Resource mantığı)
from app.entities.models import DeviceLog

@router.get("/logs")
def api_fetch_logs(db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    """
    Sisteme ait tüm karışık (Esnek JSONB) Log datalarını çeker. 
    İç içe OrderBy kullanarak zamana göre sondan sıralarız.
    """
    from app.entities.models import DeviceLog
    # Limitli (Son 15 log) performanslı çekim
    logs = db.query(DeviceLog).order_by(DeviceLog.created_at.desc()).limit(15).all()
    
    return [
        {
            "id": str(log.id),
            "device_id": str(log.device_id),
            "action_type": log.action_type,
            "details": log.details,
            "created_at": log.created_at.strftime("%Y-%m-%d %H:%M")
        } for log in logs
    ]

@router.patch("/{device_id}/toggle")
def api_toggle_device(
    device_id: str,
    db: Session = Depends(get_db), 
    user_id: str = Depends(get_current_user_id)
):
    repo = DeviceRepository(db)
    service = DeviceService(repo)
    result = service.toggle_device(device_id, user_id)
    
    if result["status_code"] != 200:
        raise HTTPException(status_code=result["status_code"], detail=result["message"])
        
    return {"data": result["data"]}

@router.patch("/{device_id}/settings")
def api_update_settings(
    device_id: str,
    payload: DeviceSettingsUpdateDTO,
    db: Session = Depends(get_db), 
    user_id: str = Depends(get_current_user_id)
):
    repo = DeviceRepository(db)
    service = DeviceService(repo)
    result = service.update_device_settings(device_id, payload.settings, user_id)
    
    if result["status_code"] != 200:
        raise HTTPException(status_code=result["status_code"], detail=result["message"])
        
    return {"data": result["data"]}
