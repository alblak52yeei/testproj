from flask import Flask, request
from Src.settings_manager import settings_manager
from Src.Storage.storage import storage
from Src.errors import error_proxy
from Src.exceptions import operation_exception
from Src.Logics.report_factory import report_factory
from Src.Logics.start_factory import start_factory
from Src.Logics.storage_prototype import storage_prototype
from Src.Logics.process_factory import process_factory
from Src.Logics.convertor import convertor
from Src.Logics.convert_factory import convert_factory
from Src.Logics.storage_service import storage_service

from datetime import datetime
import json
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Сформировать начальный набор данных
options = settings_manager() 
start = start_factory(options.settings)
start.create()


@app.route("/api/report/<storage_key>", methods = ["GET"])
def get_report(storage_key: str):
    """
        Сформировать отчет
    Args:
        storage_key (str): Ключ - тип данных: номенклатура, группы и т.д.
    """
    
    keys = storage.storage_keys( start.storage )
    if storage_key == "" or  storage_key not in keys:
        return error_proxy.create_error_response(app, f"Некорректный передан запрос! Необходимо передать: /api/report/<storage_key>. Список ключей (storage_key): {keys}.", 400)
    
    # Создаем фабрику
    report = report_factory()
    data = start.storage.data
    
    # Формируем результат
    try:
        result = report.create_response( options.settings.report_mode, data, storage_key, app )  
        return result
    except Exception as ex:
        return error_proxy.create_error_response(app, f"Ошибка при формировании отчета {ex}", 500)

@app.route("/api/storage/rests", methods = ["GET"])
def get_rests():
    # Получить
    args = request.args

    if "start_period" not in args.keys():
        error_proxy.create_error_response("Необходимо передать параметры: start_period")
    
    if "stop_period" not in args.keys():
        error_proxy.create_error_response("Необходимо передать параметры: stop_period")
    
    manager = settings_manager()
    start = start_factory(manager.settings)
    start.create()
    key = storage.storage_transaction_key()

    start_date = datetime.strptime(args["start_period"], '%Y-%m-%d')
    stop_date = datetime.strptime(args["stop_period"], '%Y-%m-%d')


    data = storage_service(start.storage.data[key]).create_turns(start_date, stop_date)

    return storage_service.create_response(data, app)
    
@app.route("/api/storage/<nomenclature_id>/turns", methods = ["GET"])
def get_turns(nomenclature_id: str):
    nomenclature_id = int(nomenclature_id)

    manager = settings_manager()
    start = start_factory(manager.settings)
    start.create()

    transaction_key = storage.storage_transaction_key()
    transaction_data = start.storage.data[transaction_key]

    nomenclature_key = storage.nomenclature_key()
    nomenclature_data = start.storage.data[nomenclature_key][nomenclature_id]

    prototype = storage_prototype(transaction_data)
    
    result = prototype.filter_nomenclature(nomenclature_data)

    return storage_service.create_response(result.data, app)

@app.route('/api/storage/<recipe_id>/debits')
def debits_recipe(recipe_id):
    args = request.args

    if 'storage_id' not in args:
        raise operation_exception("Не указан склад")

    recipes = [recipe for recipe in start.storage.data[storage.receipt_key()] if recipe.id == recipe_id]
    storages_ = [storage for storage in start.storage.data[storage.storages_key()] if storage.id == args['storage_id']]

    if not recipes or not storages_:
        raise operation_exception("Нет подходяших  данных!")
    
    recipe = recipes[0]
    storage_ = storages_[0]
    
    start.storage.data[storage.storage_transaction_key()] += storage_service(start.storage.data[storage.storage_transaction_key()]).create_debits(recipe, storage_)

    return storage_service.create_response({'success': True}, app)
    '''

    recipe = recipes[0]
    storage_ = storages_[0]
http://127.0.0.1:5000/api/storage/4c510777671243ba893b0a1169268eee/debits?storage_id=45584cad18104591add82c0bb1994bfe
e52b7d0d1816403aba681794b471a250
    start.storage.data[storage.journal_key()] += storage_service(start.storage.data[storage.journal_key()]).create_debits(recipe, storage_)

    return storage_service.create_response({'success': True}, app)'''
if __name__ == "__main__":
    app.run(debug = True)