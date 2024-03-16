from abc import ABC, abstractmethod

class abstract_process(ABC):
    operations = {True: 1, False: -1}

    @abstractmethod
    def create(self):
        pass