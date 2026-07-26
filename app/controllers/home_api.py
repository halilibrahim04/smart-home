from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.dtos.home_dto import HomeCreateRequestDTO, HomeResponseDTO
from app.repositories.home_repository import HomeRepository
from app.services.home_service import HomeService
from app.controllers.device_api import get_db, get_current_user_id

router = APIRouter(prefix="/api/homes", tags=["Homes"])

@router.post("", status_code=201)
def api_create_home(
    dto: HomeCreateRequestDTO, 
    db: Session = Depends(get_db), 
    user_id: str = Depends(get_current_user_id)
):
    repo = HomeRepository(db)
    service = HomeService(repo)
    result = service.add_home(dto, user_id)
    
    if result["status_code"] != 201:
        raise HTTPException(status_code=result["status_code"], detail=result["message"])
        
    return {"data": result["data"]}

@router.get("", response_model=List[HomeResponseDTO])
def api_fetch_homes(
    db: Session = Depends(get_db), 
    user_id: str = Depends(get_current_user_id)
):
    repo = HomeRepository(db)
    service = HomeService(repo)
    result = service.get_user_homes(user_id)
    return result["data"]
