import pytest
from database import Column
from database import Row
from exceptions import TableAlreadyExistsError, DuplicatePrimaryKeyError, RequiredColumnMissing, NoQualifiedRowsForDelete, UpdateColumnTypeMismatch, RequiredColumnCannotBeNone, TableDoesNotExistError, TableNotFoundError, UnknownColumnError, InvalidDataTypeInWhereClause

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

def test_insert_into_existing_table_with_missing_column(test_db):
    new_row = {"emp_id": 107, "name": "Missing Column Employee", "salary": 75000.00}  # Missing 'age'
    with pytest.raises(RequiredColumnMissing):
        test_db.insert_table_row("employees", new_row)

def test_default_value_insertion(test_db):
    new_row = {"emp_id": 101, "name": "Default Value Test", "salary": 60000.00, "age": 28}
    test_db.insert_table_row("employees", new_row)
    result = test_db.select(table_name="employees").where("emp_id", "==", 101).execute()
    assert len(result) == 1
    assert result[0]["department_id"] == 0  # Default value for department_id
    assert result[0]["project_id"] == 0     # Default value for project_id

def test_insert_duplicate_primary_key(test_db):
    duplicate_row = {"emp_id": 1, "name": "Duplicate Primary Key", "salary": 110000.00, "age": 34}
    with pytest.raises(DuplicatePrimaryKeyError):
        test_db.insert_table_row("employees", duplicate_row)

def test_update_existing_row(test_db):
    test_db.update("employees").set_cols({"age":32, "salary": 95000.00}).where("emp_id", "==", 1).execute()
    
    # Verify update
    result = test_db.select(table_name="employees").where("emp_id", "==", 1).execute()
    assert len(result) == 1
    assert result[0]["salary"] == 95000.00
    assert result[0]["age"] == 32

def test_update_non_existing_row(test_db):

    test_db.update("employees").set_cols({"age":32, "salary": 95000.00}).where("emp_id", "==", 999).execute()
    
    # Verify that no rows were updated
    result = test_db.select(table_name="employees").where("emp_id", "==", 999).execute()
    assert len(result) == 0

def test_update_with_invalid_column(test_db):
    with pytest.raises(UnknownColumnError):
        test_db.update("employees").set_cols({"non_existing_column": 123}).where("emp_id", "==", 1).execute()

def test_update_with_invalid_table(test_db):
    with pytest.raises(TableDoesNotExistError):
        test_db.update("non_existing_table").set_cols({"salary": 123}).where("emp_id", "==", 1).execute()

def test_update_with_invalid_condition(test_db):
    with pytest.raises(InvalidDataTypeInWhereClause):
        test_db.update("employees").set_cols({"salary": 123}).where("emp_id", ">", "invalid_value").execute()

def test_update_with_missing_required_column(test_db):
    with pytest.raises(RequiredColumnCannotBeNone):
        test_db.update("employees").set_cols({"department_id": None}).where("emp_id", "==", 1).execute()

def test_update_with_type_mismatch(test_db):
    with pytest.raises(UpdateColumnTypeMismatch):
        test_db.update("employees").set_cols({"salary": "not_a_number"}).where("emp_id", "==", 1).execute()

def test_delete_existing_row(test_db):
    # Insert a row to delete
    new_row = {"emp_id": 104, "name": "Delete Me", "salary": 80000.00, "age": 29}
    test_db.insert_table_row("employees", new_row)
    
    # Delete the row
    test_db.delete_from("employees").where("emp_id", "==", 104).execute()
    
    # Verify deletion
    result = test_db.select(table_name="employees").where("emp_id", "==", 104).execute()
    assert len(result) == 0

def test_delete_non_existing_row(test_db):
    with pytest.raises(NoQualifiedRowsForDelete):
        test_db.delete_from("employees").where("emp_id", "==", 999).execute()

def test_delete_with_invalid_column(test_db):
    with pytest.raises(UnknownColumnError):
        test_db.delete_from("employees").where("non_existing_column", "==", 1).execute()

def test_delete_with_invalid_table(test_db):
    with pytest.raises(TableDoesNotExistError):
        test_db.delete_from("non_existing_table").where("emp_id", "==", 1).execute()

def test_delete_with_invalid_condition(test_db):
    with pytest.raises(InvalidDataTypeInWhereClause):
        test_db.delete_from("employees").where("emp_id", ">", "invalid_value").execute()

