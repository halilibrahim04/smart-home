from app.repositories.user_repository import UserRepository
from app.core.auth_utils import generate_jwt

class AuthService:
    """
    KAVRAM #41: İş(Business) Kuralları katmanı
    """
    def __init__(self, repository: UserRepository):
        self.repository = repository
        
    def login(self, email: str, plain_password: str, expected_role: str):
        # 1. DB'den gerçek model kullanıcıyı (User Class) çek
        user = self.repository.find_user_by_email(email)
        
        # 2. Kullanıcı Var mı?
        if not user:
            return {"status_code": 404, "message": "Email adresi PostgreSQL veritabanında bulunamadı!"}
            
        # 3. Şifre Doğrulama (Gerçek tabloda Hash tutulur, şu an test için şifreyle eşliyoruz)
        if plain_password != user.password_hash:
            return {"status_code": 401, "message": "Hatalı parola reddedildi!"}
            
        # 4. Yetki Doğrulaması (RBAC)
        if user.role != expected_role:
            return {"status_code": 403, "message": f"Bu hesabın yetkisi {expected_role} paneline yetmiyor."}
            
        # Başarılı: DB'deki native UUID formatındaki ID gönderilir!
        token = generate_jwt(user_id=str(user.id), role=user.role)
        return {"status_code": 200, "token": token}
