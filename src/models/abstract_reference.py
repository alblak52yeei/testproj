import uuid
from src.argument_exception import argument_exception
from src.error_proxy import error_proxy
from abc import ABC

class abstract_reference(ABC):
    __id: uuid.UUID
    __ref_name: str = ""
    __error: error_proxy = error_proxy()

    def __init__(self, name: str = None) -> None:
        self.ref_name = name
        self.__id = uuid.uuid4
    
    def error(self):
        return self.__error
    
    @property
    def id(self):
        return self.__id

    @property
    def ref_name(self):
        return self.__ref_name.strip()
    
    @ref_name.setter
    def ref_name(self, value: str):
        if not isinstance(value, str):
            raise argument_exception("ERROR: Неверный аргумент name")
        
        if value == "":
            raise argument_exception("ERROR: Пустой аргумент name")
        
        value = value.strip()

        if len(value) >= 50:
            raise argument_exception("ERROR: Неверная длина name")
        self.__ref_name = value