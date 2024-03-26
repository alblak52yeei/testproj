from Src.Logics.storage_service import storage_service
from Src.Logics.start_factory import start_factory
from Src.settings_manager import settings_manager
from Src.Storage.storage import storage
import unittest

class test_models(unittest.TestCase):
    def test_reciepe_devits(self):
        options = settings_manager()
        start = start_factory(options.settings)
        start.create()

        reciepe = start.storage.data[storage.receipt_key()][0]
        storage1 = start.storage.data[storage.storages_key()][0]

        service = storage_service(start.storage.data[storage.storage_transaction_key()])
        result = service.create_debits(reciepe , storage1)

        assert result is not None
        assert len(result) != 0