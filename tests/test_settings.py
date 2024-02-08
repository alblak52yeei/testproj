import unittest
from src.settings_manager import settings_manager

class test_settings(unittest.TestCase):
    def test_check_open_settings(self):
        manager = settings_manager()

        result = manager.open("../tests/settings.json")

        assert result == True

    def test_check_create_manager(self):
        manager1 = settings_manager()
        manager2 = settings_manager()

        print(manager1.number)
        print(manager2.number)

        assert(manager1.number == manager2.number)

    def test_check_manager_open(self):
        manager = settings_manager()
        
        assert manager.open("../tests/settings.json")

    def test_check_manager_convert(self):
        manager = settings_manager()
        manager.open("../tests/settings.json")

        data = manager.convert()
        
        v = [i for i in dir(data) if not i.startswith("_") and getattr(data, i) is None]

        assert len(v) == 0



unittest.main()