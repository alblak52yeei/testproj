from Src.reference import reference


class storage_model(reference):
    __adress: str = ''

    def __init__(self, adress: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__adress = adress

    def adress(self) -> str:
        return self.__adress