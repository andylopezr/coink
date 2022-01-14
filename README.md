# REST API With Flask & SQL Alchemy

> Form Database API using Python Flask, SQL Alchemy and Marshmallow

## Quick Start Using Pipenv

``` bash
# Activate venv
$ pipenv shell

# Install dependencies
$ pipenv install

# Create DB
$ python
>> from app import db
>> db.create_all()
>> exit()

# Run Server (http://localhost:5000)
python app.py
```

## Endpoints

* GET     /get
* GET     /create
* POST    /create
