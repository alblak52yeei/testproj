from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import  nomenclature_model
from Src.Models.unit_model import unit_model
from Src.exceptions import argument_exception
from Src.Logics.nomenclature_service import nomenclature_service
from Src.Storage.storage import storage
import unittest

class nomenclature_service_test(unittest.TestCase):

    def test_add_nomenclature(self):
        group = group_model.create_default_group()
        unit = unit_model.create_ting()
        item = nomenclature_model("Тест", group, unit)

        service = nomenclature_service()
        result = service.add(item)

        assert result

    def test_change_nomenclature(self):
        group = group_model.create_default_group()
        unit = unit_model.create_ting()
        item = nomenclature_model("Тест", group, unit)

        service = nomenclature_service()
        result = service.change(item)

        # Так как номенклатуры нет, должно вернуть false
        assert result == False


        key = storage.nomenclature_key()
        item = storage().data[key][0]


        item.name = "Ааааа"
        result = service.change(item)

        assert result == True

    def test_get_nomenclature(self):
        service = nomenclature_service()

        key = storage.nomenclature_key()
        item = storage().data[key][0]

        result = service.get(item.id)

        assert isinstance(result, nomenclature_model)

    def test_delete_nomenclature(self):
        group = group_model.create_default_group()
        unit = unit_model.create_ting()
        item = nomenclature_model("Тест", group, unit)

        service = nomenclature_service()
        result = service.delete(item)

        # Так как номенклатуры нет, должно вернуть false
        assert result == False


        key = storage.nomenclature_key()
        item = storage().data[key][1]

        result = service.delete(item)

        assert result == True