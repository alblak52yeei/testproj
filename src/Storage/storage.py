


class storage:
    __data = {}
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(storage, cls).__new__(cls)
            
        return cls.instance  
    
    @property
    def data(self):
        return self.__data
    
    @staticmethod
    def nomenclature_key():
        return "nomenclature"
    
    @staticmethod
    def group_key():
        return "group"
    
    @staticmethod
    def unit_key():
        return "unit"
    
    