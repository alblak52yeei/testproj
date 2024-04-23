from Src.Logics.Services.service import service
from Src.Logics.storage_observer import storage_observer
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.event_type import event_type
from Src.Storage import storage

class post_processing_service(service):
    def __init__(self, data: list) -> None:
        super().__init__(data)
        storage_observer.observers.append(self)

    def handle_event(self, handle_type: str, nomenclature: nomenclature_model):
        """
            Обработать событие
        Args:
            handle_type (str): _description_
        """
        is_changed = False
        #super().handle_event(handle_type, arg)

        if handle_type == event_type.deleted_nomenclature():
            recipes = self.__data[storage.receipt_key()]
            
            for recipe in recipes:
                for row in recipe.rows():
                    if row.nomenclature.id == nomenclature.id:
                        recipe.delete(row)
                        is_changed = True
                        print("Remove recipe with id", recipe.id)

        # Если было изменение, то сохраняем
        if is_changed:
            self.save()