from Src.exceptions import exception_proxy
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model
from Src.Storage.storage import storage

class nomenclature_service:
    __storage: storage = storage()

    def __get_nomenclatures(self):
        # Получаем список номенклатур
        key = self.__storage.nomenclature_key()
        nomenclatures = self.__storage.data[key]

        return nomenclatures

    def __find_nomenclature_in_storage(self, current_nomenclature: nomenclature_model):
        # Получаем список номенклатур
        nomenclatures = self.__get_nomenclatures()

        # Находим нужную по ID
        for i, nomenclature in enumerate(nomenclatures):
            if current_nomenclature.id == nomenclature.id:
                return i, nomenclature
        
        return False, False
        
    def __find_nomenclature_by_id(self, nomenclature_id: int):
        # Получаем список номенклатур
        nomenclatures = self.__get_nomenclatures()

        # Находим нужную по ID
        for i, nomenclature in enumerate(nomenclatures):
            if nomenclature_id == nomenclature.id:
                return i, nomenclature
        
        return False, False
    
    def add(self, nomenclature: nomenclature_model):
        exception_proxy.validate(nomenclature, nomenclature_model)

        index, finded_nomenclature = self.__find_nomenclature_in_storage(nomenclature)

        if index or finded_nomenclature:
            return False # такой объект уже есть

        # Добавляем номенклатуру
        nomenclatures = self.__get_nomenclatures()
        nomenclatures.append(nomenclature)

        # Сохраняем
        self.__storage.save()

        # Возвращаем True, так как объект был добавлен
        return True
    
    def change(self, nomenclature: nomenclature_model):
        exception_proxy.validate(nomenclature, nomenclature_model)

        index, finded_nomenclature = self.__find_nomenclature_in_storage(nomenclature)

        if not finded_nomenclature:
            return False # такого объекта нет

        # Получаем все номенклатуры
        nomenclatures = self.__get_nomenclatures()

        print("ID", index)
        nomenclatures[index] = nomenclature

        # Сохраняем
        self.__storage.save()

        # Возвращаем True, так как объект был изменен
        return True
    
    def delete(self, nomenclature: nomenclature_model):
        exception_proxy.validate(nomenclature, nomenclature_model)

        index, finded_nomenclature = self.__find_nomenclature_in_storage(nomenclature)

        if not finded_nomenclature:
            return False # такого объекта нет

        # Получаем все номенклатуры
        nomenclatures = self.__get_nomenclatures()
        nomenclatures[index] = None

        # Сохраняем
        self.__storage.save()

        # Возвращаем True, так как объект был изменен
        return True
    
    def get(self, nomenclature_id: str):
        exception_proxy.validate(nomenclature_id, str)

        index, finded_nomenclature = self.__find_nomenclature_by_id(nomenclature_id)

        if not finded_nomenclature:
            return False # такого объекта нет

        # Получаем все номенклатуры
        nomenclatures = self.__get_nomenclatures()
        return nomenclatures[index]
