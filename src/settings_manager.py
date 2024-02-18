import os
import uuid
import json
from src.settings import settings
from src.argument_exception import argument_exception
from src.operation_exception import operation_exception

class settings_manager(object):
    __file_name = "settings.json"
    # Уникальный номер
    __unique_number = None
    
    __data = {}
    # Настройки инстанс
    __settings = settings()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(settings_manager, cls).__new__(cls)
    
        return cls.instance
    
    def __convert(self):
        """
            Метод конверта данных в json
        """
        if len(self.__data) == 0:
            raise argument_exception("ERROR: Невозможно создать объект типа settings.py")
        
        fields = dir(self.__settings.__class__)

        for field in fields:
            # Проверяем есть ли такое значение у объекта
            if not field in self.__data.keys():
                continue

            setattr(self.__settings, field, self.__data[field])



    def __init__(self) -> None:
        self.__unique_number = uuid.uuid4()

    def open(self, file_name: str) -> bool:
        """
            Метод открытия файла
        """
        if not isinstance(file_name, str):
            raise argument_exception("ERROR: Неверный аргумент file_name")

        if file_name == "":
            raise argument_exception("ERROR: Неверный аргумент file_name")
        
        self.__file_name = file_name.strip()

        try:
            self.__open()
            self.__convert()
        except:
            return False


    def __open(self):
        file_path = os.path.split(__file__)
        settings_file = "%s/%s" % (file_path[0], self.__file_name)

        if not os.path.exists(settings_file):
            raise operation_exception("ERROR: невозможно загрузить настройки")
        
        with open(settings_file, "r") as read_file:
            self.__data = json.load(read_file)

    @property 
    def settings(self): 
        return self.__settings

    @property 
    def data(self): 
        return self.__data
    
    @property
    def number(self):
        return str(self.__unique_number.hex)
    
    @number.setter
    def number(self, value: int) -> str:
        self.__unique_number = value