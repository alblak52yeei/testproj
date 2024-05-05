import uuid

from Src.Storage.storage import storage

from Src.exceptions import argument_exception
from Src.Logics.storage_observer import storage_observer
from Src.Models.event_type import event_type
from Src.Logics.Services.service import service
from Src.Models.nomenclature_model import nomenclature_model

class post_processing_service(service):
    __nomenclature = None
    __storage = None
    __deleted = False

    def __init__(self, nomenclature: nomenclature_model, data: list):
        super().__init__(data)
        self.__storage=storage()
        self.__nomenclature = nomenclature

        #добавляем в наблюдатели
        storage_observer.observers.append(self)


    def handle_event(self, handle_type: str, arg = None):
        super().handle_event(handle_type)

        if not self.__deleted and handle_type == event_type.deleted_nomenclature() and str(arg.id) == str(self.__nomenclature.id):
            # Удаляем обсервер
            self.__deleted = True
            storage_observer.observers.remove(self)

            self.clear_reciepe()
            self.clear_journal()

    #очищаем рецепт
    def clear_reciepe(self):
        key = storage.receipt_key()

        for recipe in self.__storage.data[key]:
            for key in recipe.consist.keys():
                row = recipe.consist[key]

                if row.nomenclature.id == self.__nomenclature.id:
                    del row

    #очищаем журнал
    def clear_journal(self):
        key = storage.storage_transaction_key()
        res = [ ]
        
        #собираем второй массив без операций над удалённой номенклатурой
        for cur_line in self.__storage.data[key]:
            if cur_line.nomenclature.id != self.__nomenclature.id:
                res.append(cur_line)

        self.__storage.data[key] = res
        #перерасчитываем оборот за блок период
        storage_observer.raise_event(event_type.changed_block_period(), None)