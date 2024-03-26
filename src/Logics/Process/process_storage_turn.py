from Src.Logics.Process.abstract_process import abstract_process
from Src.Models.storage_turn_model import storage_turn_model

class process_storage_turn(abstract_process):
    @classmethod
    def create(cls, journal: list[storage_turn_model]):
        return []