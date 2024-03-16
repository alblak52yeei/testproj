from Src.reference import reference
from datetime import datetime
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model
from Src.Models.unit_model import unit_model
from Src.exceptions import argument_exception

class storage_transaction_model(reference):
    __storage: storage_model
    __nomen: nomenclature_model
    __operation: bool
    __contes: int
    __unit: unit_model
    __period: datetime


    def __init__(self, storage: storage_model, nomen: nomenclature_model, operation: bool, countes: int, unit: unit_model, period: datetime,  name: str = ''):
        super().__init__(name)
        
        self.__storage = storage
        self.__nomen = nomen
        self.__operation = operation
        self.__contes = countes
        self.__unit = unit
        self.__period = period

    
    @property
    def name(self):
        return self.name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise argument_exception("Invalid name")
        
        self.__name = value

    def storage(self):
        return self.__storage

    def nomenculature(self) -> nomenclature_model:
        return self.__nomen

    def opearation(self):
        return self.__operation

    def counts(self):
        return self.__contes
    
    def unit(self):
        return self.__unit

    def period(self):
        return self.__period