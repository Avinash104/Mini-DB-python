import pytest
from database import Column
from database import Row
from database import (TableAlreadyExistsError, 
                      TableDoesNotExistError, 
                      TableNotFoundError)

def test_database_connection(test_db):

    assert test_db is not None
    assert hasattr(test_db, 'get_table_rows')
    assert hasattr(test_db, 'select')
    assert hasattr(test_db, 'update')

def test_create_table(test_db):
    
    table_name = "test_table"
    columns = [
            Column("emp_id", int, primary_key=True),
            Column("name", str),
            Column("department_id", int),
    ]
    test_db.create_table(table_name, columns)
    assert table_name in test_db.tables
    assert len(test_db.tables[table_name].columns) == 3

def test_duplicate_table_creation(test_db):

    table_name = "test_table"
    columns = [
        Column("emp_id", int, primary_key=True),
        Column("name", str),
        Column("department_id", int),
    ]
    test_db.create_table(table_name, columns)

    with pytest.raises(TableAlreadyExistsError):
        test_db.create_table(table_name, columns)

def test_get_existing_table(test_db):
    result = test_db.get_table_rows("employees")
    assert isinstance(result, list)
    print(type(result[0].items()))
    assert all(isinstance(row, Row) for row in result)

def test_get_non_existing_table(test_db):
    with pytest.raises(TableDoesNotExistError):
        test_db.get_table_rows("non_existing_table")

def test_insert_into_existing_table(test_db):

    new_row = {"emp_id": 100, "name": "Test Employee", "department_id":1,"manager_id":3, "experience":5, 
               "salary": 50000.00, "age": 30, "city": "Pune", }

    test_db.insert_table_row("employees", new_row)
    result = test_db.select(table_name="employees").where("emp_id", "==", 100).execute()
    assert len(result) == 1
    assert result[0]["name"] == "Test Employee"

def test_insert_into_missing_table(test_db):
    new_row = {"emp_id": 100, "name": "Test Employee", "experience":5, 
               "salary": 50000.00, "age": 30, "city": "Pune", "project_id": 101}
    test_db.insert_table_row("employees", new_row)
    print(test_db.select("employees").where("emp_id", "==", 100))

    with pytest.raises(TableNotFoundError):
        test_db.insert_table_row("employees2", new_row)
