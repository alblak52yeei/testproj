import unittest
from src.settings_manager import settings_manager
from src.models.company import company_model
from src.models.range import range_model
from src.models.nomenclature import nomenclature_model
from src.models.nomenclature_group import nomenclature_group_model

class test_settings(unittest.TestCase):
    def test_check_company_convert(self):
        manager = settings_manager()
        manager.open("../tests/settings.json")
        settings = manager.settings

        company = company_model(settings)
        result = True

        for i in dir(company):
            if i.startswith("_") or not hasattr(settings, i):
                continue
            
            if getattr(settings, i) != getattr(company, i):
                result = False
                break

        assert result == True

    def test_nomenclature_group(self):
        group = nomenclature_group_model('Group one')

        assert bool(group) == True

    def test_nomen(self):
        nom = nomenclature_model("Номенклатура 1", 'Большое название', 
                                nomenclature_group_model('Group'), range_model(name='unit'))

        assert bool(nom) == True