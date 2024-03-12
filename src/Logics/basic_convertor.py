from Src.Logics.convertor import convertor


class basic_convertor(convertor):
    def convert(self, obj, field:str):
        super().convert(obj, field)

        return {field: obj} 