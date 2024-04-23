from Src.reference import reference
from Src.exceptions import exception_proxy, operation_exception
from Src.Models.unit_model import unit_model
from Src.Models.group_model import group_model
from Src.Logics.convert_factory import convert_factory
from Src.Logics.process_factory import process_factory
from Src.Logics.storage_prototype import storage_prototype
from Src.exceptions import argument_exception, exception_proxy, operation_exception
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.receipe_model import receipe_model
from Src.Models.storage_model import storage_model
from Src.Models.receipe_row_model import receipe_row_model
from Src.Storage.storage import storage


class nomenclature_service:
    """
    Получение нуменклатуры"""
    def get(nomenclature_name: str, nomenclatures: dict):
        """
            Получить значение элемента номенклатуры из словаря
        Args:
            nomenclature_name (str): наименование
            nomenclatures (dict): исходный словарь storage.data

        Returns:
            nomenclature_model: _description_
        """
        exception_proxy.validate(nomenclature_name, str)
        
        keys = list(filter(lambda x: x == nomenclature_name, nomenclatures.keys() ))
        if len(keys) == 0:
            raise operation_exception(f"Некоректно передан список. Не найдена номенклатура {nomenclature_name}!")
                
        return nomenclatures[keys[0]]
    def add(nomenclature_name: str, nomenclatures: dict):
        exception_proxy.validate(nomenclature_name,str)
        keys = input()
        if keys in nomenclature_name:
            return 'Имя есть в нуменклатуре'
        else:
            nomenclatures.append(keys)
    def delete(nomenclature_name: str, nomenclatures: dict):
        exception_proxy.validate(nomenclature_name,str)
        del nomenclatures
    def get_information_nom(self, nomenclature: nomenclature_model) -> list:
        """
            Получить инфу по нуменклатуре
        Args:
            nomenclature (nomenclature_model): _description_

        Returns:
            list: Обороты
        """
        exception_proxy.validate(nomenclature, nomenclature_model)
        prototype = storage_prototype(  self.__data )  
        filter = prototype.filter_by_nomenclature( nomenclature )
        
        return self.__processing( filter. data )   
    def get_information_rec(self, receipt: receipe_model) -> list:
        """
            Получить информцию об рецепте
        Args:
            receipt (receipe_model): _description_

        Returns:
            list: _description_
        """
        exception_proxy.validate(receipt, receipe_model)
        
        
        
        # Отфильтровать по рецепту
        transactions = []
        filter =  storage_prototype(  self.__data )
        for item in receipt.rows():
            filter =  filter.filter_by_nomenclature( item.nomenclature )
            if filter.is_empty:
                for transaction in filter.data:
                    transactions.append( transaction )
                    
            filter.data = self.__data        
            
        return self.__processing( transactions )  