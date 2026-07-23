def generate_jwt(user_id: str, role: str) -> str:
    # Sahte (Mock) bir JWT üretici.
    # Format: header.payload.signature
    return f"eyJhbGciOiJIUz.payload(user={user_id},role={role}).X9signature"

def decode_jwt(token: str) -> dict:
    # Mock Token Çözücü
    if not token or "signature" not in token:
        return None
    
    if "role=admin" in token:
        return {"user_id": "U01", "role": "admin"}
    elif "role=user" in token:
        return {"user_id": "U02", "role": "user"}
        
    return None
