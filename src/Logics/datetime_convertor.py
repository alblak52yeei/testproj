from Src.Logics.convertor import convertor
import datetime


class datetime_convertor(convertor):
    def convert(self, obj, field:str):
        super().convert(obj, field)

        return { field: obj.strftime('%Y-%m-%d') } 