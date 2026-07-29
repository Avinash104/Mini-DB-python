import pytest
from exceptions import TableAlreadyExistsError, DuplicatePrimaryKeyError, RequiredColumnMissing, NoQualifiedRowsForDelete, UpdateColumnTypeMismatch, RequiredColumnCannotBeNone, TableDoesNotExistError, TableNotFoundError, UnknownColumnError, InvalidDataTypeInWhereClause

def test_insert_valid_row(test_db):
    new_row = {"emp_id": 100, "name": "Test Employee", "salary": 50000.00, "age": 30}
    test_db.insert_into("employees", new_row)
    result = test_db.select(table_name="employees").where("emp_id", "==", 100).execute()
    assert len(result) == 1
    assert result[0]["name"] == "Test Employee"

# def test_insert_missing_required_column(test_db):
#     new_row = {"emp_id": 101, "name": "Another Employee", "salary": 60000.00}  # Missing 'age'
#     with pytest.raises(ValueError):
#         test_db.insert_into("employees", new_row)

# def test_insert_extra_column(test_db):
#     new_row = {"emp_id": 102, "name": "Extra Column Employee", "salary": 70000.00, "age": 28, "extra_col": "extra_value"}
#     with pytest.raises(ValueError):
#         test_db.insert_into("employees", new_row)

# def test_insert_wrong_datatype(test_db):
#     new_row = {"emp_id": 103, "name": "Wrong Datatype Employee", "salary": "not_a_number", "age": 25}  # salary should be a float
#     with pytest.raises(ValueError):
#         test_db.insert_into("employees", new_row)

# def test_delete_rows(test_db):
#     # Insert a row to delete
#     new_row = {"emp_id": 104, "name": "Delete Me", "salary": 80000.00, "age": 29}
#     test_db.insert_into("employees", new_row)
    
#     # Delete the row
#     test_db.delete_from("employees").where("emp_id", "==", 104).execute()
    
#     # Verify deletion
#     result = test_db.select(table_name="employees").where("emp_id", "==", 104).execute()
#     assert len(result) == 0

# def test_update_rows(test_db):
#     # Insert a row to update
#     new_row = {"emp_id": 105, "name": "Update Me", "salary": 90000.00, "age": 31}
#     test_db.insert_into("employees", new_row)
    
#     # Update the row
#     test_db.update(table_name="employees").where("emp_id", "==", 105).set_cols({"salary": 95000.00, "age": 32}).execute()
    
#     # Verify update
#     result = test_db.select(table_name="employees").where("emp_id", "==", 105).execute()
#     assert len(result) == 1
#     assert result[0]["salary"] == 95000.00
#     assert result[0]["age"] == 32

# def test_primary_key_duplicat(test_db):
#     duplicate_row = {"emp_id": 1, "name": "Duplicate Primary Key", "salary": 110000.00, "age": 34}
#     with pytest.raises(DuplicatePrimaryKeyError):
#         test_db.insert_table_row("employees", duplicate_row)

# def test_insert_into_missing_table(test_db):
#     new_row = {"emp_id": 107, "name": "Missing Table Test", "salary": 120000.00, "age": 35}
#     with pytest.raises(ValueError):
#         test_db.insert_into("missing_table", new_row)

# def test_insert_with_invalid_column(test_db):
#     new_row = {"emp_id": 108, "name": "Invalid Column Test", "salary": 130000.00, "age": 36, "invalid_col": "invalid_value"}
#     with pytest.raises(ValueError):
#         test_db.insert_into("employees", new_row)

# def test_insert_with_invalid_datatype(test_db):
#     new_row = {"emp_id": 109, "name": "Invalid Datatype Test", "salary": "not_a_number", "age": 37}  # salary should be a float
#     with pytest.raises(ValueError):
#         test_db.insert_into("employees", new_row) 

# def test_insert_duplicate_primary_key(test_db):
#     duplicate_row = {"emp_id": 106, "name": "Duplicate Primary Key", "salary": 110000.00, "age": 34}
#     with pytest.raises(ValueError):
#         test_db.insert_into("employees", duplicate_row)

# def test_update_existing_row(test_db):
#     test_db.update("employees").set("salary", 95000.00).set("age", 32).where("emp_id", "==", 105).execute()
    
#     # Verify update
#     result = test_db.select(table_name="employees").where("emp_id", "==", 105).execute()
#     assert len(result) == 1
#     assert result[0]["salary"] == 95000.00
#     assert result[0]["age"] == 32

# def test_update_non_existing_row(test_db):
#     test_db.update("employees").set("salary", 80000.00).where("emp_id", "==", 999).execute()
    
#     # Verify that no rows were updated
#     result = test_db.select(table_name="employees").where("emp_id", "==", 999).execute()
#     assert len(result) == 0

# def test_update_with_invalid_column(test_db):
#     with pytest.raises(ValueError):
#         test_db.update("employees").set("non_existing_column", 123).where("emp_id", "==", 1).execute()

# def test_update_with_invalid_table(test_db):
#     with pytest.raises(ValueError):
#         test_db.update("non_existing_table").set("salary", 123).where("emp_id", "==", 1).execute()

# def test_update_with_invalid_condition(test_db):
#     with pytest.raises(ValueError):
#         test_db.update("employees").set("salary", 123).where("emp_id", ">", "invalid_value").execute()

# def test_delete_existing_row(test_db):
#     # Insert a row to delete
#     new_row = {"emp_id": 104, "name": "Delete Me", "salary": 80000.00, "age": 29}
#     test_db.insert_into("employees", new_row)
    
#     # Delete the row
#     test_db.delete_from("employees").where("emp_id", "==", 104).execute()
    
#     # Verify deletion
#     result = test_db.select(table_name="employees").where("emp_id", "==", 104).execute()
#     assert len(result) == 0

# def test_delete_non_existing_row(test_db):
#     test_db.delete_from("employees").where("emp_id", "==", 999).execute()
    
#     # Verify that no rows were deleted
#     result = test_db.select(table_name="employees").where("emp_id", "==", 999).execute()
#     assert len(result) == 0

# def test_delete_with_invalid_column(test_db):
#     with pytest.raises(ValueError):
#         test_db.delete_from("employees").where("non_existing_column", "==", 1).execute()

# def test_delete_with_invalid_table(test_db):
#     with pytest.raises(ValueError):
#         test_db.delete_from("non_existing_table").where("emp_id", "==", 1).execute()

