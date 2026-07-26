from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

app = FastAPI(title="Smart Home API")

# KAVRAM #33: CORS: Frontend (Localhost TBD) ile Backend'in (8000) haberleşebilmesi için Güvenlik İzni
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_service = AuthService(UserRepository())

from app.controllers.device_api import router as device_router
app.include_router(device_router)

from app.controllers.home_api import router as home_router
app.include_router(home_router)

class LoginPayload(BaseModel):
    email: str
    password: str
    role: str

@app.post("/api/login")
def api_login(payload: LoginPayload):
    """
    GERÇEK DÜNYA NETWORK'ü (Kavram #36, #37, #45, #48, #50)
    Frontend'den Pydantic yardımıyla DTO verisi gelir ve Servis katmanına aktarılır.
    """
    result = auth_service.login(payload.email, payload.password, payload.role)
    
    if result.get("status_code") != 200:
        raise HTTPException(status_code=result["status_code"], detail=result.get("message"))
        
    return {"token": result.get("token")}

if __name__ == "__main__":
    print("Gerçek Backend Sunucusu (Uvicorn) Başlatılıyor...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
