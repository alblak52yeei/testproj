from Src.Logics.convertor import convertor
from Src.Logics.convert_factory import convert_factory


class reference_convertor(convertor):
    def convert(self, obj, field:str):
        return convert_factory().convert(object)