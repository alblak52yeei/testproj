from Src.Logics.storage_prototype import storage_prototype
from Src.Logics.start_factory import start_factory
from Src.settings_manager import settings_manager
from Src.Storage.storage import storage
from datetime import datetime
import unittest

class prototype_test(unittest.TestCase):
    def test_check_prototype(self):
        # Подготовка
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()
        key = storage.storage_transaction_key()
        data = start.storage.data[key]

        start_date = datetime.strptime('2024-01-01', '%Y-%m-%d')
        stop_date = datetime.strptime('2024-01-10', '%Y-%m-%d')

        prototype = storage_prototype(data)

        # Действие

        result = prototype.filter_date(start_date, stop_date)
        
        assert isinstance(result, storage_prototype)

    def test_check_nomenclature_prototype(self):
        # Подготовка
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()

        transaction_key = storage.storage_transaction_key()
        transaction_data = start.storage.data[transaction_key]

        nomenclature_key = storage.nomenclature_key()
        nomenclature_data = start.storage.data[nomenclature_key][1]

        prototype = storage_prototype(transaction_data)
        
        # Действие

        result = prototype.filter_nomenclature(nomenclature_data)
        
        assert isinstance(result, storage_prototype)

    def test_check_nomenclature_prototype(self):
        # Подготовка
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()

        start_date = datetime.strptime('2024-01-01', '%Y-%m-%d')
        stop_date = datetime.strptime('2024-01-10', '%Y-%m-%d')

        transaction_key = storage.storage_transaction_key()
        transaction_data = start.storage.data[transaction_key]

        nomenclature_key = storage.nomenclature_key()
        nomenclature_data = start.storage.data[nomenclature_key]["id"]

        prototype = storage_prototype(transaction_data)
        
        # Действие

        result = prototype.filter_nomenclature(nomenclature_data).filter_date(start_date, stop_date)
        
        assert isinstance(result, storage_prototype)

    def test_check_receipe_prototype(self):
        # Подготовка
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()

        transaction_key = storage.storage_transaction_key()
        transaction_data = start.storage.data[transaction_key]

        key = storage.receipt_key()
        data = start.storage.data[key]["id"]

        prototype = storage_prototype(transaction_data)
        
        # Действие

        result = prototype.filter_recipe(data)
        
        assert isinstance(result, storage_prototype)

    def test_check_storage_prototype(self):
        # Подготовка
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()

        transaction_key = storage.storage_transaction_key()
        transaction_data = start.storage.data[transaction_key]

        key = storage.storages_key()
        data = start.storage.data[key]["id"]

        prototype = storage_prototype(transaction_data)
        
        # Действие

        result = prototype.filter_recipe(data)
        
        assert isinstance(result, storage_prototype)