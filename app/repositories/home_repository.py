from sqlalchemy.orm import Session
from app.entities.models import Home

class HomeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_user(self, owner_id: str):
        return self.db.query(Home).filter(Home.owner_id == owner_id).all()

    def create(self, name: str, location_city: str, owner_id: str) -> Home:
        new_home = Home(name=name, location_city=location_city, owner_id=owner_id)
        self.db.add(new_home)
        self.db.commit()
        self.db.refresh(new_home)
        return new_home
