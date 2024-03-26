from Src.Logics.convert_factory import convert_factory
from Src.Logics.process_factory import process_factory
from Src.Logics.storage_prototype import storage_prototype
from Src.Models.receipe_model import receipe_model
from Src.Models.storage_model import storage_model
from Src.Models.storage_row_model import storage_row_model
from Src.exceptions import argument_exception, exception_proxy, operation_exception
from datetime import datetime
import json
class storage_service:
    __data = {}

    def __init__(self, data: list) -> None:
        if len(data) == 0:
            raise argument_exception("Некорректно переданы параметры")
        
        self.__data = data

    def create_turns(self, start_period: datetime, stop_period: datetime) -> dict:
        exception_proxy(start_period, datetime)
        exception_proxy(stop_period, datetime)

        if start_period > stop_period:
            raise argument_exception("Некорректно переданы параметры")
        
        # Отфильтровать
        prototype = storage_prototype(self.__data)
        transactions = prototype.filter_date(start_period, stop_period)
    
        processing = process_factory().create(process_factory.turn_key())
        # Остатки
        rests = processing().process(transactions.data)

        data = convert_factory().serialize(rests)

        return data
    
    def create_turns_by_storage_receipe(self, receipe: receipe_model, storage: storage_model):
        # Отфильтровать
    
        prototype = storage_prototype(self.__data)

        transactions = prototype.filter_storage(storage).filter_recipe(receipe)
    
        processing = process_factory().create(process_factory.turn_key())
        # Остатки
        rests = processing().process(transactions.data)

        data = convert_factory().serialize(rests)

        return data
        
    def create_debits(self, receipe: receipe_model, storage: storage_model):
        turns = self.create_turns_by_storage_receipe(receipe, storage)

        recipe_need = {}
        for recipe_row in receipe.rows:
            recipe_need[recipe_row.nomenculature.name] = recipe_row.size

        transactions = []
        for turn in turns:
            if recipe_need[turn.nomen.name] > turn.remains:
                raise operation_exception('Не удалось произвести списывание. Недостаточно остатков на складе')
            
            item = storage_row_model("Test")
            item.nomenclature = turn.nomenclature
            item.unit = turn.unit
            item.storage_type = False
            item.value = recipe_need[turn.nomen.name]
            item.storage = storage
            item.period = datetime.now()

            transactions.append(item)
        return transactions
    
    @staticmethod
    def create_response(data: dict, app):
        if app is None:
            raise argument_exception("Нет апп")
        
        data = convert_factory().serialize(data)
        json_text = json.dumps(data, sort_keys=True, indent=4, ensure_ascii=True)

        result = app.response_class(
            response =   f"{json_text}",
            status = 200,
            mimetype = "application/json; charset=utf-8"
        )  

        return result