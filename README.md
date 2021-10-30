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

- database_transactions.py:
    - The file contains three classes `MongoDBClient`,  `MongoAdapter` and `TransactionEnabledMongoAdapter`
    - The class `MongoDBClient` is a wrapper class for pymongo driver (Don't Modify this class).
    - The class `MongoAdapter` and `DefaultMongoAdapter` is a wrapper class to provide a common interface for connecting
      to MongoDB using `MongoDBClient`.
    - `DefaultMongoAdapter` contains an execute function to execute on MongoDB.
    - The class `TransactionEnabledMongoAdapter` is an extended class to provide transaction support.
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

## How to use this template

### Prerequisites:

- Use `make run` to configure the environment and to install dependencies to the virtual environment.
- For Windows users, use `make OS=win run` to run the app
- Create an .env file in the root directory of the project, with `MONGODB_CONNECTION_STR` configured. Please check
  `settings.py` for all the properties loaded from the .env file.

The following steps describe the steps to use this template:

- Create an instance of `MongoAdapter` class.
- Provide the `database_name` in the constructor. By default, it takes from the environment
  variable `CUSTOM_MONGODB_DATABASE`
- Create a `repository.py` in the app directory (`orders` in this app) or where ever you want to create.
- Create your queries / inserts / updates in `repository.py` with all of your arguments and also have **session**
  parameter. Basically this file contains all the logic to interact with the database with transactions.
- In the `views.py`, import the `repository` file and use it where ever its applicable
- To use it, create an instance of `TransactionEnabledMongoAdapter` class.
    - Next set the callback function to one of the functions from `repository.py`.
    - Next call execute function with the arguments that the callback function requires.

_**Note**_: For more clarity please check my usage of this template in this simple app.
