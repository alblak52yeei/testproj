from flask import Flask
from Src.Logics.report_factory import report_factory
from Src.Logics.start_factory import start_factory
from Src.settings_manager import settings_manager

app = Flask(__name__)

@app.route('/api/report/<storage_key>', methods = ['GET'])
def get_report(key: str):
    manager = settings_manager()
    start = start_factory(manager.settings)
    factory = report_factory()
    report = factory.create(manager.settings.report_format, start.storage)

    if key not in start.storage.data.keys():
        return "Такого ключа нет", 500

    data = report.create(key)

    response_data = app.response_class(response = data, status = 200, mimetype = 'application/text')