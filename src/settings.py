from src.argument_exception import argument_exception

class settings:
    # Инициализируем пустыми
    __first_name = None
    __inn = None
    __bik = None
    __account = None
    __cor_account = None
    __name = None
    __ownship_type = None

    @property
    def first_name(self):
        return self.__first_name
    
    @first_name.setter
    def first_name(self, value: str):
        if not isinstance(value, str):
            raise argument_exception("Некорректный аргумент!")
        
        self.__first_name = value.strip()
        
    # ИНН
    @property
    def inn(self):
        return self.__inn
    
    @inn.setter
    def inn(self, value: str):
        if not isinstance(value, str):
            raise argument_exception("ERROR: Некорректный аргумент!")
        
        if len(value) != 12:
            raise argument_exception("ERROR: Длина ИНН не равна 12!")
        
        self.__inn = value.strip()

    # Кор. счёт
    @property
    def cor_account(self):
        return self.__cor_account
    
    @cor_account.setter
    def cor_account(self, value: str):
        if not isinstance(value, str):
            raise argument_exception("Некорректный аргумент!")
        
        if len(value) != 11:
            raise argument_exception("ERROR: Длина кор. счёта не равна 11!")
        
        self.__cor_account = value.strip()
    
    # БИК
    @property
    def bik(self):
        return self.__bik
    
    @bik.setter
    def bik(self, value: str):
        if not isinstance(value, str):
            raise argument_exception("Некорректный аргумент!")
        
        if len(value) != 9:
            raise argument_exception("ERROR: Длина БИК не равна 9!")
        
        self.__bik = value.strip()

    # Счёт
    @property
    def account(self):
        return self.__account
    
    @account.setter
    def account(self, value: str):
        if not isinstance(value, str):
            raise argument_exception("Некорректный аргумент!")

        if len(value) != 11:
            raise argument_exception("ERROR: Длина счёта не равна 11!")
        
        self.__account = value.strip()

    # Наименование
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise argument_exception("Некорректный аргумент!")
        
        if str == "":
            raise argument_exception("ERROR: Пустое наименование!")
        
        self.__name = value.strip()

    # Вид собственности
    @property
    def ownship_type(self):
        return self.__ownship_type
    
    @ownship_type.setter
    def ownship_type(self, value: str):
        if not isinstance(value, str):
            raise argument_exception("Некорректный аргумент!")
        
        if len(value) != 5:
            raise argument_exception("ERROR: Длина вида собственности не равна 5!")
        
        self.__ownship_type = value.strip()