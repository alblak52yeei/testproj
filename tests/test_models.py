import unittest
from src.settings_manager import settings_manager
from src.models.company import company_model
from src.models.range import range_model
from src.models.nomenclature import nomenclature_model
from src.models.nomenclature_group import nomenclature_group_model

class test_models(unittest.TestCase):
    def test_check_company_convert(self):
        # Подготовка
        manager = settings_manager()
        manager.open("../tests/settings.json")
        settings = manager.settings

        company = company_model(settings)
        # Действие
        result = True

        for i in dir(company):
            if i.startswith("_") or not hasattr(settings, i):
                continue
            
            if getattr(settings, i) != getattr(company, i):
                result = False
                break
            
        # Проверки
        assert result == True

    def test_nomenclature_group(self):
        # Подготовка
        group = nomenclature_group_model('Group one')
        # Проверки
        assert bool(group) == True

    def test_nomen(self):
        # Подготовка
        nom = nomenclature_model("Номенклатура 1", 'Большое название', 
                                nomenclature_group_model('Group'), range_model("Range"))

        # Проверки
        assert bool(nom) == True