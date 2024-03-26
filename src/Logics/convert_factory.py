fom Src.Logics.basic_convertor import basic_convertor
from Src.Logics.datetime_convertor import datetime_convertor
from Src.Logics.reference_convertor import reference_convertor
from Src.reference import reference
import datetime


class convert_factory:
    maps = {}


    def __init__(self):
        self.maps[int] = basic_convertor
        self.maps[str] = basic_convertor
        self.maps[bool] = basic_convertor
        self.maps[datetime] = datetime_convertor

        for _ in reference.__subclasses__(): # связка
            self.maps[_] = reference_convertor


    def convert(self, obj) -> dict:
        result = self.__convert_list('data', obj) # конвертируем список данных

        if result is not None:
            return result

        result = {}

        fields = reference.create_fields(obj)

        for field in fields:
            attr = getattr(obj.__class__, field)

            if isinstance(attr, property):
                value = getattr(obj, field)
                dictionary =  self.__convert_list(field, value) # конвертируем список данных

                if dictionary is None:
                    dictionary = self.__convert_item(field, value)

                if len(dictionary) == 1:
                    result[field] =  dictionary[field]
                else:
                    result[field] = dictionary

        return result


    def __convert_item(self, obj, field:str):
        convertor = self.maps[type(obj)]()
        dictionary = convertor.convert(field, obj)

        return dictionary


    def __convert_list(self, obj, field:str):
        items = []