
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.unit_model import unit_model
from Src.settings import settings
from Src.Storage.storage import storage
from Src.Models.reciepe_model import reciepe_model
from Src.Models.reciepe_row import reciepe_row_model

class start_factory:
    __options: settings = None
    __storage: storage = None
    
    def __init__(self, _options: settings, _storage: storage = None) -> None:
        self.__options = _options
        self.__storage = _storage

        self.__build()
    
    def create(self):
        result = []

        if not self.__options.is_first_start: return result

        self.__options.is_first_start = False

        items = start_factory.create_nomenclature()

        result += items
        result += set([v.unit for v in items])
        result += set([v.group for v in items])
        result += start_factory.create_reciepes()

        return result

    def __build(self):
        if self.__storage == None:
            self.__storage = storage()

        items = start_factory.create_nomenclature()

        self.__storage.data[storage.nomenclature_key()] = items
        self.__storage.data[storage.unit_key()] = set([v.unit for v in items])
        self.__storage.data[storage.group_key()] = set([v.group for v in items])

    @property
    def storage(self):
        return self.__storage
    
    @staticmethod
    def create_nomenclature():

        nomenclature_group = group_model.create_group()

        return [
            nomenclature_model("Пшеничная мука", unit_model.create_kilogramm(), nomenclature_group),
            nomenclature_model("Сахар", unit_model.create_kilogramm(), nomenclature_group),
            nomenclature_model("Сливочное масло", unit_model.create_mililiter(), nomenclature_group),
            nomenclature_model("Яйца", unit_model.create_count(), nomenclature_group),
            nomenclature_model("Ванилин", unit_model.create_gramm(), nomenclature_group),
            nomenclature_model("Яичный белок", unit_model.create_count(), nomenclature_group),
            nomenclature_model("Сахарная пудра", unit_model.create_gramm(), nomenclature_group),
            nomenclature_model("Корица", unit_model.create_gramm(), nomenclature_group),
            nomenclature_model("Какао", unit_model.create_mililiter(), nomenclature_group),
            nomenclature_model("Куриное филе", unit_model.create_kilogramm(), nomenclature_group),
            nomenclature_model("Салат Романо", unit_model.create_count(), nomenclature_group),
            nomenclature_model("Сын Пармезан", unit_model.create_gramm(), nomenclature_group),
            nomenclature_model("Чеснок", unit_model.create_gramm(), nomenclature_group),
            nomenclature_model("Белый хлеб", unit_model.create_gramm(), nomenclature_group),
            nomenclature_model("Соль", unit_model.create_gramm(), nomenclature_group),
            nomenclature_model("Чёрный перец", unit_model.create_gramm(), nomenclature_group),
            nomenclature_model("Оливковое масло", unit_model.create_liter(), nomenclature_group),
            nomenclature_model("Лимонный сок", unit_model.create_liter(), nomenclature_group),
            nomenclature_model("Горчица дижонская", unit_model.create_gramm(), nomenclature_group),
        ]
    
    @staticmethod
    def create_reciepes():
        return [
            reciepe_model(
                'ВАФЛИ ХРУСТЯЩИЕ В ВАФЕЛЬНИЦЕ',
            reciepe_row_model(
                nomenculature = nomenclature_model('Пшеничная мука', unit_model.create_kilogramm(), group_model.create_group()),
                unit=unit_model.create_gramm(),
                size=100),
            reciepe_row_model(
                nomenculature = nomenclature_model('Сахар', unit_model.create_kilogramm(), group_model.create_group()),
                unit=unit_model.create_gramm(),
                size=80),
            reciepe_row_model(
                nomenculature = nomenclature_model('Сливочное масло', unit_model.create_gramm(), group_model.create_group()),
                unit=unit_model.create_gramm(),
                size=70),
            reciepe_row_model(
                nomenculature = nomenclature_model('Яйца', unit_model.create_count(), group_model.create_group()),
                unit=unit_model.create_count(),
                size=1),
            reciepe_row_model(
                nomenculature = nomenclature_model('Ванилин', unit_model.create_gramm(), group_model.create_group()),
                unit=unit_model.create_gramm(),
                size=5),
            description='''
Время приготовления: 20 мин
Как испечь вафли хрустящие в вафельнице? Подготовьте необходимые продукты. Из данного количества у меня получилось 8 штук диаметром около 10 см.
Масло положите в сотейник с толстым дном. Растопите его на маленьком огне на плите, на водяной бане либо в микроволновке.
Добавьте в теплое масло сахар. Перемешайте венчиком до полного растворения сахара. От тепла сахар довольно быстро растает.
Добавьте в масло яйцо. Предварительно все-таки проверьте масло, не горячее ли оно, иначе яйцо может свариться. Перемешайте яйцо с маслом до однородности.
Всыпьте муку, добавьте ванилин.
Перемешайте массу венчиком до состояния гладкого однородного теста.
Разогрейте вафельницу по инструкции к ней. У меня очень старая, еще советских времен электровафельница. Она может и не очень красивая, но печет замечательно! Я не смазываю вафельницу маслом, в тесте достаточно жира, да и к ней уже давно ничего не прилипает. Но вы смотрите по своей модели. Выкладывайте тесто по столовой ложке. Можно класть немного меньше теста, тогда вафли будут меньше и их получится больше.
Пеките вафли несколько минут до золотистого цвета. Осторожно откройте вафельницу, она очень горячая! Снимите вафлю лопаткой. Горячая она очень мягкая, как блинчик. Но по мере остывания становится твердой и хрустящей. Такие вафли можно свернуть трубочкой. Но делать это надо сразу же после выпекания, пока она мягкая и горячая, потом у вас ничего не получится, вафля поломается. Приятного аппетита!
            ''')
        ]