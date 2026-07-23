from app.entities.base_device import BaseDevice
from app.entities.interfaces import INetworkConnectable

class SmartCamera(BaseDevice, INetworkConnectable):
    
    def __init__(self, brand_name: str, resolution: str):
        super().__init__(brand_name)
        self.resolution = resolution

    def turn_on(self) -> str:
        self._is_active = True
        return f"{self.brand_name} (Camera - {self.resolution}) is now capturing video."

    def connect_to_network(self) -> bool:
        # Gerçek dünyada burada WiFi/Ethernet protokolleri yer alır
        return True
