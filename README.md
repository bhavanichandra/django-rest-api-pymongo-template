# Django REST API Pymongo Template

| Features              | Comment         |
| --------------------- | --------------- |
| MongoDB Driver        | PyMongo         |
| Using ODM             | No              |
| Transaction Support   | Yes             |
| Microservices Support | No              |
-------------------------------------------

This repo uses pymongo driver to connect to MongoDB. This repo contains three parts

1. Django StartProject rest_api_template
2. Orders App
3. Shared Python Module

## Shared Python Module

This python module contains three python files each does its own part of the job.

- database.py:
    - This file contains the logic to instantiate the pymongo client
    - Classes `MongoDBClient` singleton class that extends `Object` class, `Collection` a static class that
      has `MongoDBClient` instance which creates collection based on Database name and collection name dynamically
    - It also has `OrderCollection` and `ProductCollection` classes which creates singleton classes that
      uses `Collection` class to get the collection pointer for the database
- helper.py:
    - This file mostly will have helper functions that makes our life easier
- wrapper.py:
    - This file is created to house Helper classes to create Success or Failure responses
    - This file contains three classes
        - `Wrapper` class which has a data field to be set by the extending/implementing classes
        - `SuccessWrapper` class is used to build success responses,the data is provided by user, the `success=True` is
          given in the constructor
        - `FailureWrapper` class is built for error messages only

## Orders App

- Orders app contains the typical api logic with models, views and urls. It also has `custom_exceptions.py` file.
- It contains two classes `DatabaseInitException` and `RecordNotFound` exceptions classes. Both extends `Exception`
  class.
- `models.py` file contains the type definitions for `Order` and `Product`. Used `mypy` library to have the types
- `util.py` file contains the actual logic in which the app contacts the database file from shared python module


