import unittest
from src.settings_manager import settings_manager

class test_settings(unittest.TestCase):
    def test_check_open_settings(self):
        manager = settings_manager()

        result = manager.open("../tests/settings.json")

        assert result != False

    def test_check_create_manager(self):
        manager1 = settings_manager()
        manager2 = settings_manager()

        print(manager1.number)
        print(manager2.number)

        assert(manager1.number == manager2.number)

    def test_check_manager_convert(self):
        manager = settings_manager()
        settings, data = manager.open("../tests/settings.json")

        v = [i for i in dir(settings) if not i.startswith("_") and getattr(settings, i) != data[i] ]

        assert len(v) == 0



unittest.main()