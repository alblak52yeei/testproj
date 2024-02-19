from src.models.abstract_reference import abstract_reference

class range_model(abstract_reference):
    __base = None
    __cf: int

    def __init__(self, name: str, cf: int = 0, base = None):
        super().__init__(name)
        self.__base = base
        self.__cf = cf

    @property
    def base(self):
        return self.__base
    
    @property
    def cf(self):
        return self.__cf