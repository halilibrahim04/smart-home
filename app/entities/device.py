class Device:
    
    def __init__(self, name: str, device_type: str, ip_address: str):
        self.name = name                 
        self._type = device_type         
        self.__ip_address = ip_address   
        self.is_connected = False        

    def connect(self) -> str:
        self.is_connected = True
        return f"{self.name} connected via {self.__ip_address}."

    def disconnect(self) -> str:
        self.is_connected = False
        return f"{self.name} disconnected."
