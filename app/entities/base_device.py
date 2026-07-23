from abc import ABC, abstractmethod

class BaseDevice(ABC):
    
    def __init__(self, brand_name: str):
        self.__brand_name = brand_name
        self._is_active = False

    @property
    def brand_name(self) -> str:
        return self.__brand_name

    @abstractmethod
    def turn_on(self) -> str:
        pass
