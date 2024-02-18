from src.models.abstract_reference import abstract_reference
from src.models.company import company_model
from src.models.range import range_model
from src.models.nomenclature_group import nomenclature_group_model
from src.argument_exception import argument_exception
from src.operation_exception import operation_exception


class nomenclature_model(abstract_reference):
    __full_name = ''
    __group = None
    __ranges = None

    def __init__(self, name: str, full_name: str, group: nomenclature_group_model, ranges: range_model):
        super().__init__(name)
        self.full_name = full_name
        self.ranges = ranges
        self.group = group


    @property
    def full_name(self):
        return self.__full_name
    
    @full_name.setter
    def full_name(self, value: str):
        if not isinstance(value, str):
            raise argument_exception("ERROR: full_name не является строкой")

        value = value.strip()

        if value == "":
            raise argument_exception("ERROR: full_name пустое")
        
        self.__full_name = value

    @property
    def group(self):
        return self.__group
    
    @group.setter
    def group(self, value):
        if not isinstance(value, nomenclature_group_model):
            raise argument_exception("ERROR: full_name не является nomenclature_group_model")

        self.__group = value
        
    @property
    def ranges(self):
        return self.__ranges
    
    @ranges.setter
    def ranges(self, value):
        if not isinstance(value, range_model):
            raise argument_exception("ERROR: full_name не является nomenclature_group_model")
        
        self.__ranges = value