from Src.Storage.storage import storage
from Src.Models.log_model import log_model
from Src.errors import error_proxy

class logger:
    __type: str = None
    __storage: storage = None
    __file_name = "logs.txt"

    def __init__(self, type) -> None:
        self.__type = type
        self.__storage = storage()

    # Тип лога ошибки
    @staticmethod
    def log_type_error():
        return "ERROR"
    
    # Тип лога дебага
    @staticmethod
    def log_type_debug():
        return "DEBUG"
    
    # Тип лога информации
    @staticmethod
    def log_type_info():
        return "INFO"

    def __output_file(self, log: log_model):
        try:
            with open(self.__file_name, "a") as file:
                time = log.date.strftime('%m/%d/%Y')

                file.write(f"[{time}]: [{log.kind}] {log.text}\n")
        except:
            self._error.set_error( Exception("ERROR: Невозможно загрузить логи! Не найден файл %s", self.__file_name))   


    def write(self, text: str):
        # Создаем модель лога
        log = log_model(self.__type, text)

        # Добавляем в storage по ключу логов
        key = storage.log_key()
        self.__storage.data[key].append(log)
        
        # Добавляем в файл
        self.__output_file(log)
        