from app.repositories.user_repository import UserRepository
from app.core.auth_utils import generate_jwt

class AuthService:
    """
    KAVRAM #41: Service - İş kurallarının yazıldığı yerdir.
    Controller'dan sadece ham (str) veriyi alır, DB'yi kontrol eder, ve sonucu döner.
    """
    def __init__(self, repository: UserRepository):
        self.repository = repository
        
    def login(self, email: str, plain_password: str, expected_role: str):
        # 1. DB'den kullanıcıyı çek (Repository üzerinden sorgula)
        user = self.repository.find_user_by_email(email)
        
        # 2. İş Kuralı: Kullanıcı DB'de var mı?
        if not user:
            return {"status_code": 404, "message": "Email adresi veritabanında bulunamadı!"}
            
        # 3. İş Kuralı: Şifre kontrolü
        # Gerçekte: bcrypt.checkpw(plain_password, user.hashed_password)
        if plain_password != "123456":
            return {"status_code": 401, "message": "Hatalı parola!"}
            
        # 4. İş Kuralı: Rol Doğrulaması
        if user.role != expected_role:
            return {"status_code": 403, "message": f"Erişim izniniz {expected_role} paneline yetmiyor."}
            
        # Her Şey Başarılı: Token Ver (Kavram #50)
        token = generate_jwt(user_id=user.user_id, role=user.role)
        return {"status_code": 200, "token": token}
