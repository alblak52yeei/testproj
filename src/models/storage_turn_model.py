from Src.reference import reference
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model
from Src.Models.unit_model import unit_model

class storage_turn_model(reference):
    __storage: storage_model
    __remains: int
    __nomen: nomenclature_model
    __unit: unit_model


    def __init__(self, storage_: storage_model, remains: int,
                nomen: nomenclature_model, unit: unit_model, name: str = ''):
        super().__init__(name)
        self.__storage = storage_
        self.__remains = remains
        self.__nomen = nomen
        self.__unit = unit

    def storage(self):
        return self.__storage

    def remains(self):
        return self.__remains

    def nomen(self):
        return self.__nomen

    def unit(self):
        return self.__unit