from app.entities.smart_camera import SmartCamera
from app.services.logger_service import LoggerService

class CameraManager:
    
    # LoggerService buraya "Inject" ediliyor (Dependency Injection)
    def __init__(self, logger: LoggerService):
        self.logger = logger
        
    def setup_camera(self, camera: SmartCamera):
        self.logger.log(f"Setup started for: {camera.brand_name}")
        
        status = camera.turn_on()
        network_ok = camera.connect_to_network()
        
        if network_ok:
            self.logger.log(f"Success: {status}")
        else:
            self.logger.log("Fail: Network unreachable.")
