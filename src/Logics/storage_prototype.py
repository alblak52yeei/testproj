from Src.exceptions import argument_exception
from Src.errors import error_proxy
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.receipe_model import receipe_model
from Src.Models.storage_model import storage_model
from datetime import datetime

class storage_prototype(error_proxy):
    __data = []

    def __init__(self, data: list) -> None:
        if len(data) == 0:
            self.error = "Некорректно передана data"
        
        self.__data = data

    def filter_date(self, start_period: datetime, stop_period: datetime):
        if start_period > stop_period:
            self.error = "Некорректный период"

        if not self.is_empty:
            return self.__data
        
        result = []

        for item in self.__data:
            if item.period > start_period and item.period <= stop_period:
                result.append(item)

        return storage_prototype(result)
    
    def filter_nomenclature(self, nomenclature: nomenclature_model):
        if not isinstance(nomenclature, nomenclature_model):
            self.error = "Некорректная номенклатура"

        if not self.is_empty:
            return self.__data
        
        result = []

        for item in self.__data:
            if item.nomenclature == nomenclature:
                result.append(item)

        return storage_prototype(result)
    
    def filter_storage(self, filter_model: storage_model):
        result = []

        for item in self.data:
            if item.storage.name != filter_model.name: continue
            result.append(item)

        return storage_prototype(result)
    
    def filter_recipe(self, filter_model: receipe_model):
        recipe_nomens = set([nomenclature.name for nomenclature in filter_model.rows.values()])
        result = []

        for item in self.data:
            if item.nomenculature.name not in recipe_nomens: continue

            result.append(item)

        return storage_prototype(result) 
    
    @property
    def data(self):
        return self.__data