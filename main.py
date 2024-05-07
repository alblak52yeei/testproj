from flask import Flask, request
from Src.settings_manager import settings_manager
from Src.Storage.storage import storage
from Src.errors import error_proxy
from Src.Logics.report_factory import report_factory
from Src.Logics.start_factory import start_factory
from datetime import datetime
from Src.Logics.Services.storage_service import storage_service
from Src.Models.nomenclature_model import nomenclature_model
from Src.Logics.Services.service import service
from Src.Logics.Services.reference_service import reference_service
from Src.Logics.storage_observer import storage_observer
from Src.Models.event_type import event_type
from Src.Logics.Services.logger_service import logger_service


#from Src.Logics.logger import logger



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Сформировать начальный набор данных
options = settings_manager() 
start = start_factory(options.settings)
start.create()

#logger = logger(logger.log_type_info())
logger = logger_service([])
# Отчетность

@app.route("/api/report/<storage_key>", methods = ["GET"])
def get_report(storage_key: str):
    """
        Сформировать отчет
    """
    
    keys = storage.storage_keys( start.storage )
    if storage_key == "" or  storage_key not in keys:
        return error_proxy.create_error_response(app, f"Некорректный передан запрос! Необходимо передать: /api/report/<storage_key>. Список ключей (storage_key): {keys}.", 400)
    
    # Создаем фабрику
    report = report_factory()
    data = start.storage.data
    
    storage_observer.raise_event( event_type.info_log_writed(), f"Вызов get_report (storage_key: {storage_key})" ) 
    #logger.write(f"Вызов get_report (storage_key: {storage_key})")
    # Формируем результат
    try:
        result = report.create_response( options.settings.report_mode, data, storage_key, app )  
        return result
    except Exception as ex:
        return error_proxy.create_error_response(app, f"Ошибка при формировании отчета {ex}", 500)

# Отчетность

# Складские операции

@app.route("/api/storage/turns", methods = ["GET"] )
def get_turns():
    """
        Получить обороты за период
    """

    # Получить параметры
    args = request.args
    if "start_period" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: start_period, stop_period!")
        
    if "stop_period" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: start_period, stop_period!")
    
    start_date = datetime.strptime(args["start_period"], "%Y-%m-%d")
    stop_date = datetime.strptime(args["stop_period"], "%Y-%m-%d")
          
    source_data = start.storage.data[  storage.storage_transaction_key()   ]      
    data = storage_service( source_data   ).create_turns( start_date, stop_date )      
    result = service.create_response( app, data )

    storage_observer.raise_event( event_type.info_log_writed(), f"Вызов get_turns" ) 
    #logger.write(f"Вызов get_turns")
    return result
      
@app.route("/api/storage/<nomenclature_id>/turns", methods = ["GET"] )
def get_turns_nomenclature(nomenclature_id):
    """
        Получить обороты за период и по коду номенклатукры
    """
    
    # Получить параметры
    args = request.args
    if "start_period" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: start_period, stop_period!", 400)

    if "stop_period" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: start_period, stop_period!", 400)

    try:
        start_date = datetime.strptime(args["start_period"], "%Y-%m-%d")
        stop_date = datetime.strptime(args["stop_period"], "%Y-%m-%d")
    except:
        return error_proxy.create_error_response(app, "Некорректно перпеданы параметры: start_period, stop_period", 400)    

    transactions_data = start.storage.data[  storage.storage_transaction_key()   ]   
    nomenclature_data =  start.storage.data[  storage.nomenclature_key()   ]   
    
    nomenclatures =  nomenclature_model.create_dictionary( nomenclature_data )
    ids = [item.id for item in nomenclatures.values()]
    if nomenclature_id not in ids:
        return error_proxy.create_error_response(app, "Некорректно передан код номенклатуры!", 400)
    
    nomenclature = nomenclatures[nomenclature_id]
    storage_observer.raise_event( event_type.info_log_writed(), f"Вызов get_turns_nomenclature (nomenclature_id: {nomenclature_id})" ) 
    #logger.write(f"Вызов get_turns_nomenclature (nomenclature_id: {nomenclature_id})")
    data = storage_service( transactions_data  ).create_turns_by_nomenclature( start_date, stop_date, nomenclature )      
    result = service.create_response( data, app )
    return result      

# Складские операции

# Номерклатура
@app.route("/api/nomenclature", methods = ["PUT"])
def add_nomenclature():
    """
        Добавить номерклатуру
    """
    try:
        data = request.get_json()
        item = nomenclature_model().load(data)
        source_data = start.storage.data[  storage.nomenclature_key() ]
        result = reference_service( source_data ).add( item )
        storage_observer.raise_event( event_type.info_log_writed(), f"Вызов add_nomenclature (data.name: {data.name})" ) 
        #logger.write(f"Вызов add_nomenclature (data.name: {data.name})")
        return service.create_response( {"result": result} )
    except Exception as ex:
        return error_proxy.create_error_response(app,   f"Ошибка при добавлении данных!\n {ex}")


@app.route("/api/nomenclature", methods = ["DELETE"])
def delete_nomenclature():
    """
        Удалить номенклатуру
    """
    try:
        data = request.get_json()
        item = nomenclature_model().load(data)
        source_data = start.storage.data[  storage.nomenclature_key() ]
        result = reference_service( source_data ).delete( item )
        storage_observer.raise_event( event_type.info_log_writed(), f"Вызов add_nomenclature (item.id: {item.id})" ) 
        #logger.write(f"Вызов add_nomenclature (item.id: {item.id})")
        return service.delete_nomenclature( {"result": result} )
    except Exception as ex:
        return error_proxy.create_error_response(app,   f"Ошибка при удалении данных!\n {ex}")


@app.route("/api/nomenclature", methods = ["PATH"])
def change_nomenclature():
    """
        Изменить номенклатуру
    """
    try:
        data = request.get_json()
        item = nomenclature_model().load(data)
        source_data = start.storage.data[  storage.nomenclature_key() ]
        result = reference_service( source_data ).change( item )
        storage_observer.raise_event( event_type.info_log_writed(), f"Вызов change_nomenclature (item.id: {item.id})" ) 
        #logger.write(f"Вызов change_nomenclature (item.id: {item.id})")
        return service.create_response( {"result": result} )
    except Exception as ex:
        return error_proxy.create_error_response(app,   f"Ошибка при изменении данных!\n {ex}")
    
@app.route("/api/nomenclature", methods = ["GET"])
def get_nomenclature():
    """
        Получить список номенклатуры
    """
    args = request.args

    storage_observer.raise_event( event_type.info_log_writed(), f"Вызов get_nomenclature" ) 
    #logger.write(f"Вызов get_nomenclature")

    if "id" not in args.keys():
        # Вывод всех элементов
        source_data = start.storage.data[  storage.nomenclature_key() ]
        result = reference_service(source_data ).get()
        return service.create_response(app, result)
    else:
        # Вывод конкретного элемента
        try:
            source_data = start.storage.data[  storage.nomenclature_key() ]
            result = reference_service(source_data ).get_item(args["id"])
            return service.create_response(app, result)
        except Exception as ex:
            return error_proxy.create_error_response(app,   f"Ошибка при получении данных!\n {ex}")


# Номенклатура

@app.route("/api/block_period", methods=["GET"])
def get_block_period():
    args = request.args

    storage_observer.raise_event( event_type.info_log_writed(), f"Вызов get_block_period" ) 
    #logger.write(f"Вызов get_block_period")

    if "period" in args.keys():

        try:
            period = datetime.strptime(args["period"], "%Y-%m-%d")
            options.settings.block_period = period
            options.save()
        except:
           return error_proxy.create_error_response(app, "Некорректно перпеданы параметры: period", 400)    

    result = [options.settings.block_period.strftime('%Y-%m-%d')]
    return service.create_response(app, result)


if __name__ == "__main__":
    app.run(debug = True)