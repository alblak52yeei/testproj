from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.unit_model import unit_model
from Src.reference import reference
from Src.exceptions import exception_proxy

class reciepe_row_model(reference):
    __nomenculatures: nomenclature_model = None
    __size: int = 0
    __unit: unit_model = None

    def __init__(self, nomenculature: nomenclature_model, size: int, unit: unit_model):
        self.__nomenculatures = nomenculature
        self.__size = size
        self.__unit = unit

        super().__init__(name=f"{self.__nomenculatures.name}, {size} {self.__unit.name}")

    @property
    def nomenculature(self):
        return self.__nomenculatures

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value : int):
        exception_proxy.validate(value, int)

        self.__size = value

    @property
    def unit(self):
        return self.__unit 