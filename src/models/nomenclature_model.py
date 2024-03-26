from Src.reference import reference
from Src.exceptions import exception_proxy
from Src.Models.unit_model import unit_model
from Src.Models.group_model import group_model

class nomenclature_model(reference):
    " Группа номенклатуры "
    _group = None
    " Единица измерения "
    _unit = None
    
    @property
    def group(self):
        " Группа номенклатуры "
        return self._group
    
    @group.setter
    def group(self, value: reference):
        " Группа номенклатуры "
        exception_proxy.validate(value, reference)
        self._group = value    
    
    @property
    def unit(self):
        " Единица измерения "
        return self._unit
    
    @unit.setter
    def unit(self, value: reference):
        " Единица измерения "
        exception_proxy.validate(value, reference)
        self._unit = value    

    def __init__(self, name, unit: unit_model = None, group: group_model = None):
        super().__init__(name)
        self.unit = unit
        self.group = group