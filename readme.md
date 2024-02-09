# Банковское приложение


**Конверт настроек из json**


```
    manager = settings_manager()

    data = manager.open("../tests/settings.json")

	# data вернет все поля класса settings_manager
```

**Поля класса**


```
    manager = settings_manager()

    data = manager.open("../tests/settings.json")
	
	# Имя
	data.first_name

	# ИНН
	data.inn

	# БИК
	data.bik

	# Счёт
	data.account

	# Кор. счёт
	data.cor_account
	
	# Вид собственности
	data.ownship_type

	# Наименование
	data.name
```
