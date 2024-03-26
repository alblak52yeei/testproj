from Src.Models.nomenclature_model import nomenclature_model
from Src.reference import reference
from Src.Models.unit_model import unit_model
from Src.exceptions import exception_proxy

class reciepe_model (reference):
    __rows: list
    __description: str

    def __init__(self, name, *args, description: str = 'Киньте всё в одну чашу и перемешайте.'):
        self.__rows = list(args)
        self.description = description
        super().__init__(name=name)

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value: str):
        exception_proxy.validate(value.strip(), str)
        self.__description = value.strip()