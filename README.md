# MiniDB

A lightweight in-memory relational database built from scratch in Python.

## Features

- Create tables
- Define typed columns
- Insert rows
- Schema validation
- Custom Row abstraction
- Object-oriented design

## Example

```python
from database import Database, Column

db = Database()

db.create_table(
    "employees",
    [
        Column("id", int),
        Column("name", str),
        Column("salary", float)
    ]
)

db.insert_table_row(
    "employees",
    {
        "id": 1,
        "name": "Alice",
        "salary": 50000.0
    }
)

print(db.get_table_rows("employees"))
```

Below command is used to run the tests for the database module:
```python -m pytest tests/test_database.py```