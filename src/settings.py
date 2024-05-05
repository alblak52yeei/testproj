from Src.exceptions import exception_proxy, argument_exception
from Src.Logics.storage_observer import storage_observer
from Src.Models.event_type import event_type
from datetime import datetime

#
# Класс для описания настроек
#
class settings():
    _inn = 0
    _short_name = ""
    _first_start = True
    _mode = "csv"
    _block_period = datetime.now
    
    
    @property
    def inn(self):
        """
            ИНН
        Returns:
            int: 
        """
        return self._inn
    
    @inn.setter
    def inn(self, value: int):
        exception_proxy.validate(value, int)
        self._inn = value
        #storage_observer.raise_event( event_type.settings_changed(), "inn" ) 
         
    @property     
    def short_name(self):
        """
            Короткое наименование организации
        Returns:
            str:
        """
        return self._short_name
    
    @short_name.setter
    def short_name(self, value:str):
        exception_proxy.validate(value, str)
        self._short_name = value
        #storage_observer.raise_event( event_type.settings_changed(), "short_name" ) 
        
        
    @property    
    def is_first_start(self):
        """
           Флаг Первый старт
        """
        return self._first_start    
            
    @is_first_start.setter        
    def is_first_start(self, value: bool):
        self._first_start = value
        #storage_observer.raise_event( event_type.settings_changed(), "is_first_start" ) 
        
    @property
    def report_mode(self):
        """
            Режим построения отчетности
        Returns:
            _type_: _description_
        """
        return self._mode
    
    
    @report_mode.setter
    def report_mode(self, value: str):
        exception_proxy.validate(value, str)
        
        self._mode = value
        #storage_observer.raise_event( event_type.settings_changed(), "report_mode" ) 

    @property
    def block_period(self):
        """
            Дата блокировки периода
        """
        return self._block_period
    
    @block_period.setter
    def block_period(self, value):
        legacy_period = self._block_period
        
        if isinstance(value, datetime):
            self._block_period = value
            
            if legacy_period != self._block_period:
                storage_observer.raise_event(  event_type.changed_block_period(), None  )    

            return

        if isinstance(value, str):
            try:
               print("TO<E", value)
               self._block_period = datetime.strptime(value, "%Y-%m-%d")    
               if legacy_period != self._block_period:
                    storage_observer.raise_event(  event_type.changed_block_period(), None  )    
            except Exception as ex:
                raise argument_exception(f"Невозможно сконвертировать сроку в дату! {ex}")
        else:
            raise argument_exception("Некорректно переданы параметры!")
            
        #storage_observer.raise_event( event_type.settings_changed(), "block_period" ) 