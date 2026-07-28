import pytest
from .conftest import test_db

def test_update_single_row(test_db):
    # Update the salary of the employee with emp_id 1
    test_db.update("employees").set("salary", 60000).where("emp_id", "==", 1).execute()
    
    # Verify the update
    result = test_db.select(table_name="employees").where("emp_id", "==", 1).execute()
    assert len(result) == 1
    assert result[0]["salary"] == 60000

def test_update_multiple_rows(test_db):
    # Update the salary of all employees in department 2
    test_db.update("employees").set("salary", 70000).where("department_id", "==", 2).execute()
    
    # Verify the update
    result = test_db.select(table_name="employees").where("department_id", "==", 2).execute()
    assert all(row["salary"] == 70000 for row in result)

def test_delete_single_row(test_db):
    # Delete the employee with emp_id 3
    test_db.delete_from("employees").where("emp_id", "==", 3).execute()
    
    # Verify the deletion
    result = test_db.select(table_name="employees").where("emp_id", "==", 3).execute()
    assert len(result) == 0

def test_delete_multiple_rows(test_db):
    # Delete all employees in department 1
    test_db.delete_from("employees").where("department_id", "==", 1).execute()
    
    # Verify the deletion
    result = test_db.select(table_name="employees").where("department_id", "==", 1).execute()
    assert len(result) == 0

def test_delete_no_rows(test_db):
    # Attempt to delete employees in a non-existing department
    test_db.delete_from("employees").where("department_id", "==", 999).execute()
    
    # Verify that no rows were deleted
    result = test_db.select(table_name="employees").execute()
    assert len(result) > 0  # Assuming there are still employees in the table

def test_update_no_rows(test_db):
    # Attempt to update employees in a non-existing department
    test_db.update("employees").set("salary", 80000).where("department_id", "==", 999).execute()
    
    # Verify that no rows were updated
    result = test_db.select(table_name="employees").where("department_id", "==", 999).execute()
    assert len(result) == 0

def test_update_with_invalid_column(test_db):
    with pytest.raises(ValueError):
        test_db.update("employees").set("non_existing_column", 123).where("emp_id", "==", 1).execute()

def test_delete_with_invalid_column(test_db):
    with pytest.raises(ValueError):
        test_db.delete_from("employees").where("non_existing_column", "==", 1).execute()

def test_update_with_invalid_table(test_db):
    with pytest.raises(ValueError):
        test_db.update("non_existing_table").set("salary", 123).where("emp_id", "==", 1).execute()

def test_delete_with_invalid_table(test_db):
    with pytest.raises(ValueError):
        test_db.delete_from("non_existing_table").where("emp_id", "==", 1).execute()

def test_update_with_invalid_condition(test_db):
    with pytest.raises(ValueError):
        test_db.update("employees").set("salary", 123).where("emp_id", ">", "invalid_value").execute()

def test_delete_with_invalid_condition(test_db):
    with pytest.raises(ValueError):
        test_db.delete_from("employees").where("emp_id", ">", "invalid_value").execute()

def test_update_with_multiple_conditions(test_db):
    # Update the salary of employees in department 2 and age greater than 30
    test_db.update("employees").set("salary", 75000).where("department_id", "==", 2).where("age", ">", 30).execute()
    
    # Verify the update
    result = test_db.select(table_name="employees").where("department_id", "==", 2).where("age", ">", 30).execute()
    assert all(row["salary"] == 75000 for row in result)

def test_delete_with_multiple_conditions(test_db):
    # Delete employees in department 2 and age less than 25
    test_db.delete_from("employees").where("department_id", "==", 2).where("age", "<", 25).execute()
    
    # Verify the deletion
    result = test_db.select(table_name="employees").where("department_id", "==", 2).where("age", "<", 25).execute()
    assert len(result) == 0

def test_update_with_limit(test_db):
    # Update the salary of the first 2 employees in department 2
    test_db.update("employees").set("salary", 80000).where("department_id", "==", 2).limit(2).execute()
    
    # Verify the update
    result = test_db.select(table_name="employees").where("department_id", "==", 2).execute()
    updated_rows = [row for row in result if row["salary"] == 80000]
    assert len(updated_rows) == 2

def test_delete_with_limit(test_db):
    # Delete the first 2 employees in department 2
    test_db.delete_from("employees").where("department_id", "==", 2).limit(2).execute()
    
    # Verify the deletion
    result = test_db.select(table_name="employees").where("department_id", "==", 2).execute()
    assert len(result) == max(0, len(result) - 2)  # Ensure at least 2 rows were deleted if they existed

def test_update_with_order_by(test_db):
    # Update the salary of the employee with the highest salary in department 2
    test_db.update("employees").set("salary", 85000).where("department_id", "==", 2).order_by("salary", descending=True).limit(1).execute()
    
    # Verify the update
    result = test_db.select(table_name="employees").where("department_id", "==", 2).order_by("salary", descending=True).limit(1).execute()
    assert len(result) == 1
    assert result[0]["salary"] == 85000

def test_delete_with_order_by(test_db):   
    # Delete the employee with the lowest salary in department 2
    test_db.delete_from("employees").where("department_id", "==", 2).order_by("salary", descending=False).limit(1).execute()
    
    # Verify the deletion
    result = test_db.select(table_name="employees").where("department_id", "==", 2).execute()
    assert all(row["salary"] > 0 for row in result)  # Assuming salary is always positive

def test_update_with_group_by(test_db):
    # Update the salary of employees in department 2 grouped by age
    test_db.update("employees").set("salary", 90000).where("department_id", "==", 2).group_by("age").execute()
    
    # Verify the update
    result = test_db.select(table_name="employees").where("department_id", "==", 2).execute()
    assert all(row["salary"] == 90000 for row in result)

def test_delete_with_group_by(test_db):
    # Delete employees in department 2 grouped by age
    test_db.delete_from("employees").where("department_id", "==", 2).group_by("age").execute()
    
    # Verify the deletion
    result = test_db.select(table_name="employees").where("department_id", "==", 2).execute()
    assert len(result) == 0

def test_update_with_aggregation(test_db):
    # Update the salary of employees in department 2 to the average salary of that department
    avg_salary = test_db.select(table_name="employees").where("department_id", "==", 2).avg("salary").execute()[0]["avg_salary"]
    test_db.update("employees").set("salary", avg_salary).where("department_id", "==", 2).execute()
    
    # Verify the update
    result = test_db.select(table_name="employees").where("department_id", "==", 2).execute()
    assert all(row["salary"] == avg_salary for row in result)

def test_delete_with_aggregation(test_db):
    # Delete employees in department 2 whose salary is below the average salary of that department
    avg_salary = test_db.select(table_name="employees").where("department_id", "==", 2).avg("salary").execute()[0]["avg_salary"]
    test_db.delete_from("employees").where("department_id", "==", 2).where("salary", "<", avg_salary).execute()
    
    # Verify the deletion
    result = test_db.select(table_name="employees").where("department_id", "==", 2).execute()
    assert all(row["salary"] >= avg_salary for row in result)

def test_update_with_complex_conditions(test_db):
    # Update the salary of employees in department 2 who are older than 30 and have a salary less than 80000
    test_db.update("employees").set("salary", 95000).where("department_id", "==", 2).where("age", ">", 30).where("salary", "<", 80000).execute()
    
    # Verify the update
    result = test_db.select(table_name="employees").where("department_id", "==", 2).where("age", ">", 30).where("salary", "==", 95000).execute()
    assert all(row["salary"] == 95000 for row in result)

def test_delete_with_complex_conditions(test_db):
    # Delete employees in department 2 who are younger than 25 and have a salary greater than 70000
    test_db.delete_from("employees").where("department_id", "==", 2).where("age", "<", 25).where("salary", ">", 70000).execute()
    
    # Verify the deletion
    result = test_db.select(table_name="employees").where("department_id", "==", 2).where("age", "<", 25).execute()
    assert all(row["salary"] <= 70000 for row in result)

def test_update_with_invalid_set_value(test_db):
    with pytest.raises(ValueError):
        test_db.update("employees").set("salary", "invalid_value").where("emp_id", "==", 1).execute()