import os
import uuid
import json
from src.settings import settings

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
        if len(self.__data) == 0:
            raise Exception("ERROR: Невозможно создать объект типа settings.py")
        
        fields = dir(self.__settings.__class__)

        for field in fields:
            # Проверяем есть ли такое значение у объекта
            if not field in self.__data.keys():
                continue

            setattr(self.__settings, field, self.__data[field])

        return self.__settings, self.__data
        

    def __init__(self) -> None:
        self.__unique_number = uuid.uuid4()

    def open(self, file_name: str) -> bool:
        if not isinstance(file_name, str):
            raise Exception("ERROR: Неверный аргумент file_name")

        if file_name == "":
            raise Exception("ERROR: Неверный аргумент file_name")
        
        self.__file_name = file_name.strip()

        try:
            self.__open()
            return self.__convert()
        except:
            return False


    def __open(self):
        file_path = os.path.split(__file__)
        settings_file = "%s/%s" % (file_path[0], self.__file_name)

        if not os.path.exists(settings_file):
            raise Exception("ERROR: невозможно загрузить настройки")
        
        with open(settings_file, "r") as read_file:
            self.__data = json.load(read_file)

    @property
    def number(self):
        return str(self.__unique_number.hex)
    
    @number.setter
    def number(self, value: int) -> str:
        self.__unique_number = value