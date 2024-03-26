diff --git a/src/Logics/Process/abstract_process.py b/src/Logics/Process/abstract_process.py
deleted file mode 100644
index 3d3de40..0000000
--- a/src/Logics/Process/abstract_process.py
+++ /dev/null
@@ -1,8 +0,0 @@
-from abc import ABC, abstractmethod
-
-class abstract_process(ABC):
-    operations = {True: 1, False: -1}
-
-    @abstractmethod
-    def create(self):
-        pass
\ No newline at end of file
diff --git a/src/Logics/Process/process_factory.py b/src/Logics/Process/process_factory.py
deleted file mode 100644
index 6f2446a..0000000
--- a/src/Logics/Process/process_factory.py
+++ /dev/null
@@ -1,21 +0,0 @@
-from Src.Storage.storage import storage
-from Src.Logics.Process.process_storage_turn import process_storage_turn
-from Src.exceptions import operation_exception
-
-class process_factory:
-    __maps: dict = {}
-
-    def __init__(self):
-        self.__build_structure()
-
-
-    def __build_structure(self):
-        self.__maps[storage.process_turn_key()] = process_storage_turn
-
-
-    def create(self, format: str, storage_: storage):
-        if format not in self.__maps.keys():
-            raise operation_exception("Нет подходящего обработчика")
-
-        return self.__maps[format]
-        
\ No newline at end of file
diff --git a/src/Logics/Process/process_storage_turn.py b/src/Logics/Process/process_storage_turn.py
deleted file mode 100644
index 3e72908..0000000
--- a/src/Logics/Process/process_storage_turn.py
+++ /dev/null
@@ -1,7 +0,0 @@
-from Src.Logics.Process.abstract_process import abstract_process
-from Src.Models.storage_turn_model import storage_turn_model
-
-class process_storage_turn(abstract_process):
-    @classmethod
-    def create(cls, journal: list[storage_turn_model]):
-        return []
\ No newline at end of file
diff --git a/src/Logics/basic_convertor.py b/src/Logics/basic_convertor.py
index fae4787..d14eef4 100644
--- a/src/Logics/basic_convertor.py
+++ b/src/Logics/basic_convertor.py
@@ -1,8 +1,28 @@
 from Src.Logics.convertor import convertor
 
-
+#
+# Конвертор простых значений в словарь
+#
 class basic_convertor(convertor):
-    def convert(self, obj, field:str):
-        super().convert(obj, field)
-
-        return {field: obj} 
\ No newline at end of file
+   
+   def serialize(self, field: str, object) -> dict:
+      """
+            Подготовить словарь 
+        Args:
+            field (str): поле
+            object (_type_): значение
+      """
+      super().serialize( field, object)
+      
+      if not isinstance(object, (int, str, bool, float)):
+          self.error = f"Некорректный тип данных передан для конвертации. Ожидается: (int, str, bool). Передан: {type(object)}"
+          return None
+      
+      try:
+            return { field: object }
+      except Exception as ex:
+            self.set_error(ex)  
+            
+      return None        
+        
+    
\ No newline at end of file
diff --git a/src/Logics/convert_factory.py b/src/Logics/convert_factory.py
index 2bf1ef6..bef21ba 100644
--- a/src/Logics/convert_factory.py
+++ b/src/Logics/convert_factory.py
@@ -1,58 +1,135 @@
-fom Src.Logics.basic_convertor import basic_convertor
+from Src.Logics.basic_convertor import basic_convertor
 from Src.Logics.datetime_convertor import datetime_convertor
-from Src.Logics.reference_convertor import reference_convertor
+from Src.exceptions import exception_proxy, operation_exception
 from Src.reference import reference
-import datetime
+from Src.Logics.convertor import convertor
 
+import datetime
 
+#
+# Конвертор reference в словарь
+#
+class reference_convertor(convertor):
+    
+    def serialize(self, field: str, object: reference) -> dict:
+        """
+            Подготовить словарь 
+        Args:
+            field (str): поле
+            object (_type_): значение
+        """
+        super().serialize(field, object)
+        
+        factory = convert_factory()
+        return factory.serialize(object)
+    
+#
+# Фабрика для конвертация данных
+#
 class convert_factory:
-    maps = {}
-
-
-    def __init__(self):
-        self.maps[int] = basic_convertor
-        self.maps[str] = basic_convertor
-        self.maps[bool] = basic_convertor
-        self.maps[datetime] = datetime_convertor
-
-        for _ in reference.__subclasses__(): # связка
-            self.maps[_] = reference_convertor
-
-
-    def convert(self, obj) -> dict:
-        result = self.__convert_list('data', obj) # конвертируем список данных
-
+    _maps = {}
+    
+    def __init__(self) -> None:
+        # Связка с простыми типами
+        self._maps[datetime.datetime] = datetime_convertor
+        self._maps[int] = basic_convertor
+        self._maps[float] = basic_convertor
+        self._maps[str] = basic_convertor
+        self._maps[bool] = basic_convertor
+        
+        # Связка для всех моделей
+        for  inheritor in reference.__subclasses__():
+            self._maps[inheritor] = reference_convertor
+    
+        
+    def serialize(self, object) -> dict:
+        """
+            Подготовить словарь
+        Args:
+            object (_type_): произвольный тип
+
+        Returns:
+            dict: словарь
+        """
+        
+        # Сконвертируем данные как список
+        result = self.__convert_list("data", object)
         if result is not None:
             return result
-
+        
+        # Сконвертируем данные как значение
         result = {}
-
-        fields = reference.create_fields(obj)
-
+        fields = reference.create_fields(object)
+        
         for field in fields:
-            attr = getattr(obj.__class__, field)
-
-            if isinstance(attr, property):
-                value = getattr(obj, field)
-                dictionary =  self.__convert_list(field, value) # конвертируем список данных
-
+            attribute = getattr(object.__class__, field)
+            if isinstance(attribute, property):
+                value = getattr(object, field)
+                
+                # Сконвертируем данные как список
+                dictionary =  self.__convert_list(field, value)
                 if dictionary is None:
+                    # Сконвертируем данные как значение
                     dictionary = self.__convert_item(field, value)
-
+                    
                 if len(dictionary) == 1:
                     result[field] =  dictionary[field]
                 else:
-                    result[field] = dictionary
-
-        return result
-
-
-    def __convert_item(self, obj, field:str):
-        convertor = self.maps[type(obj)]()
-        dictionary = convertor.convert(field, obj)
-
-        return dictionary
-
-
-    def __convert_list(self, obj, field:str):
-        items = []
\ No newline at end of file
+                    result[field] = dictionary       
+          
+        return result  
+    
+    def __convert_item(self, field: str,  source):
+        """
+            Сконвертировать элемент        
+        Args:
+            field (str): Наименование поля
+            source (_type_): Значение
+
+        Returns:
+            dict: _description_
+        """
+        exception_proxy.validate(field, str)
+        if source is None:
+            return {field: None}
+        
+        if type(source) not in self._maps.keys():
+            raise operation_exception(f"Не возможно подобрать конвертор для типа {type(source)}")
+
+        # Определим конвертор
+        convertor = self._maps[ type(source)]()
+        dictionary = convertor.serialize( field, source )
+        
+        if not convertor.is_empty:
+            raise operation_exception(f"Ошибка при конвертации данных {convertor.error}")
+        
+        return  dictionary
+            
+    def __convert_list(self, field: str,  source) -> list:
+        """
+            Сконвертировать список
+        Args:
+            source (_type_): _description_
+
+        Returns:
+            dict: _description_
+        """
+        exception_proxy.validate(field, str)
+        
+        # Сконвертировать список
+        if isinstance(source, list):
+            result = []
+            for item in source:
+                result.append( self.__convert_item( field,  item ))  
+            
+            return result 
+        
+        # Сконвертировать словарь
+        if isinstance(source, dict):
+            result = {}
+            for key in source:
+                object = source[key]
+                value = self.__convert_item( key,  object )
+                result[key] = value
+                
+            return result    
diff --git a/src/Logics/convertor.py b/src/Logics/convertor.py
index 9081e67..7ad4182 100644
--- a/src/Logics/convertor.py
+++ b/src/Logics/convertor.py
@@ -1,7 +1,25 @@
-from abc import abstractmethod
+import abc
+from Src.errors import error_proxy
+from Src.exceptions import exception_proxy
 
-
-class convertor:
-    @abstractmethod
-    def convert(self, obj, field) -> dict:
-        pass 
\ No newline at end of file
+# 
+# Абстрактный класс для наследования.
+# Используется для формирования набора словарей. 
+#
+class convertor(error_proxy):
+    
+    @abc.abstractmethod
+    def serialize(self, field: str, object) -> dict:
+        """
+            Сконвертировать объект в словарь
+        Args:
+            source (_type_): Любой тип данных
+        """
+        exception_proxy.validate(field, str)
+        self.clear()
+         
+        
+        
+        
+        
+    
diff --git a/src/Logics/csv_reporting.py b/src/Logics/csv_reporting.py
index 4e56f13..fb102e0 100644
--- a/src/Logics/csv_reporting.py
+++ b/src/Logics/csv_reporting.py
@@ -1,30 +1,43 @@
 from Src.Logics.reporting import reporting
+from Src.exceptions import operation_exception
 
-class csv_reporting(reporting):
-    def create(self, key: str) -> str:
-        data = self.data
-        keys = []
-
-        # Получаем список всех атрибутов и проходим по ним
-        attrs = dir(data[key][0]) 
 
-        for attr in attrs:
-            if not attr.startswith("_") or attr.startswith("create_"):
-                keys.append(attr)
-
-        self.fields = keys
+#
+# Класс - реализация построение данных в формате csv
+#
+class csv_reporting(reporting):
+    
+    def create(self, storage_key: str):
+        super().create(storage_key)
+        result = ""
+        delimetr = ";"
 
-        data = self.data[key]
-        headers = "; ".join(self.fields)
-        result = headers + '\n'
+        # Исходные данные
+        items = self.data[ storage_key ]
+        if items == None:
+            raise operation_exception("Невозможно сформировать данные. Данные не заполнены!")
         
-        for element in data:
+        if len(items) == 0:
+            raise operation_exception("Невозможно сформировать данные. Нет данных!")
+        
+        # Заголовок 
+        header = delimetr.join(self.fields)
+        result += f"{header}\n"
+        
+        # Данные
+        for item in items:
             row = ""
-
             for field in self.fields:
-                val = getattr(element, field)
-                row += f"{val}; "
-
-            result += row[:-1] + '\n'
+                attribute = getattr(item.__class__, field)
+                if isinstance(attribute, property):
+                    value = getattr(item, field)
+                    if isinstance(value, (list, dict)) or value is None:
+                        value = ""
+                        
+                    row +=f"{value}{delimetr}"
+                
+            result += f"{row[:-1]}\n"
+            
         
+        # Результат csv
         return result
\ No newline at end of file
diff --git a/src/Logics/datetime_convertor.py b/src/Logics/datetime_convertor.py
index a01f1d5..2ee90ac 100644
--- a/src/Logics/datetime_convertor.py
+++ b/src/Logics/datetime_convertor.py
@@ -1,9 +1,27 @@
 from Src.Logics.convertor import convertor
-import datetime
+from datetime import datetime
 
 
+#
+# Конвертор datetime в словарь
+#
 class datetime_convertor(convertor):
-    def convert(self, obj, field:str):
-        super().convert(obj, field)
-
-        return { field: obj.strftime('%Y-%m-%d') } 
\ No newline at end of file
+    
+    def serialize(self, field: str,  object):
+        """
+            Подготовить словарь 
+        Args:
+            field (str): поле
+            object (_type_): значение
+        """
+        super().serialize( field, object)
+      
+        if not isinstance(object, datetime):
+          self._error.error = f"Некорректный тип данных передан для конвертации. Ожидается: datetime. Передан: {type(object)}"
+          return None
+      
+        try:
+            return { field: object.strftime('%Y-%m-%d') }
+        except Exception as ex:
+            self.set_error(ex)    
+        
\ No newline at end of file
diff --git a/src/Logics/json_reporting.py b/src/Logics/json_reporting.py
index 2b59a6f..f8e9c49 100644
--- a/src/Logics/json_reporting.py
+++ b/src/Logics/json_reporting.py
@@ -1,25 +1,38 @@
 from Src.Logics.reporting import reporting
 from Src.exceptions import operation_exception
+from Src.Logics.convert_factory import convert_factory
+
 import json
 
+#
+# Формирование отчета в формате json
+#
 class json_reporting(reporting):
-    def create(self, typeKey: str):
-        super().create(typeKey)
-        result = []
-        # Исходные данные
-        items = self.data[ typeKey ]
+    
+      def create(self, storage_key: str):
+        super().create(storage_key)
+        
+         # Исходные данные
+        items = self.data[ storage_key ]
         if items == None:
             raise operation_exception("Невозможно сформировать данные. Данные не заполнены!")
-
+        
         if len(items) == 0:
             raise operation_exception("Невозможно сформировать данные. Нет данных!")
-
-        data = {}
-        for item in items:
-            for field in self.fields:
-                value = getattr(item, field)
-                data[ field ] = value
-                result.append( data )        
-
-        data = json.dumps( result )
-        return data 
+        
+        # Сериализуем данные
+        factory = convert_factory()
+        data = factory.serialize( items )
+        
+        # Формируем Json
+        result = json.dumps(data, sort_keys = True, indent = 4, ensure_ascii = False)  
+        return result
+      
+      def mimetype(self) -> str:
+          return "application/json; charset=utf-8"     
+                
+        
+        
+        
+    
+    
\ No newline at end of file
diff --git a/src/Logics/markdown_reporting.py b/src/Logics/markdown_reporting.py
index 79b0c22..7a0aebe 100644
--- a/src/Logics/markdown_reporting.py
+++ b/src/Logics/markdown_reporting.py
@@ -3,12 +3,12 @@ from Src.exceptions import operation_exception
 
 class markdown_reporting(reporting):
     
-      def create(self, typeKey: str):
-        super().create(typeKey)
+      def create(self, storage_key: str):
+        super().create(storage_key)
         result = []
 
         # Исходные данные
-        items = self.data[ typeKey ]
+        items = self.data[ storage_key ]
         if items == None:
             raise operation_exception("Невозможно сформировать данные. Данные не заполнены!")
         
@@ -17,7 +17,7 @@ class markdown_reporting(reporting):
             raise operation_exception("Невозможно сформировать данные. Нет данных!")
         
         # Заголовок
-        result.append(f"# {typeKey}")
+        result.append(f"# {storage_key}")
         
         # Шапка таблицы
         header = ""
@@ -33,11 +33,17 @@ class markdown_reporting(reporting):
         for item in items:
             row = ""
             for field in self.fields:
-                value = getattr(item, field)
-                if value is None:
-                    value = ""
-                    
-                row +=f"|{value}"    
+                attribute = getattr(item.__class__, field)
+                if isinstance(attribute, property):
+                    value = getattr(item, field)
+                    if isinstance(value, (list, dict)) or value is None:
+                        value = ""
+                        
+                    row +=f"|{value}"  
+                
             result.append(f"{row}|")
             
-        return "\n".join(result)        
\ No newline at end of file
+        return "\n".join(result)        
+    
+     
+    
\ No newline at end of file
diff --git a/src/Logics/reference_convertor.py b/src/Logics/reference_convertor.py
deleted file mode 100644
index 5c4c8db..0000000
--- a/src/Logics/reference_convertor.py
+++ /dev/null
@@ -1,7 +0,0 @@
-from Src.Logics.convertor import convertor
-from Src.Logics.convert_factory import convert_factory
-
-
-class reference_convertor(convertor):
-    def convert(self, obj, field:str):
-        return convert_factory().convert(object)
\ No newline at end of file
diff --git a/src/Logics/report_factory.py b/src/Logics/report_factory.py
index 0cd6641..e0e2914 100644
--- a/src/Logics/report_factory.py
+++ b/src/Logics/report_factory.py
@@ -1,35 +1,91 @@
 from Src.Logics.reporting import reporting
-from Src.Logics.markdown_reporting import markdown_reporting
+from Src.Logics .markdown_reporting import markdown_reporting
 from Src.Logics.csv_reporting import csv_reporting
+from Src.Logics.json_reporting import json_reporting
 from Src.exceptions import exception_proxy, argument_exception, operation_exception
 
-# Фабрика для отчётов
+#
+# Фабрика для отчетов
+#
 class report_factory:
     __maps = {}
-
+    
+    # Формат данных для экспорт в Web сервер
+    __mimetype: str
+    
     def __init__(self) -> None:
-        self.__build_structure()
-        
+       self.__build_structure()
+
     def __build_structure(self):
         """
             Сформировать структуру
         """
-        self.__maps["csv"] = csv_reporting
+        self.__maps["csv"]  = csv_reporting
         self.__maps["markdown"] = markdown_reporting
+        self.__maps["json"] = json_reporting
+      
+    @property  
+    def mimetype(self):
+        """
+           Формат данных для экспорт в Web сервер 
+        Returns:
+            _type_: _description_
+        """
+        return self.__mimetype
+      
+    def create(self, format: str, data:dict) -> reporting:
+        """
+            Сформировать объект для построения отчетности
+        Args:
+            format (str): Тип формта
+            data (_type_): Словарь с данными
 
-    def create(self, format: str, data) -> reporting:
+        Returns:
+            reporting: _description_
+        """
         exception_proxy.validate(format, str)
-
-        if data is None:
-            raise argument_exception("Данные не переданы")
+        exception_proxy.validate(data, dict)
         
         if len(data) == 0:
-            raise argument_exception("Данные пустые")
+            raise argument_exception("Пустые данные")
         
         if format not in self.__maps.keys():
-            raise operation_exception("Такого формата не существует")
+            raise operation_exception(f"Для {format} нет обработчика") 
+        
+        # Получаем тип связанный с форматом
+        report_type = self.__maps[format]
+        # Получаем объект 
+        result = report_type(data)
+        self.__mimetype = result.mimetype()
         
-        result_type = self.__maps[format]
-        result = result_type(data)
+        return result 
+             
+    def create_response(self, format: str, data:dict, storage_key: str,  app):
+        """
+            Сформировать отчет и вывести его в формате response_class для Web сервера
+        Args:
+            format (str): тип формата: csv, markdown, json
+            data (dict): исходные данные
+            storage_key (str): ключ для отбора данных в storage
+            app (_type_): Flask приложение
+        Returns:
+            response_class: _description_
+        """
+        if app is None:
+            raise argument_exception("Некорректно переданы параметры!")
+        exception_proxy.validate(storage_key, str)
 
-        return result
\ No newline at end of file
+        # Получаем нужный отчет        
+        report = self.create(format, data)
+        # Формируем данные
+        info = report.create(storage_key)
+        
+        # Подготовить ответ    
+        result = app.response_class(
+            response = f"{info}",
+            status = 200,
+            mimetype = self.mimetype
+        )
+        
+        return result
+      
\ No newline at end of file
diff --git a/src/Logics/reporting.py b/src/Logics/reporting.py
index 9fd777b..2089f7f 100644
--- a/src/Logics/reporting.py
+++ b/src/Logics/reporting.py
@@ -1,27 +1,96 @@
-from abc import abstractmethod, ABC
+import abc 
 from Src.settings import settings
+from Src.exceptions import exception_proxy, operation_exception
+from Src.reference import reference
 
-class reporting(ABC):
-    _settings : settings
-    _data : dict
-    _fields : list
 
-    @abstractmethod
-    def create(self, key:str) -> str:
-        pass
+#
+# Абстрактный класс для реализации отчетности
+#
+class reporting(abc.ABC):
+    # Набор данных
+    __data = {}
+    # Список полей
+    __fields = []    
+
+    
+    def __init__(self, _data):
+        """
+
+        Args:
+            _data (_type_): Словарь с данными
+        """
+        
+        exception_proxy.validate(_data, dict)
+        self.__data = _data
+        
+
+    @abc.abstractmethod
+    def create(self, storage_key: str):
+        """
+            Сформировать отчет
+        Args:
+            storage_key (str): Ключ для отбора данных
+        """
+        exception_proxy.validate(storage_key, str)
+        self.__fields = self.build(storage_key, self.__data)
+        
+        return ""
+    
+    def mimetype(self) -> str:
+        """
+          Тип данных для формирования ответа Web сервера
+        Returns:
+            str: _description_
+        """
+        return "application/text"    
     
-    def __init__(self, settings_:settings, data_) -> None:
-        self._settings = settings_
-        self._data = data_
+    @staticmethod
+    def build( storage_key: str, data: dict) -> list:
+        """
+            Предобработка. Получить набор полей
+        Args:
+            storage_key (str): ключ в словаре_
+            data (dict): Данные - словарь
 
+        Returns:
+            list: список
+        """
+        
+        exception_proxy.validate(storage_key, str)
+        if data is None:
+            raise operation_exception("Набор данных не определен!")
+        
+        if len(data) == 0:
+            raise operation_exception("Набор данных пуст!")
+        
+        item = data[storage_key][0]
+        result = reference.create_fields( item )
+        return result    
+    
+    def _build(self, storage_key: str) -> list:
+        """
+           Предобработка данных. Возвращает набор полей класса typeKey
+        Args:
+            storage_key (str): ключ для выборки данных
+        Returns:
+            list: список
+        """
+        return reporting.build(storage_key, self.__data)
+        
+        
+    @property    
+    def fields(self) -> list:
+        """
+        Набор полей от исходного объекта на основании которого формируем отчет
+        """    
+        return self.__fields    
+            
     @property         
     def data(self) -> dict:
-        return self._data
+        """
 
-    @property
-    def fields(self) -> list:
-        return self._fields
-    
-    @fields.setter
-    def fields(self, val) -> list:
-        self._fields = val
\ No newline at end of file
+        Returns:
+            dict: словарь с данными
+        """
+        return self.__data    
\ No newline at end of file
diff --git a/src/Logics/start_factory.py b/src/Logics/start_factory.py
index 0c74f68..20811b7 100644
--- a/src/Logics/start_factory.py
+++ b/src/Logics/start_factory.py
@@ -1,113 +1,294 @@
-
+# Модели
 from Src.Models.group_model import group_model
-from Src.Models.nomenclature_model import nomenclature_model
 from Src.Models.unit_model import unit_model
+from Src.Models.nomenclature_model import nomenclature_model
+from Src.reference import reference
+from Src.Models.receipe_model import receipe_model
+from Src.Models.storage_row_model import storage_row_model
+from Src.Models.storage_model import storage_model
+
+# Системное
 from Src.settings import settings
 from Src.Storage.storage import storage
-from Src.Models.reciepe_model import reciepe_model
-from Src.Models.reciepe_row import reciepe_row_model
+from Src.exceptions import exception_proxy, operation_exception, argument_exception
 
+#
+# Класс для обработки данных. Начало работы приложения
+#
 class start_factory:
-    __options: settings = None
+    __oprions: settings = None
     __storage: storage = None
     
-    def __init__(self, _options: settings, _storage: storage = None) -> None:
-        self.__options = _options
+    def __init__(self, _options: settings,
+                 _storage: storage = None) -> None:
+        
+        exception_proxy.validate(_options, settings)
+        self.__oprions = _options
         self.__storage = _storage
-
-        self.__build()
+        
     
-    def create(self):
-        result = []
-
-        if not self.__options.is_first_start: return result
-
-        self.__options.is_first_start = False
-
-        items = start_factory.create_nomenclature()
-
-        result += items
-        result += set([v.unit for v in items])
-        result += set([v.group for v in items])
-        result += start_factory.create_reciepes()
-
-        return result
-
-    def __build(self):
+    def __save(self, key:str, items: list):
+        """
+            Сохранить данные
+        Args:
+            key (str): ключ доступ
+            items (list): список
+        """
+        exception_proxy.validate(key, str)
+        
         if self.__storage == None:
             self.__storage = storage()
-
-        items = start_factory.create_nomenclature()
-
-        self.__storage.data[storage.nomenclature_key()] = items
-        self.__storage.data[storage.unit_key()] = set([v.unit for v in items])
-        self.__storage.data[storage.group_key()] = set([v.group for v in items])
-
-    @property
+            
+        self.__storage.data[ key ] = items
+        
+    @property            
     def storage(self):
+        """
+             Ссылка на объект хранилище данных
+        Returns:
+            _type_: _description_
+        """
         return self.__storage
     
+    # Статические методы
+    
     @staticmethod
-    def create_nomenclature():
+    def create_units() -> list:
+        """
+            Сформировать список единиц измерения
+        Returns:
+            _type_: _description_
+        """
+        items = []
+        items.append( unit_model.create_gram() )
+        items.append( unit_model.create_killogram() )
+        items.append( unit_model.create_liter() )
+        items.append( unit_model.create_milliliter() )
+        items.append( unit_model.create_ting() )
+        
+        return items
+    
+    @staticmethod
+    def create_nomenclatures() -> list:
+        """
+          Сформировать список номенклатуры
+        """
+        
+        group = group_model.create_default_group()
+        items = [ {"Мука пшеничная": "киллограмм"}, 
+                  {"Сахар":"киллограмм"}, 
+                  {"Сливочное масло" : "киллограмм"}, 
+                  {"Яйца": "штука"}, {"Ванилин": "грамм"}, 
+                  {"Куринное филе": "киллограмм"}, 
+                  {"Салат Романо": "грамм"},
+                  {"Сыр Пармезан" : "киллограмм"}, 
+                  {"Чеснок": "киллограмм"}, 
+                  {"Белый хлеб": "киллограмм"},
+                  {"Соль": "киллограмм"}, {"Черный перец": "грамм"}, 
+                  {"Оливковое масло": "литр"}, 
+                  {"Лимонный сок": "литр"},
+                  {"Горчица дижонская": "грамм"},
+                  {"Сахарная пудра": "грамм"},{"Ванилиин": "грамм"},
+                  {"Корица": "грамм"},
+                  {"Какао": "киллограмм"}]
+        
+        # Подготовим словарь со список единиц измерения
+        units = reference.create_dictionary(start_factory.create_units())
+        
+        result = []
+        for position in items:
+            # Получаем список кортежей и берем первое значение
+            _list =  list(position.items())
+            if len(_list) < 1:
+                raise operation_exception("Невозможно сформировать элементы номенклатуры! Некорректный список исходных элементов!")
+            
+            tuple = list(_list)[0]
+            
+            # Получаем неименование номенклатуры и единицы измерения
+            if len(tuple) < 2:
+                raise operation_exception("Невозможно сформировать элемент номенклатуры. Длина кортежа не корректна!")
+            
+            name   = tuple[0]
+            unit_name = tuple[1]
+            
+            if not unit_name in units.keys():
+                raise operation_exception(f"Невозможно найти в списке указанную единицу измерения {unit_name}!")
+            
+            # Создаем объект - номенклатура
+            item = nomenclature_model( name, group, units[unit_name])
+            result.append(item)
+          
+        return result
+      
+    @staticmethod      
+    def create_groups() -> list:
+        """
+            Сформировать список групп номенклатуры
+        Returns:
+            _type_: _description_
+        """
+        items = []
+        items.append( group_model.create_default_group())
+        return items         
+    
+    @staticmethod
+    def create_receipts(_data: list = None) -> list:
+        """
+            Сформировать список рецептов
+        Args:
+            _data (list, optional): Список номенклатуры. Defaults to None.
 
-        nomenclature_group = group_model.create_group()
+        Raises:
+            argument_exception: _description_
 
-        return [
-            nomenclature_model("Пшеничная мука", unit_model.create_kilogramm(), nomenclature_group),
-            nomenclature_model("Сахар", unit_model.create_kilogramm(), nomenclature_group),
-            nomenclature_model("Сливочное масло", unit_model.create_mililiter(), nomenclature_group),
-            nomenclature_model("Яйца", unit_model.create_count(), nomenclature_group),
-            nomenclature_model("Ванилин", unit_model.create_gramm(), nomenclature_group),
-            nomenclature_model("Яичный белок", unit_model.create_count(), nomenclature_group),
-            nomenclature_model("Сахарная пудра", unit_model.create_gramm(), nomenclature_group),
-            nomenclature_model("Корица", unit_model.create_gramm(), nomenclature_group),
-            nomenclature_model("Какао", unit_model.create_mililiter(), nomenclature_group),
-            nomenclature_model("Куриное филе", unit_model.create_kilogramm(), nomenclature_group),
-            nomenclature_model("Салат Романо", unit_model.create_count(), nomenclature_group),
-            nomenclature_model("Сын Пармезан", unit_model.create_gramm(), nomenclature_group),
-            nomenclature_model("Чеснок", unit_model.create_gramm(), nomenclature_group),
-            nomenclature_model("Белый хлеб", unit_model.create_gramm(), nomenclature_group),
-            nomenclature_model("Соль", unit_model.create_gramm(), nomenclature_group),
-            nomenclature_model("Чёрный перец", unit_model.create_gramm(), nomenclature_group),
-            nomenclature_model("Оливковое масло", unit_model.create_liter(), nomenclature_group),
-            nomenclature_model("Лимонный сок", unit_model.create_liter(), nomenclature_group),
-            nomenclature_model("Горчица дижонская", unit_model.create_gramm(), nomenclature_group),
-        ]
-    
+        Returns:
+            _type_: Массив объектов receipe_model
+        """
+        result = []
+        
+        if _data is None:
+            data = start_factory.create_nomenclatures()
+        else:
+            data = _data
+            
+        if len(data) == 0:
+            raise argument_exception("Некорректно переданы параметры! Список номенклатуры пуст.")        
+        
+        # Вафли хрустящие в вафильнице
+        items = [ {"Мука пшеничная": 100}, {"Сахар": 80}, {"Сливочное масло": 70},
+                  {"Яйца": 1} , {"Ванилин": 5 }
+                ]
+        item = receipe_model.create_receipt("Вафли хрустящие в вафильнице", "", items, data)
+        
+        # Шаги приготовления
+        item.instructions.extend([
+            "Масло положите в сотейник с толстым дном. Растопите его на маленьком огне на плите, на водяной бане либо в микроволновке.",
+            "Добавьте в теплое масло сахар. Перемешайте венчиком до полного растворения сахара. От тепла сахар довольно быстро растает.",
+            "Добавьте в масло яйцо. Предварительно все-таки проверьте масло, не горячее ли оно, иначе яйцо может свариться. Перемешайте яйцо с маслом до однородности.",
+            "Всыпьте муку, добавьте ванилин.",
+            "Перемешайте массу венчиком до состояния гладкого однородного теста."])
+        
+        item.comments = "Время приготовления: 20 мин. 8 порций"
+        result.append( item )
+        
+        # Цезарь с курицей
+        items = [ {"Куринное филе": 200}, {"Салат Романо": 50}, {"Сыр Пармезан": 50},
+                  {"Чеснок": 10} , {"Белый хлеб": 30 }, {"Соль": 5}, {"Черный перец": 2},
+                  {"Оливковое масло": 10}, {"Лимонный сок": 5}, {"Горчица дижонская": 5},
+                  {"Яйца": 2}
+                ]
+        item =  receipe_model.create_receipt("Цезарь с курицей", "", items, data)
+        item.instructions.extend([
+            "Нарезать куриное филе кубиками, нарубите чеснок, нарежьте хлеб на кубики."
+            "Очистить салат и обсушить его."
+            "Натереть сыр Пармезан на терке."
+            "Обжарить на сковороде куриное филе с чесноком до готовности."
+            "На той же сковородке обжарьить кубики хлеба до золотистости."
+            "В миске смешайте оливковое масло, лимонный сок, горчицу, измельченный чеснок, соль и перец."
+            "В большой миске смешайте кубики курицы, хлеба, листья салата."
+            "Добавить заправку и тщательно перемешать"])
+            
+        result.append(item)
+        
+        # Безе
+        items = [ {"Яйца": 3}, {"Сахарная пудра":180}, {"Ванилиин" : 5}, {"Корица": 5} ,{"Какао": 20} ]
+        result.append( receipe_model.create_receipt("Безе", "", items, data))
+        return result
+        
     @staticmethod
-    def create_reciepes():
-        return [
-            reciepe_model(
-                'ВАФЛИ ХРУСТЯЩИЕ В ВАФЕЛЬНИЦЕ',
-            reciepe_row_model(
-                nomenculature = nomenclature_model('Пшеничная мука', unit_model.create_kilogramm(), group_model.create_group()),
-                unit=unit_model.create_gramm(),
-                size=100),
-            reciepe_row_model(
-                nomenculature = nomenclature_model('Сахар', unit_model.create_kilogramm(), group_model.create_group()),
-                unit=unit_model.create_gramm(),
-                size=80),
-            reciepe_row_model(
-                nomenculature = nomenclature_model('Сливочное масло', unit_model.create_gramm(), group_model.create_group()),
-                unit=unit_model.create_gramm(),
-                size=70),
-            reciepe_row_model(
-                nomenculature = nomenclature_model('Яйца', unit_model.create_count(), group_model.create_group()),
-                unit=unit_model.create_count(),
-                size=1),
-            reciepe_row_model(
-                nomenculature = nomenclature_model('Ванилин', unit_model.create_gramm(), group_model.create_group()),
-                unit=unit_model.create_gramm(),
-                size=5),
-            description='''
-Время приготовления: 20 мин
-Как испечь вафли хрустящие в вафельнице? Подготовьте необходимые продукты. Из данного количества у меня получилось 8 штук диаметром около 10 см.
-Масло положите в сотейник с толстым дном. Растопите его на маленьком огне на плите, на водяной бане либо в микроволновке.
-Добавьте в теплое масло сахар. Перемешайте венчиком до полного растворения сахара. От тепла сахар довольно быстро растает.
-Добавьте в масло яйцо. Предварительно все-таки проверьте масло, не горячее ли оно, иначе яйцо может свариться. Перемешайте яйцо с маслом до однородности.
-Всыпьте муку, добавьте ванилин.
-Перемешайте массу венчиком до состояния гладкого однородного теста.
-Разогрейте вафельницу по инструкции к ней. У меня очень старая, еще советских времен электровафельница. Она может и не очень красивая, но печет замечательно! Я не смазываю вафельницу маслом, в тесте достаточно жира, да и к ней уже давно ничего не прилипает. Но вы смотрите по своей модели. Выкладывайте тесто по столовой ложке. Можно класть немного меньше теста, тогда вафли будут меньше и их получится больше.
-Пеките вафли несколько минут до золотистого цвета. Осторожно откройте вафельницу, она очень горячая! Снимите вафлю лопаткой. Горячая она очень мягкая, как блинчик. Но по мере остывания становится твердой и хрустящей. Такие вафли можно свернуть трубочкой. Но делать это надо сразу же после выпекания, пока она мягкая и горячая, потом у вас ничего не получится, вафля поломается. Приятного аппетита!
-            ''')
-        ]
\ No newline at end of file
+    def create_storage_transactions(data: dict) -> list:
+        """
+            Сформировать список складских транзакций
+        Returns:
+            _type_: Массив объектов storage_row_model
+        """
+        result = []
+        default_storage = storage_model.create_default()
+            
+        if len(data.keys()) == 0:
+            raise operation_exception("Набор данных пуст. Невозможно сформировать список транзакций!")  
+        
+        items = [ { "Мука пшеничная": [1, "киллограмм"] }, 
+                  { "Черный перец": [50, "грамм" ] },
+                  { "Сахар" :[0.5, "киллограмм"] },
+                  { "Яйца": [6,"штука" ] },
+                  { "Оливковое масло": [0.2,"литр" ] },
+                  { "Куринное филе": [0.5, "киллограмм"] },
+                  { "Салат Романо": [1, "штука"] },
+                  { "Белый хлеб" : [3, "штука"] },
+                  { "Сыр Пармезан": [0.2, "киллограмм" ] },
+                  { "Горчица дижонская" : [0.1, "литр"] },
+                  { "Черный перец": [10, "грамм" ] },
+                  { "Лимонный сок": [1, "литр"] },
+                  { "Какао": [1,"киллограмм"] },
+                  { "Сыр Пармезан": [0.3, "киллограмм" ] },
+                  { "Ванилиин": [100, "грамм"] }  ]
+        
+        for element in items:
+            key = list(element.keys())[0]
+            values = list(element.values())[0]
+            
+            row = storage_row_model.create_credit_row(key, values, data, default_storage)
+            result.append(row)
+        
+        return result
+        
+    @staticmethod
+    def create_storages():
+        storages = []
+        
+        # Добавляем в список складов два склада
+        storages.append(storage_model('Первый склад', 'ул. Советская, д. 31'))
+        storages.append(storage_model('Второй склад', 'ул. Карла Либкнехта, д. 128'))
+        
+        return storages
+    
+    # Основной метод
+    def create(self) -> bool:
+        """
+           В зависимости от настроек, сформировать или загрузить набор данных
+        Returns:
+            _type_: _description_
+        """
+        if self.__oprions.is_first_start == True:
+            # 1. Формируем и зпоминаем номеклатуру
+            nomenclatures = start_factory.create_nomenclatures()
+            self.__save( storage.nomenclature_key(), nomenclatures )
+            
+            # 2. Формируем и запоминаем рецепты
+            items = start_factory.create_receipts(nomenclatures)
+            self.__save( storage.receipt_key(), items)
+      
+            # 3. Формируем и запоминаем единицы измерения
+            items = start_factory.create_units()
+            self.__save( storage.unit_key(), items)
+            
+            # 4. Формируем и запоминаем группы номенклатуры
+            items = start_factory.create_groups()
+            self.__save( storage.group_key(), items)
+            
+            # 5. Формируем типовые складские проводки
+            items = start_factory.create_storage_transactions( self.storage.data )
+            self.__save( storage.storage_transaction_key(), items)
+            
+            # 6. Формируем склады
+            items = start_factory.create_storages()
+            self.__save( storage.storages_key(), items)
+
+            return True
+           
+           
+        else:
+            # Другой вариант. Загрузка из источника данных    
+            return False
+        
+        
+    
+        
+        
+        
+        
+    
+    
+    
+    
\ No newline at end of file
diff --git a/src/Logics/storage_prototype.py b/src/Logics/storage_prototype.py
index 6f6639d..3e859c0 100644
--- a/src/Logics/storage_prototype.py
+++ b/src/Logics/storage_prototype.py
@@ -62,7 +62,7 @@ class storage_prototype(error_proxy):
 
             result.append(item)
 
-        return storage_prototype(result)
+        return storage_prototype(result) 
     
     @property
     def data(self):
diff --git a/src/Logics/storage_service.py b/src/Logics/storage_service.py
index 221a627..302120f 100644
--- a/src/Logics/storage_service.py
+++ b/src/Logics/storage_service.py
@@ -63,7 +63,7 @@ class storage_service:
                 raise operation_exception('Не удалось произвести списывание. Недостаточно остатков на складе')
             
             item = storage_row_model("Test")
-            item.nomenclature = turn.nomenclature
+            item.nomenclature = turn.nomenclature 
             item.unit = turn.unit
             item.storage_type = False
             item.value = recipe_need[turn.nomen.name]
diff --git a/src/Storage/storage.py b/src/Storage/storage.py
index fbb8f85..40c5888 100644
--- a/src/Storage/storage.py
+++ b/src/Storage/storage.py
@@ -1,29 +1,95 @@
-
-
-
+#
+# Класс хранилище данных
+#
 class storage:
     __data = {}
     
+    
     def __new__(cls):
         if not hasattr(cls, 'instance'):
             cls.instance = super(storage, cls).__new__(cls)
-            
         return cls.instance  
     
     @property
-    def data(self):
+    def data(self) -> dict:
+        """
+         Данные по моделям
+
+        Returns:
+            _type_: _description_
+        """
         return self.__data
-    
+
+ 
     @staticmethod
     def nomenclature_key():
-        return "nomenclature"
-    
+        """
+            Ключ для хранения номенклатуры
+        Returns:
+            _type_: _description_
+        """
+        return "nomenclatures"
+
+  
     @staticmethod
     def group_key():
-        return "group"
-    
+        """
+            Списк номенклатурных групп
+        Returns:
+            _type_: _description_
+        """
+        return "groups"
+      
+      
     @staticmethod
+    def storage_transaction_key():
+        """
+            Список складских проводок
+        Returns:
+            _type_: _description_
+        """
+        return "transactions"  
+          
+    @staticmethod
+    def storages_key():
+        """
+            Список складов
+        Returns:
+            _type_: _description_
+        """
+        return "storages"  
+
+    @staticmethod  
     def unit_key():
-        return "unit"
+        """
+              Список единиц измерения
+        Returns:
+            _type_: _description_
+        """
+        return "units"
     
+    @staticmethod
+    def receipt_key():
+        """
+            Список рецептов
+        Returns:
+            _type_: _description_
+        """
+        return "receipts"
+    
+    # Код взят: https://github.com/UpTechCompany/GitExample/blob/6665bc70c4933da12f07c0a0d7a4fc638c157c40/storage/storage.py#L30
+    
+    @staticmethod
+    def storage_keys(cls):
+        """
+            Получить список ключей
+        Returns:
+            _type_: _description_
+        """
+        keys = []
+        methods = [getattr(cls, method) for method in dir(cls) if callable(getattr(cls, method))]
+        for method in methods:
+            if method.__name__.endswith("_key") and callable(method):
+                keys.append(method())
+        return keys
     
\ No newline at end of file
diff --git a/src/argument_exception.py b/src/argument_exception.py
deleted file mode 100644
index fb82930..0000000
--- a/src/argument_exception.py
+++ /dev/null
@@ -1,12 +0,0 @@
-from src.error_proxy import error_proxy
-
-class argument_exception(Exception):
-    __inner_error: error_proxy = error_proxy()
-
-    def __init__(self, *args: object) -> None:
-        super().__init__(*args)
-        self.__inner_error.set_error(self)
-
-    @property
-    def error(self):
-        return self.__inner_error
\ No newline at end of file
diff --git a/src/error_proxy.py b/src/error_proxy.py
deleted file mode 100644
index 4613df9..0000000
--- a/src/error_proxy.py
+++ /dev/null
@@ -1,75 +0,0 @@
-class error_proxy:
-    __error_text = ""
-    __error_source = ""
-    __is_error = False
-
-    def __init__(self, error_text: str = "", error_source: str = "") -> None:
-        self.__error_source = error_proxy
-        self.error_text = error_text
-    
-    @property
-    def error_text(self):
-        """
-            Текст сообщения
-        """
-        
-        return self.__error_text
-    
-    @error_text.setter
-    def error_text(self, value: str):
-        if not isinstance(value, str):
-            raise Exception("ERROR: Некорректно передан аргумент")
-        
-        value = value.strip()
-
-        if value == "":
-            self.__is_error = False
-            return
-        
-        self.__error_text = value
-        self.__is_error = True
-
-    @property
-    def error_source(self):
-        """
-            Источник ошибки
-        """
-                
-        return self.__error_source
-    
-    @error_source.setter
-    def error_source(self, value: str):
-        if not isinstance(value, str):
-            raise Exception("ERROR: Некорректно передан аргумент")
-        
-        value = value.strip()
-
-        if value == "":
-            return
-        
-        self.__error_source = value
-
-    @property
-    def is_error(self):
-        """
-            Флаг. Есть ли ошибка
-        """
-        
-        return self.__is_error
-    
-    def set_error(self, exception: Exception):
-        """
-            Сохранить ошибку
-        """
-    
-        if not isinstance(self, Exception):
-            self.error_text = "Некорректно переданы параметры!"
-            self.error_source = "set_error"
-
-            return
-
-        if exception is not None:
-            self.error_text = f"ОШИБКА! {str(exception)}"
-            self.error_source = f"ИСКЛЮЧЕНИЕ! {type(exception)}"
-        else:
-            self.error_text = ""
\ No newline at end of file
diff --git a/src/errors.py b/src/errors.py
index 56d7a5b..cb29788 100644
--- a/src/errors.py
+++ b/src/errors.py
@@ -1,4 +1,4 @@
-# Набор классов для обработки информации связанной с ошибками
+import json
 
 #
 # Класс для обработки и хранения текстовой информации об ошибке
@@ -51,5 +51,44 @@ class error_proxy:
         if len(self._error_text) != 0:
             return False
         else:
-            return True         
+            return True       
+        
+    def clear(self):
+        """
+            Очистить
+        """
+        self._error_text = "" 
+        
+    @staticmethod    
+    def create_error_response( app,  message: str, http_code: int = 0):
+        """
+            Сформировать структуру response_class для описания ошибки
+        Args:
+            app (_type_): Flask
+            message (str): Сообщение
+            http_code(int): Код возврата
+
+        Returns:
+            response_class: _description_
+        """
+        
+        if app is None:
+            raise Exception("Некорректно переданы параметры!")
+        
+        if http_code == 0:
+            code = 500
+        else:
+            code = http_code
+        
+        # Формируем описание        
+        json_text = json.dumps({"details" : message}, sort_keys = True, indent = 4,  ensure_ascii = False)  
+        
+        # Формируем результат
+        result = app.response_class(
+            response =   f"{json_text}",
+            status = code,
+            mimetype = "application/json; charset=utf-8"
+        )    
+        
+        return result
             
\ No newline at end of file
diff --git a/src/exceptions.py b/src/exceptions.py
index 2649c40..552326c 100644
--- a/src/exceptions.py
+++ b/src/exceptions.py
@@ -38,6 +38,9 @@ class exception_proxy(Exception):
         Returns:
             True или Exception
         """
+        
+        if value is None:
+            raise argument_exception("Пустой аргумент")
 
         # Проверка типа
         if not isinstance(value, type_):
@@ -52,6 +55,8 @@ class exception_proxy(Exception):
 
         return True
      
+   
+         
      
 #
 # Исключение при проверки аргументов
diff --git a/src/models/abstract_reference.py b/src/models/abstract_reference.py
deleted file mode 100644
index 9e43eda..0000000
--- a/src/models/abstract_reference.py
+++ /dev/null
@@ -1,38 +0,0 @@
-import uuid
-from src.argument_exception import argument_exception
-from src.error_proxy import error_proxy
-from abc import ABC
-
-class abstract_reference(ABC):
-    __id: uuid.UUID
-    __ref_name: str = ""
-    __error: error_proxy = error_proxy()
-
-    def __init__(self, name: str = None) -> None:
-        self.ref_name = name
-        self.__id = uuid.uuid4
-    
-    def error(self):
-        return self.__error
-    
-    @property
-    def id(self):
-        return self.__id
-
-    @property
-    def ref_name(self):
-        return self.__ref_name.strip()
-    
-    @ref_name.setter
-    def ref_name(self, value: str):
-        if not isinstance(value, str):
-            raise argument_exception("ERROR: Неверный аргумент name")
-        
-        if value == "":
-            raise argument_exception("ERROR: Пустой аргумент name")
-        
-        value = value.strip()
-
-        if len(value) >= 50:
-            raise argument_exception("ERROR: Неверная длина name")
-        self.__ref_name = value
\ No newline at end of file
diff --git a/src/models/company.py b/src/models/company.py
deleted file mode 100644
index d2fc18b..0000000
--- a/src/models/company.py
+++ /dev/null
@@ -1,44 +0,0 @@
-# ИНН, БИК, Счет, Форма собственности.
-from src.models.abstract_reference import abstract_reference
-from src.argument_exception import argument_exception
-from src.operation_exception import operation_exception
-
-class company_model(abstract_reference):
-    __inn = None
-    __bik = None
-    __account = None
-    __ownship_type = None
-    __settings = None
-
-    def __init__(self, settings, name: str = "Company"):
-        super().__init__(name)
-        self.__settings = settings
-        self.__convert()
-
-    def __convert(self):
-        for field in dir(self):
-            if field.startswith("_") or not hasattr(self.__settings, field):
-                continue
-            
-            value = getattr(self.__settings, field)
-            setattr(self, f"_{self.__class__.__name__}__{field}", value)
-
-    # ИНН
-    @property
-    def inn(self):
-        return self.__inn
-
-    # БИК
-    @property
-    def bik(self):
-        return self.__bik
-    
-    # Счёт
-    @property
-    def account(self):
-        return self.__account
-
-    # Вид собственности
-    @property
-    def ownship_type(self):
-        return self.__ownship_type
\ No newline at end of file
diff --git a/src/models/group_model.py b/src/models/group_model.py
index 2916d0a..4f2e84b 100644
--- a/src/models/group_model.py
+++ b/src/models/group_model.py
@@ -4,7 +4,13 @@ from Src.reference import reference
 # Модель группу номенклатуры
 # 
 class group_model(reference):
-    def create_group():
+    def create_default_group():
+        """
+        Фабричный метод. Создать группу по умолчанию
+
+        Returns:
+            _type_: _description_
+        """
         item = group_model("Ингредиенты")
-        
-        return item
\ No newline at end of file
+        return item
+    
\ No newline at end of file
diff --git a/src/models/nomenclature.py b/src/models/nomenclature.py
deleted file mode 100644
index f43c861..0000000
--- a/src/models/nomenclature.py
+++ /dev/null
@@ -1,57 +0,0 @@
-from src.models.abstract_reference import abstract_reference
-from src.models.company import company_model
-from src.models.range import range_model
-from src.models.nomenclature_group import nomenclature_group_model
-from src.argument_exception import argument_exception
-from src.operation_exception import operation_exception
-
-
-class nomenclature_model(abstract_reference):
-    __full_name = ''
-    __group = None
-    __ranges = None
-
-    def __init__(self, name: str, full_name: str, group: nomenclature_group_model, ranges: range_model):
-        super().__init__(name)
-        self.full_name = full_name
-        self.ranges = ranges
-        self.group = group
-
-
-    @property
-    def full_name(self):
-        return self.__full_name
-    
-    @full_name.setter
-    def full_name(self, value: str):
-        if not isinstance(value, str):
-            raise argument_exception("ERROR: full_name не является строкой")
-
-        value = value.strip()
-
-        if value == "":
-            raise argument_exception("ERROR: full_name пустое")
-        
-        self.__full_name = value
-
-    @property
-    def group(self):
-        return self.__group
-    
-    @group.setter
-    def group(self, value):
-        if not isinstance(value, nomenclature_group_model):
-            raise argument_exception("ERROR: full_name не является nomenclature_group_model")
-
-        self.__group = value
-        
-    @property
-    def ranges(self):
-        return self.__ranges
-    
-    @ranges.setter
-    def ranges(self, value):
-        if not isinstance(value, range_model):
-            raise argument_exception("ERROR: full_name не является nomenclature_group_model")
-        
-        self.__ranges = value
\ No newline at end of file
diff --git a/src/models/nomenclature_group.py b/src/models/nomenclature_group.py
deleted file mode 100644
index a986d55..0000000
--- a/src/models/nomenclature_group.py
+++ /dev/null
@@ -1,4 +0,0 @@
-from src.models.abstract_reference import abstract_reference
-
-class nomenclature_group_model(abstract_reference):
-    pass
\ No newline at end of file
diff --git a/src/models/nomenclature_model.py b/src/models/nomenclature_model.py
index e7027c0..1e111e9 100644
--- a/src/models/nomenclature_model.py
+++ b/src/models/nomenclature_model.py
@@ -1,7 +1,6 @@
 from Src.reference import reference
 from Src.exceptions import exception_proxy
-from Src.Models.unit_model import unit_model
-from Src.Models.group_model import group_model
+
 
 class nomenclature_model(reference):
     " Группа номенклатуры "
@@ -9,6 +8,26 @@ class nomenclature_model(reference):
     " Единица измерения "
     _unit = None
     
+    
+    def __init__(self, name:str, group: reference = None, unit: reference = None):
+        """_summary_
+
+        Args:
+            name (str): Наименование
+            group (reference): Группа
+            unit (reference): Единица измерения
+        """
+        
+        if not group is None:
+            exception_proxy.validate(group, reference)
+            self._group = group
+            
+        if not unit is None:  
+            exception_proxy.validate(unit, reference)  
+            self._unit = unit
+            
+        super().__init__(name)
+    
     @property
     def group(self):
         " Группа номенклатуры "
@@ -29,9 +48,7 @@ class nomenclature_model(reference):
     def unit(self, value: reference):
         " Единица измерения "
         exception_proxy.validate(value, reference)
-        self._unit = value    
-
-    def __init__(self, name, unit: unit_model = None, group: group_model = None):
-        super().__init__(name)
-        self.unit = unit
-        self.group = group
\ No newline at end of file
+        self._unit = value
+        
+  
+    
\ No newline at end of file
diff --git a/src/models/range.py b/src/models/range.py
deleted file mode 100644
index a4dd81f..0000000
--- a/src/models/range.py
+++ /dev/null
@@ -1,18 +0,0 @@
-from src.models.abstract_reference import abstract_reference
-
-class range_model(abstract_reference):
-    __base = None
-    __cf: int
-
-    def __init__(self, name: str, cf: int = 0, base = None):
-        super().__init__(name)
-        self.__base = base
-        self.__cf = cf
-
-    @property
-    def base(self):
-        return self.__base
-    
-    @property
-    def cf(self):
-        return self.__cf
\ No newline at end of file
diff --git a/src/models/receipe_model.py b/src/models/receipe_model.py
index 367c24f..2135766 100644
--- a/src/models/receipe_model.py
+++ b/src/models/receipe_model.py
@@ -21,6 +21,10 @@ class receipe_model(reference):
     # Описание
     _comments: str = ""
     
+    @property
+    def rows(self):
+        return self._rows
+    
     def  rows_ids(self):
         result = []
         for item in self._rows:
@@ -58,8 +62,22 @@ class receipe_model(reference):
             # Получаем свойство size
             self._brutto += self._rows[position].size 
             
+    @property     
+    def brutto(self):
+        """
+            Вес брутто
+        Returns:
+            int : _description_
+        """
+        return self._brutto
+    
+    @brutto.setter
+    def brutto(self, value: int) -> int:
+        exception_proxy.validate(value, int)
+        self._brutto = value     
+            
     @property         
-    def netto(self):
+    def netto(self) -> int:
         return self._netto                        
         
     @netto.setter
@@ -96,6 +114,15 @@ class receipe_model(reference):
         """
         exception_proxy.validate(value, str)
         self._comments = value   
+        
+    @property            
+    def consist(self) -> list:
+        """
+            Состав рецепта
+        Returns:
+            _type_: _description_
+        """
+        return self._rows    
     
     
     @staticmethod
diff --git a/src/models/reciepe_model.py b/src/models/reciepe_model.py
deleted file mode 100644
index 01a9225..0000000
--- a/src/models/reciepe_model.py
+++ /dev/null
@@ -1,22 +0,0 @@
-from Src.Models.nomenclature_model import nomenclature_model
-from Src.reference import reference
-from Src.Models.unit_model import unit_model
-from Src.exceptions import exception_proxy
-
-class reciepe_model (reference):
-    __rows: list
-    __description: str
-
-    def __init__(self, name, *args, description: str = 'Киньте всё в одну чашу и перемешайте.'):
-        self.__rows = list(args)
-        self.description = description
-        super().__init__(name=name)
-
-    @property
-    def description(self):
-        return self.__description
-
-    @description.setter
-    def description(self, value: str):
-        exception_proxy.validate(value.strip(), str)
-        self.__description = value.strip()
\ No newline at end of file
diff --git a/src/models/reciepe_row.py b/src/models/reciepe_row.py
deleted file mode 100644
index 92a1616..0000000
--- a/src/models/reciepe_row.py
+++ /dev/null
@@ -1,34 +0,0 @@
-from Src.Models.nomenclature_model import nomenclature_model
-from Src.Models.unit_model import unit_model
-from Src.reference import reference
-from Src.exceptions import exception_proxy
-
-class reciepe_row_model(reference):
-    __nomenculatures: nomenclature_model = None
-    __size: int = 0
-    __unit: unit_model = None
-
-    def __init__(self, nomenculature: nomenclature_model, size: int, unit: unit_model):
-        self.__nomenculatures = nomenculature
-        self.__size = size
-        self.__unit = unit
-
-        super().__init__(name=f"{self.__nomenculatures.name}, {size} {self.__unit.name}")
-
-    @property
-    def nomenculature(self):
-        return self.__nomenculatures
-
-    @property
-    def size(self):
-        return self.__size
-
-    @size.setter
-    def size(self, value : int):
-        exception_proxy.validate(value, int)
-
-        self.__size = value
-
-    @property
-    def unit(self):
-        return self.__unit 
\ No newline at end of file
diff --git a/src/models/storage_model.py b/src/models/storage_model.py
index 047c1a6..51a3b71 100644
--- a/src/models/storage_model.py
+++ b/src/models/storage_model.py
@@ -1,12 +1,44 @@
-from Src.reference import reference
-
-
-class storage_model(reference):
-    __adress: str = ''
-
-    def __init__(self, adress: str, *args, **kwargs):
-        super().__init__(*args, **kwargs)
-        self.__adress = adress
-
-    def adress(self) -> str:
-        return self.__adress
\ No newline at end of file
+from Src.reference import reference
+from Src.exceptions import exception_proxy
+
+#
+# Модель склада
+#
+class storage_model(reference):
+    _address: str = ""
+    
+    def __init__(self, name, address="ул. 2-я Желездодорожная, д. 147"):
+        super().__init__(name)
+        self.address = address
+
+    @property
+    def address(self) -> str:
+        """
+            Адрес
+
+        Returns:
+            _type_: _description_
+        """
+        return self._address
+    
+    @address.setter
+    def address(self, value:str):
+        """
+            Адрес
+        Args:
+            value (str): _description_
+        """
+        exception_proxy.validate(value, str)
+        self._address = value
+        
+    @staticmethod    
+    def create_default() -> reference:
+        """
+            Сформировать склад по умолчанию
+        Returns:
+            reference: _description_
+        """
+        storage = storage_model("default")
+        storage.address = "г. Москва. ул. Академика Королева, 10"
+        
+        return storage    
\ No newline at end of file
diff --git a/src/models/storage_transaction_model.py b/src/models/storage_transaction_model.py
deleted file mode 100644
index 35a4e79..0000000
--- a/src/models/storage_transaction_model.py
+++ /dev/null
@@ -1,55 +0,0 @@
-from Src.reference import reference
-from datetime import datetime
-from Src.Models.nomenclature_model import nomenclature_model
-from Src.Models.storage_model import storage_model
-from Src.Models.unit_model import unit_model
-from Src.exceptions import argument_exception
-
-class storage_transaction_model(reference):
-    __storage: storage_model
-    __nomen: nomenclature_model
-    __operation: bool
-    __contes: int
-    __unit: unit_model
-    __period: datetime
-
-
-    def __init__(self, storage: storage_model, nomen: nomenclature_model, operation: bool, countes: int, unit: unit_model, period: datetime,  name: str = ''):
-        super().__init__(name)
-        
-        self.__storage = storage
-        self.__nomen = nomen
-        self.__operation = operation
-        self.__contes = countes
-        self.__unit = unit
-        self.__period = period
-
-    
-    @property
-    def name(self):
-        return self.name
-    
-    @name.setter
-    def name(self, value):
-        if not isinstance(value, str):
-            raise argument_exception("Invalid name")
-        
-        self.__name = value
-
-    def storage(self):
-        return self.__storage
-
-    def nomenculature(self) -> nomenclature_model:
-        return self.__nomen
-
-    def opearation(self):
-        return self.__operation
-
-    def counts(self):
-        return self.__contes
-    
-    def unit(self):
-        return self.__unit
-
-    def period(self):
-        return self.__period
\ No newline at end of file
diff --git a/src/models/storage_turn_model.py b/src/models/storage_turn_model.py
deleted file mode 100644
index 1084157..0000000
--- a/src/models/storage_turn_model.py
+++ /dev/null
@@ -1,31 +0,0 @@
-from Src.reference import reference
-from Src.Models.nomenclature_model import nomenclature_model
-from Src.Models.storage_model import storage_model
-from Src.Models.unit_model import unit_model
-
-class storage_turn_model(reference):
-    __storage: storage_model
-    __remains: int
-    __nomen: nomenclature_model
-    __unit: unit_model
-
-
-    def __init__(self, storage_: storage_model, remains: int,
-                nomen: nomenclature_model, unit: unit_model, name: str = ''):
-        super().__init__(name)
-        self.__storage = storage_
-        self.__remains = remains
-        self.__nomen = nomen
-        self.__unit = unit
-
-    def storage(self):
-        return self.__storage
-
-    def remains(self):
-        return self.__remains
-
-    def nomen(self):
-        return self.__nomen
-
-    def unit(self):
-        return self.__unit
\ No newline at end of file
diff --git a/src/models/unit_model.py b/src/models/unit_model.py
index 72807f0..28cb7be 100644
--- a/src/models/unit_model.py
+++ b/src/models/unit_model.py
@@ -1,6 +1,8 @@
 from Src.reference import reference
 from Src.exceptions import exception_proxy, argument_exception
 
+
+
 #
 # Модель единицы измерения для номенклатуры
 #
@@ -12,28 +14,28 @@ class unit_model(reference):
     # Коэффициент пересчета к базовой единице измерения
     __coefficient: int = 1
     
-    def __init__(self, name: str, base_unit: reference = None, coefficient: int = 1 ):
+    def __init__(self, name: str, base: reference = None, coeff: int = 1 ):
         super().__init__(name)
         
-        if self.base_unit != None:
-            self.base_unit = base_unit
+        if base != None:
+            self.base_unit = base
             
-        if coefficient != 1:
-            self.coefficient = coefficient    
+        if coeff != 1:
+            self.coefficient = coeff   
         
     
     @property
-    def base_unit(self):
+    def base_unit(self) -> reference:
         """
             Базовая единица измерения
         Returns:
             _type_: _description_
         """
         return self.__base_unit
-    
+
     
     @base_unit.setter
-    def base(self, value: reference ):
+    def base_unit(self, value: reference ):
         exception_proxy.validate(value, reference)
         self.__base_unit = value
         
@@ -48,7 +50,7 @@ class unit_model(reference):
         return self.__coefficient
     
     @coefficient.setter
-    def coefficient(self, value:int):
+    def   coefficient(self, value:int):
         exception_proxy.validate(value, int)
         
         if(value <= 0):
@@ -56,35 +58,65 @@ class unit_model(reference):
         
         self.__coefficient = value  
         
-    @staticmethod
-    def create_gramm():
-        item = unit_model("грамм", None, 1)
+        
+    # Фабричные методы    
+        
+    @staticmethod    
+    def create_gram():
+        """
+            Создать единицу измерения - грамм
 
-        return item
+        Returns:
+            _type_: _description_
+        """
+        item = unit_model("грамм", None, 1)
+        return item    
     
     @staticmethod
-    def create_kilogramm():
-        base = unit_model.create_gramm()
-        item = unit_model("грамм", base, 1000)
-
+    def create_killogram():
+        """
+            Создать единицу измерения - киллограмм
+        Returns:
+            _type_: _description_
+        """
+        base = unit_model.create_gram()
+        item = unit_model("киллограмм", base, 1000)
         return item
     
     @staticmethod
-    def create_count():
-        item = unit_model("шт", None, 1)
-
-        return item
+    def create_ting():
+        """
+            Создать единицу изменения - штуки
+        Returns:
+            _type_: _description_
+        """
+        return unit_model("штука")
     
-    @staticmethod
-    def create_mililiter():
-        item = unit_model("милилитр", None, 1)
-
-        return item
+    def create_milliliter():
+        """
+            Создать единицу измерения - миллилитр
+        Returns:
+            _type_: _description_
+        """
+        return unit_model("миллилитр")
     
-    @staticmethod
     def create_liter():
-        base = unit_model.create_mililiter()
-
-        item = unit_model("литр", base, 1)
+        """
+            Создать единицу измерения - литр
+        Returns:
+            _type_: _description_
+        """
+        base = unit_model.create_milliliter()
+        item = unit_model("литр", base, 1000)
+        return item
+    
+    
 
-        return item
\ No newline at end of file
+        
+        
+        
+        
+        
+        
+    
+    
\ No newline at end of file
diff --git a/src/operation_exception.py b/src/operation_exception.py
deleted file mode 100644
index 664adab..0000000
--- a/src/operation_exception.py
+++ /dev/null
@@ -1,12 +0,0 @@
-from src.error_proxy import error_proxy
-from src.argument_exception import argument_exception
-class operation_exception(argument_exception):
-    __inner_error: error_proxy = error_proxy()
-
-    def __init__(self, *args: object) -> None:
-        super().__init__(*args)
-        self.__inner_error.set_error(self)
-
-    @property
-    def error(self):
-        return self.__inner_error
\ No newline at end of file
diff --git a/src/reference.py b/src/reference.py
index 4aacb56..badeaef 100644
--- a/src/reference.py
+++ b/src/reference.py
@@ -1,7 +1,7 @@
 import uuid
 from abc import ABC
 from Src.errors import error_proxy
-from Src.exceptions import exception_proxy
+from Src.exceptions import exception_proxy, argument_exception
 
 #
 # Абстрактный класс для наследования
@@ -17,7 +17,7 @@ class reference(ABC):
     _error = error_proxy()
     
     def __init__(self, name):
-        _id = uuid.uuid4()
+        self._id = uuid.uuid4()
         self.name = name
     
     @property
@@ -42,16 +42,70 @@ class reference(ABC):
         exception_proxy.validate( value.strip(), str)
         self._description = value.strip()
         
-        
     @property
     def id(self):
         " Уникальный код записи "
-        return self._id  
+        return str(self._id.hex)  
 
     @property
     def is_error(self):
         " Флаг. Есть ошибка "
-        return self._error.error != ""     
+        return self._error.error != ""  
+    
+    @staticmethod
+    def create_dictionary(items: list):
+        """
+            Сформировать словарь из списка элементов reference 
+        Args:
+            items (list): _description_
+        """
+        exception_proxy.validate(items, list)
+        
+        result = {}
+        for position in items:
+            result[ position.name ] = position
+           
+        return result   
+   
+    @staticmethod
+    def create_fields(source) -> list:
+        """
+            Сформировать список полей от объекта типа reference
+        Args:
+            source (_type_): _description_
+
+        Returns:
+            list: _description_
+        """
+        
+        if source is None:
+            raise argument_exception("Некорректно переданы параметры!")
+        
+        items = list(filter(lambda x: not x.startswith("_") and not x.startswith("create_") , dir(source))) 
+        result = []
+        
+        for item in items:
+            attribute = getattr(source.__class__, item)
+            if isinstance(attribute, property):
+                result.append(item)
+                    
+        return result
+    
+    def __str__(self) -> str:
+        """
+            Изменим строковое представление класса
+        Returns:
+            str: _description_
+        """
+        return self.id
+    
+    def __hash__(self) -> int:
+        """
+            Формирование хеш по коду
+        Returns:
+            int: _description_
+        """
+        return hash(self.id)
     
     
                 
diff --git a/src/settings.json b/src/settings.json
index 013d2ed..43a9893 100644
--- a/src/settings.json
+++ b/src/settings.json
@@ -1,5 +1,6 @@
 {
    "inn":3800020344,
    "short_name":"ООО Ромашка",
-   "is_first_start": true
+   "is_first_start": true,
+   "report_mode":"json"
 }
diff --git a/src/settings.py b/src/settings.py
index 7edcab1..dd96291 100644
--- a/src/settings.py
+++ b/src/settings.py
@@ -1,112 +1,68 @@
-from src.argument_exception import argument_exception
+from Src.exceptions import exception_proxy
 
-class settings:
-    # Инициализируем пустыми
-    __first_name = None
-    __inn = None
-    __bik = None
-    __account = None
-    __cor_account = None
-    __name = None
-    __ownship_type = None
-
-    @property
-    def first_name(self):
-        return self.__first_name
+#
+# Класс для описания настроек
+#
+class settings():
+    _inn = 0
+    _short_name = ""
+    _first_start = True
+    _mode = "csv"
+    
     
-    @first_name.setter
-    def first_name(self, value: str):
-        if not isinstance(value, str):
-            raise argument_exception("Некорректный аргумент!")
-        
-        self.__first_name = value.strip()
-        
-    # ИНН
     @property
     def inn(self):
-        return self.__inn
+        """
+            ИНН
+        Returns:
+            int: 
+        """
+        return self._inn
     
     @inn.setter
-    def inn(self, value: str):
-        if not isinstance(value, str):
-            raise argument_exception("ERROR: Некорректный аргумент!")
-        
-        if len(value) != 12:
-            raise argument_exception("ERROR: Длина ИНН не равна 12!")
-        
-        self.__inn = value.strip()
-
-    # Кор. счёт
-    @property
-    def cor_account(self):
-        return self.__cor_account
-    
-    @cor_account.setter
-    def cor_account(self, value: str):
-        if not isinstance(value, str):
-            raise argument_exception("Некорректный аргумент!")
-        
-        if len(value) != 11:
-            raise argument_exception("ERROR: Длина кор. счёта не равна 11!")
-        
-        self.__cor_account = value.strip()
+    def inn(self, value: int):
+        exception_proxy.validate(value, int)
+        self._inn = value
+         
+    @property     
+    def short_name(self):
+        """
+            Короткое наименование организации
+        Returns:
+            str:
+        """
+        return self._short_name
     
-    # БИК
-    @property
-    def bik(self):
-        return self.__bik
-    
-    @bik.setter
-    def bik(self, value: str):
-        if not isinstance(value, str):
-            raise argument_exception("Некорректный аргумент!")
+    @short_name.setter
+    def short_name(self, value:str):
+        exception_proxy.validate(value, str)
+        self._short_name = value
         
-        if len(value) != 9:
-            raise argument_exception("ERROR: Длина БИК не равна 9!")
         
-        self.__bik = value.strip()
-
-    # Счёт
-    @property
-    def account(self):
-        return self.__account
-    
-    @account.setter
-    def account(self, value: str):
-        if not isinstance(value, str):
-            raise argument_exception("Некорректный аргумент!")
-
-        if len(value) != 11:
-            raise argument_exception("ERROR: Длина счёта не равна 11!")
+    @property    
+    def is_first_start(self):
+        """
+           Флаг Первый старт
+        """
+        return self._first_start    
+            
+    @is_first_start.setter        
+    def is_first_start(self, value: bool):
+        self._first_start = value
         
-        self.__account = value.strip()
-
-    # Наименование
     @property
-    def name(self):
-        return self.__name
+    def report_mode(self):
+        """
+            Режим построения отчетности
+        Returns:
+            _type_: _description_
+        """
+        return self._mode
     
-    @name.setter
-    def name(self, value: str):
-        if not isinstance(value, str):
-            raise argument_exception("Некорректный аргумент!")
-        
-        if str == "":
-            raise argument_exception("ERROR: Пустое наименование!")
-        
-        self.__name = value.strip()
-
-    # Вид собственности
-    @property
-    def ownship_type(self):
-        return self.__ownship_type
     
-    @ownship_type.setter
-    def ownship_type(self, value: str):
-        if not isinstance(value, str):
-            raise argument_exception("Некорректный аргумент!")
-        
-        if len(value) != 5:
-            raise argument_exception("ERROR: Длина вида собственности не равна 5!")
+    @report_mode.setter
+    def report_mode(self, value: str):
+        exception_proxy.validate(value, str)
         
-        self.__ownship_type = value.strip()
\ No newline at end of file
+        self._mode = value
+    
\ No newline at end of file
diff --git a/src/settings_manager.py b/src/settings_manager.py
index 885c389..db5da6f 100644
--- a/src/settings_manager.py
+++ b/src/settings_manager.py
@@ -1,87 +1,120 @@
 import os
-import uuid
 import json
-from src.settings import settings
-from src.argument_exception import argument_exception
-from src.operation_exception import operation_exception
+import uuid
+
+from Src.settings import settings
+from Src.errors import error_proxy
+from Src.exceptions import exception_proxy
 
+
+#
+# Менеджер настроек
+#   
 class settings_manager(object):
-    __file_name = "settings.json"
-    # Уникальный номер
-    __unique_number = None
+    # Наименование файла по умолчанию
+    _settings_file_name = "settings.json"
+    # Словарь с исходными данными
+    _data = None
+    # Внутренний уникальный номер
+    _uniqueNumber = None
+    # Данные с настройками
+    _settings = None
+    # Описание ошибок
+    _error = error_proxy()
     
-    __data = {}
-    # Настройки инстанс
-    __settings = settings()
-
     def __new__(cls):
-        if not hasattr(cls, "instance"):
+        if not hasattr(cls, 'instance'):
             cls.instance = super(settings_manager, cls).__new__(cls)
-    
-        return cls.instance
-    
-    def __convert(self):
-        """
-            Метод конверта данных в json
-        """
-        if len(self.__data) == 0:
-            raise argument_exception("ERROR: Невозможно создать объект типа settings.py")
-        
-        fields = dir(self.__settings.__class__)
-
-        for field in fields:
-            # Проверяем есть ли такое значение у объекта
-            if not field in self.__data.keys():
-                continue
+        return cls.instance  
+      
 
-            setattr(self.__settings, field, self.__data[field])
+    def __init__(self):
+        if self._uniqueNumber is None:
+            self._uniqueNumber = uuid.uuid4()
+            self.open(self._settings_file_name)
+            
+            # После загрузки создаем объект класса settings
+            self._settings = settings()
+            self.__load()
+                
 
-
-
-    def __init__(self) -> None:
-        self.__unique_number = uuid.uuid4()
-
-    def open(self, file_name: str) -> bool:
+    def __open(self):
         """
-            Метод открытия файла
+            Открыть файл с настройками
         """
-        if not isinstance(file_name, str):
-            raise argument_exception("ERROR: Неверный аргумент file_name")
-
-        if file_name == "":
-            raise argument_exception("ERROR: Неверный аргумент file_name")
-        
-        self.__file_name = file_name.strip()
+        file_path = os.path.split(__file__)
+        settings_file = "%s/%s" % (file_path[0], self._settings_file_name)
+        if not os.path.exists(settings_file):
+            self._error.set_error( Exception("ERROR: Невозможно загрузить настройки! Не найден файл %s", settings_file))
 
         try:
-            self.__open()
-            self.__convert()
+            with open(settings_file, "r") as read_file:
+                self._data = json.load(read_file)     
         except:
-            return False
-
-
-    def __open(self):
-        file_path = os.path.split(__file__)
-        settings_file = "%s/%s" % (file_path[0], self.__file_name)
+            self._error.set_error( Exception("ERROR: Невозможно загрузить настройки! Не найден файл %s", settings_file))     
 
-        if not os.path.exists(settings_file):
-            raise operation_exception("ERROR: невозможно загрузить настройки")
+    def open(self, file_name: str):
+        """
+            Открыть файл с настройками
+        Args:
+            file_name (str):
+        """
+        exception_proxy.validate( file_name, str)
+            
+        self._settings_file_name = file_name
+        self.__open()
+        self.__load()
+    
+    
+    def __load(self):
+        """
+            Private: Загрузить словарь в объект
+        """
         
-        with open(settings_file, "r") as read_file:
-            self.__data = json.load(read_file)
-
-    @property 
-    def settings(self): 
-        return self.__settings
-
-    @property 
-    def data(self): 
-        return self.__data
+        if len(self._data) == 0:
+            return
+        
+        # Список полей от типа назначения    
+        fields = list(filter(lambda x: not x.startswith("_"), dir(self._settings.__class__)))
+        
+        # Заполняем свойства 
+        for field in fields:
+            keys = list(filter(lambda x: x == field, self._data.keys()))
+            if len(keys) != 0:
+                value = self._data[field]
+                
+                # Если обычное свойство - заполняем.
+                if not isinstance(value, list) and not isinstance(value, dict):
+                    setattr(self._settings, field, value)
+                
+        
+    
+    @property    
+    def settings(self) -> settings:
+        """
+            Текущие настройки в приложении
+        Returns:
+            settings: _
+        """
+        return self._settings 
     
     @property
-    def number(self):
-        return str(self.__unique_number.hex)
+    def data(self):
+        """
+            Словарь, который содержит данные из настроек
+        Returns:
+            dict:
+        """
+        return self._data
     
-    @number.setter
-    def number(self, value: int) -> str:
-        self.__unique_number = value
\ No newline at end of file
+    @property
+    def error(self) -> error_proxy:
+        """
+            Текущая информация об ошибке
+        Returns:
+            error_proxy: 
+        """
+        return self._error
+
+
+    
\ No newline at end of file
diff --git a/tests/settings.json b/tests/settings.json
deleted file mode 100644
index 7a2ac68..0000000
--- a/tests/settings.json
+++ /dev/null
@@ -1,9 +0,0 @@
-{
-    "first_name": "Volovikov",
-    "inn": "575757575757",
-    "bik": "999999999",
-    "account": "11111111111",
-    "cor_account": "22222222222",
-    "name": "Afdsfdsf",
-    "ownship_type": "12345"
-}
\ No newline at end of file
diff --git a/tests/tempCodeRunnerFile.py b/tests/tempCodeRunnerFile.py
deleted file mode 100644
index 4791ed5..0000000
--- a/tests/tempCodeRunnerFile.py
+++ /dev/null
@@ -1 +0,0 @@
-True
\ No newline at end of file
diff --git a/tests/test_errors.py b/tests/test_errors.py
deleted file mode 100644
index 2ed49e4..0000000
--- a/tests/test_errors.py
+++ /dev/null
@@ -1,29 +0,0 @@
-import unittest
-from src.error_proxy import error_proxy
-from src.argument_exception import argument_exception
-
-class test_errors(unittest.TestCase):
-    def test_check_set_exception(self):
-        error = error_proxy()
-        try:
-            result = 1 / 0
-        except Exception as ex:
-            error.set_error(ex)
-
-        assert error.is_error == True
-
-    def test_check_argument_exception(self):
-        try:
-            raise argument_exception("Test")
-        except argument_exception as ex:
-            print(ex.error.error_text)
-            print(ex.error.error_source)
-            assert ex.error.is_error
-            return
-
-        assert 1 != 1
-
-    def test_check_set_error_text(self):
-        error = error_proxy("Test", "test")
-
-        assert error.is_error == True
\ No newline at end of file
diff --git a/tests/test_models.py b/tests/test_models.py
deleted file mode 100644
index f2c9115..0000000
--- a/tests/test_models.py
+++ /dev/null
@@ -1,42 +0,0 @@
-import unittest
-from src.settings_manager import settings_manager
-from src.models.company import company_model
-from src.models.range import range_model
-from src.models.nomenclature import nomenclature_model
-from src.models.nomenclature_group import nomenclature_group_model
-
-class test_models(unittest.TestCase):
-    def test_check_company_convert(self):
-        # Подготовка
-        manager = settings_manager()
-        manager.open("../tests/settings.json")
-        settings = manager.settings
-
-        company = company_model(settings)
-        # Действие
-        result = True
-
-        for i in dir(company):
-            if i.startswith("_") or not hasattr(settings, i):
-                continue
-            
-            if getattr(settings, i) != getattr(company, i):
-                result = False
-                break
-            
-        # Проверки
-        assert result == True
-
-    def test_nomenclature_group(self):
-        # Подготовка
-        group = nomenclature_group_model('Group one')
-        # Проверки
-        assert bool(group) == True
-
-    def test_nomen(self):
-        # Подготовка
-        nom = nomenclature_model("Номенклатура 1", 'Большое название', 
-                                nomenclature_group_model('Group'), range_model("Range"))
-
-        # Проверки
-        assert bool(nom) == True
\ No newline at end of file
diff --git a/tests/test_settings.py b/tests/test_settings.py
deleted file mode 100644
index a2dc48f..0000000
--- a/tests/test_settings.py
+++ /dev/null
@@ -1,30 +0,0 @@
-import unittest
-from src.settings_manager import settings_manager
-
-class test_settings(unittest.TestCase):
-    def test_check_open_settings(self):
-        manager = settings_manager()
-
-        result = manager.open("../tests/settings.json")
-
-        assert result != False
-
-    def test_check_create_manager(self):
-        manager1 = settings_manager()
-        manager2 = settings_manager()
-
-        print(manager1.number)
-        print(manager2.number)
-
-        assert(manager1.number == manager2.number)
-
-    def test_check_manager_convert(self):
-        manager = settings_manager()
-        manager.open("../tests/settings.json")
-        
-        settings = manager.settings
-        data = manager.data
-
-        v = [i for i in dir(settings) if not i.startswith("_") and getattr(settings, i) != data[i] ]
-
-        assert len(v) == 0
\ No newline at end of file
diff --git "a/\320\220\321\200\321\205\320\270\320\262.zip" "b/\320\220\321\200\321\205\320\270\320\262.zip"
deleted file mode 100644
index 70692ac..0000000
Binary files "a/\320\220\321\200\321\205\320\270\320\262.zip" and /dev/null differ
