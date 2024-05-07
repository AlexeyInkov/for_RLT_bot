# Тестовое задание
## Python3, Asyncio, MongoDB, Aiogram

### Описание задачи:
##### написание алгоритма агрегации статистических данных о зарплатах сотрудников компании по временным промежуткам. Ссылка на скачивание коллекции со статистическими данными, которую необходимо использовать при выполнении задания, находится в конце документа.
## Установка
### Установка MongoDB
```https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/```

### Запуск MongoDB
```sudo systemctl start mongod```

### Восстановление db из dump
```mongorestore --nsInclude=sampleDB.sample_collection /home/alex/Downloads/dump/```

#### Установка зависимостей

```pip install -r requirements.txt```

#### Запуск

- ```python main.py ```
