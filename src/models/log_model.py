from datetime import datetime

class log_model:
    __kind: str = None
    __text: str = None
    __date: datetime = None

    def __init__(self, kind: str, text: str) -> None:
        self.__kind = kind
        self.__text = text
        self.__date = datetime.now()

    @property
    def kind(self):
        return self.__kind
    
    @property
    def text(self):
        return self.__text
    
    @property
    def date(self):
        return self.__date