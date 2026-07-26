from app.core.database import SessionLocal
from app.entities.models import User

class UserRepository:
    def __init__(self):
        self.db = SessionLocal()

    def find_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()
        
    def __del__(self):
        self.db.close()
