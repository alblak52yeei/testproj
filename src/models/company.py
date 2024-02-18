# ИНН, БИК, Счет, Форма собственности.
from src.models.abstract_reference import abstract_reference
from src.argument_exception import argument_exception
from src.operation_exception import operation_exception

class company_model(abstract_reference):
    __inn = None
    __bik = None
    __account = None
    __ownship_type = None
    __settings = None

    def __init__(self, settings, name: str = "Company"):
        super().__init__(name)
        self.__settings = settings
        self.__convert()

    def __convert(self):
        for field in dir(self):
            if field.startswith("_") or not hasattr(self.__settings, field):
                continue
            
            value = getattr(self.__settings, field)
            setattr(self, f"_{self.__class__.__name__}__{field}", value)

    # ИНН
    @property
    def inn(self):
        return self.__inn

    # БИК
    @property
    def bik(self):
        return self.__bik
    
    # Счёт
    @property
    def account(self):
        return self.__account

    # Вид собственности
    @property
    def ownship_type(self):
        return self.__ownship_type