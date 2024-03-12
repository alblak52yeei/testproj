from Src.Logics.convert_factory import convert_factory
from Src.Logics.start_factory import start_factory
import unittest

class convert_test(unittest.TestCase):
    def test_check_convert_nomenclature(self):
        # Подготовка
        items = start_factory.create_nomenclatures()
        factory = convert_factory()
        item = items[0]
        # Действие
        res = factory.convert(item)
        # Проверкa
        assert res is not None


    def test_check_convert_nomenctalure_json(self):
        # Подготовка
        items = start_factory.create_nomenclatures()
        factory = convert_factory()
        # Действие
        res = factory.convert(items)
        # Проверкa
        assert res is not None 