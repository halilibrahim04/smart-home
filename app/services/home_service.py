from app.repositories.home_repository import HomeRepository
from app.dtos.home_dto import HomeCreateRequestDTO

class HomeService:
    def __init__(self, repository: HomeRepository):
        self.repo = repository

    def add_home(self, dto: HomeCreateRequestDTO, owner_id: str):
        # Güvenlik Kuralları (Mekan Adı Validasyonu)
        if len(dto.name) < 3:
            return {"status_code": 400, "message": "Mekan adı çok kısa (En az 3 karakter olmalı)."}
        
        home = self.repo.create(name=dto.name, location_city=dto.location_city, owner_id=owner_id)
        return {"status_code": 201, "data": home}

    def get_user_homes(self, user_id: str):
        homes = self.repo.get_all_by_user(user_id)
        return {"status_code": 200, "data": homes}
