from abc import abstractmethod, ABC
from Src.settings import settings

class reporting(ABC):
    _settings : settings
    _data : dict
    _fields : list

    @abstractmethod
    def create(self, key:str) -> str:
        pass
    
    def __init__(self, settings_:settings, data_) -> None:
        self._settings = settings_
        self._data = data_

    @property         
    def data(self) -> dict:
        return self._data

    @property
    def fields(self) -> list:
        return self._fields
    
    @fields.setter
    def fields(self, val) -> list:
        self._fields = val