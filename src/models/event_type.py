from Src.reference import reference


#
# Типы событий
#
class event_type(reference):
 
    @staticmethod
    def changed_block_period() -> str:
        """
            Событие изменения даты блокировки
        Returns:
            str: _description_
        """
        return "changed_block_period"

    @staticmethod
    def deleted_nomenclature() -> str:
        """
            Событие удаления номенлатуры
        Returns:
            str: _description_
        """
        return "deleted_nomenclature"
    
    @staticmethod
    def settings_changed() -> str:
        """
            Событие изменения настроек
        Returns:
            str: _description_
        """
        return "settings_changed"
    
    @staticmethod
    def info_log_writed() -> str:
        return "info_log_writed"
    
    @staticmethod
    def debug_log_writed() -> str:
        return "debug_log_writed"
    
    @staticmethod
    def error_log_writed() -> str:
        return "error_log_writed"