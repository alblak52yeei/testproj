from Src.Logics.Services.service import service
from Src.Logics.storage_observer import storage_observer
from Src.Models.event_type import event_type
from Src.Logics.logger import logger


class logger_service(service):
    def __init__(self, data: list) -> None:
        super().__init__(data)
        storage_observer.observers.append(self)
        
    def handle_event(self, handle_type: str, arg = None):
        super().handle_event(handle_type, arg)

        if handle_type == event_type.debug_log_writed():
            return logger(logger.log_type_debug()).write(arg)
        
        if handle_type == event_type.info_log_writed():
            return logger(logger.log_type_info()).write(arg)
        
        if handle_type == event_type.error_log_writed():
            return logger(logger.log_type_error()).write(arg)