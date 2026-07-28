import pytest
from .conftest import test_db

def test_inner_join(test_db):
    result = test_db.select(table_name="employees").inner_join("departments", "department_id", "id").execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "id" in row for row in result)

def test_left_join(test_db):
    result = test_db.select(table_name="employees").left_join("departments", "department_id", "id").execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "id" in row for row in result)

def test_right_join(test_db):
    result = test_db.select(table_name="employees").right_join("departments", "department_id", "id").execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "id" in row for row in result)

def test_multiple_joins(test_db):
    result = test_db.select(table_name="employees").inner_join("departments", "department_id", "id").left_join("projects", "project_id", "id").execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "id" in row and "project_id" in row for row in result)

def test_join_with_conditions(test_db):
    result = test_db.select(table_name="employees").inner_join("departments", "department_id", "id").where("salary", ">", 50000).execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "id" in row and "salary" in row for row in result)
    assert all(row["salary"] > 50000 for row in result)

def test_join_with_group_by(test_db):
    result = test_db.select(table_name="employees").inner_join("departments", "department_id", "id").group_by("department_id").count().execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "count" in row for row in result)

def test_join_with_order_by(test_db):
    result = test_db.select(table_name="employees").inner_join("departments", "department_id", "id").order_by("salary").execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "id" in row and "salary" in row for row in result)
    salaries = [row["salary"] for row in result]
    assert salaries == sorted(salaries)

def test_join_with_limit(test_db):
    result = test_db.select(table_name="employees").inner_join("departments", "department_id", "id").limit(5).execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "id" in row for row in result)
    assert len(result) <= 5

def test_join_with_multiple_conditions(test_db):
    result = test_db.select(table_name="employees").inner_join("departments", "department_id", "id").where("salary", ">", 50000).where("age", "<", 30).execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "id" in row and "salary" in row and "age" in row for row in result)
    assert all(row["salary"] > 50000 and row["age"] < 30 for row in result)

def test_join_with_group_by_and_order_by(test_db):
    result = test_db.select(table_name="employees").inner_join("departments", "department_id", "id").group_by("department_id").count().order_by("count").execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "count" in row for row in result)
    counts = [row["count"] for row in result]
    assert counts == sorted(counts)

def test_join_with_group_by_and_limit(test_db):
    result = test_db.select(table_name="employees").inner_join("departments", "department_id", "id").group_by("department_id").count().limit(3).execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "count" in row for row in result)
    assert len(result) <= 3

def test_join_with_order_by_and_limit(test_db):
    result = test_db.select(table_name="employees").inner_join("departments", "department_id", "id").order_by("salary").limit(4).execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "id" in row and "salary" in row for row in result)
    salaries = [row["salary"] for row in result]
    assert salaries == sorted(salaries)
    assert len(result) <= 4

def test_join_missing_table(test_db):
    with pytest.raises(ValueError):
        test_db.select(table_name="employees").inner_join("non_existing_table", "department_id", "id").execute()

def test_join_unknown_column(test_db):
    with pytest.raises(ValueError):
        test_db.select(table_name="employees").inner_join("departments", "unknown_column", "id").execute()

def test_join_returns_expected_columns(test_db):
    result = test_db.select(table_name="employees", column_list=["employees.emp_id", "departments.department_name"]).inner_join("departments", "department_id", "id").execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("emp_id" in row and "department_name" in row for row in result)

