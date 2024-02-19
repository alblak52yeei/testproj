from src.error_proxy import error_proxy
from src.argument_exception import argument_exception
class operation_exception(argument_exception):
    __inner_error: error_proxy = error_proxy()

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__inner_error.set_error(self)

    @property
    def error(self):
        return self.__inner_error