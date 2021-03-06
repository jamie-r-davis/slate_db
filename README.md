# Slate DB
A Python wrapper for executing Slate Custom SQL in Python.

## Installation
You must first install the [ODBC Driver for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-2017).

Then install via pip:
```
pip install git+https://github.com/jamie-r-davis/slate_db
```

## Usage
The `SlateDB.select` method returns a generator which will yield any records that match your `sql` query. By default, each record is returned as an AttrDict, enabling access via keys or via attributes:

```python
>>> from slate_db import SlateDB
>>> db = SlateDB(server='your.server.com',
                 port=1441,
                 db='dbname-test',
                 username='user',
                 password='secret-password')

# select all records with last name "Smith"
>>> sql = """select * from person where last = 'Smith'"""
>>> for record in db.select(sql):
>>>     print("Via attribute: {} <{}>".format(record.name, record.email))
>>>     print("Via key: {} <{}>".format(record['name'], record['email']])
# Via attribute: Smith, John <john.smith@example.com>
# Via key: Smith, John <john.smith@example.com>
# Via attribute: Smith, Granny <granny.smith@example.com>
# Via key: Smith, Granny <granny.smith@example.com> 
```
