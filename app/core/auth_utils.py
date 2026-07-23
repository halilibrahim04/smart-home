import jwt
import time

SECRET_KEY = "SUPER_SECURE_KEY_123"

def generate_jwt(user_id: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "role": role,
        "exp": time.time() + 3600
    }
    # KAVRAM #50: Hiçbir simülasyon olmadan Python'ın native PyJWT modülüyle Cripto imzalama.
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"user_id": payload["sub"], "role": payload["role"]}
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
