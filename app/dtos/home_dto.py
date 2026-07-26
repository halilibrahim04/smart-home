from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class HomeCreateRequestDTO(BaseModel):
    name: str # Örn: "Yazlık Ev"
    location_city: str # Örn: "Antalya"

class HomeResponseDTO(BaseModel):
    id: UUID
    name: str
    location_city: str
    created_at: datetime
    
    # SQLAlchemy objesini otomatik okuması için (V2)
    model_config = ConfigDict(from_attributes=True)
