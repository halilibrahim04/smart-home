from app.repositories.user_repository import UserRepository
from app.core.auth_utils import generate_jwt

class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        
    def login(self, email: str, plain_password: str, expected_role: str) -> dict:
        user = self.repository.find_user_by_email(email)
        
        if not user:
            return {"status_code": 404, "message": "Email adresi sistemde kayıtlı değil!"}
            
        if plain_password != user.password_hash:
            return {"status_code": 401, "message": "Hatalı parola girişi."}
            
        if user.role != expected_role:
            return {"status_code": 403, "message": f"Erişim yetkiniz {expected_role} paneli için geçersiz."}
            
        token = generate_jwt(user_id=str(user.id), role=user.role)
        return {"status_code": 200, "token": token}
