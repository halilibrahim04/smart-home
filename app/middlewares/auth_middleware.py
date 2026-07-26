from app.core.auth_utils import decode_jwt

class AuthMiddleware:
    
    def process_request(self, request: dict, required_role: str = None) -> dict:
        
        token = request.get("headers", {}).get("Authorization")
        if not token:
            return {"status_code": 401, "message": "Unauthorized - Lütfen Giriş Yapın."}
        
        # Token Geçerlilik Kontrolü
        user_data = decode_jwt(token)
        if not user_data:
            return {"status_code": 401, "message": "Unauthorized - Geçersiz Token!"}
            
        user_role = user_data.get("role")
        if required_role and user_role != required_role:
            return {"status_code": 403, "message": f"Forbidden - Sadece '{required_role}' rolü erişebilir."}
        
        return {"status_code": 200, "message": "OK", "user": user_data}
