from Src.Models.unit_model import unit_model
from Src.Logics.start_factory import start_factory
from Src.settings_manager import settings_manager
from Src.Storage.storage import storage
from Src.Models.reciepe_row import reciepe_row_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.group_model import group_model
from Src.Logics.start_factory import start_factory

import unittest

class factory_test(unittest.TestCase):
    def test_check_create_factory(self):
        unit = unit_model.create_gramm()

        assert unit is not None

    def test_check_nomenclature_group(self):
        result = start_factory.create_nomenclature();

        print(result)
        assert len(result) > 0

    def test_check_factory_create_method(self):
        manager = settings_manager()
        factory = start_factory(manager.settings)

        result = factory.create()

        assert len(result) > 0
        assert factory.storage is not None
        assert storage.nomenclature_key() in factory.storage.data
        assert storage.unit_key() in factory.storage.data
        assert storage.group_key() in factory.storage.data

    def test_reciepe_row(self):
        row = reciepe_row_model(
                nomenculature = nomenclature_model('Пшеничная мука', unit_model.create_kilogramm(), group_model.create_group()),
                unit=unit_model.create_gramm(),
                size=100),

        assert bool(row) == True

    def test_reciepe(self):
        data = start_factory.create_reciepes()

        assert data is not None