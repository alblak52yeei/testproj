from abc import abstractmethod


class convertor:
    @abstractmethod
    def convert(self, obj, field) -> dict:
        pass 