from abc import ABC, abstractmethod

class INetworkConnectable(ABC):
    
    @abstractmethod
    def connect_to_network(self) -> bool:
        pass
