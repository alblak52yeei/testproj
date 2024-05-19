from Src.Logics.Services.service import service
from Src.Models.event_type import event_type
from Src.Storage.storage import storage
from Src.errors import error_proxy
from Src.exceptions import exception_proxy
from Src.Logics.convert_factory import convert_factory
from Src.Logics.storage_observer import storage_observer

import json

class console_log_service(service):

    __item:error_proxy = None
    __factory:convert_factory = None

    def __init__(self, data: list = None) -> None:
        super().__init__(data)

        self.__factory = convert_factory()
        storage_observer.append(self)

    @property
    def item(self) -> error_proxy:
        return self.__item
    
    @item.setter
    def item(self, value: error_proxy):
        exception_proxy.validate(value, error_proxy)

        self.__item = value

    def __observer_log_console(self):
        """
            Сохранить лог в консоль
        """
        data = self.__factory.serialize(self.item)
        json_text = json.dumps(data, sort_keys = True, indent = 4, ensure_ascii = False)

        # Выводим  
        print(json_text)    


    def handle_event(self, handle_type: str ):
        """
            Обработать событие
        Args:
            handle_type (str): Ключ
        """
        super().handle_event(handle_type)

        # Добавить лог в консоль
        if handle_type == event_type.write_log() and self.__item is not None:
            self.__observer_log_console()