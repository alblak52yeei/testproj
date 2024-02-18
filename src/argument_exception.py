from src.error_proxy import error_proxy

class argument_exception(Exception):
    __inner_error: error_proxy = error_proxy()

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__inner_error.set_error(self)

    @property
    def error(self):
        return self.__inner_error