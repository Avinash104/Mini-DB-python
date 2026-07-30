import pytest
from database import UnknownColumnError, UnknownGroupbyColumn, QueryInvalidAggregationError

"""Test cases for the query builder functionality of the Database class."""

"""Test cases for where clause"""
def test_where_equal(test_db):
    result = test_db.select(table_name="employees", column_list=["emp_id", "name", "salary", "age"])
    result = result.where("emp_id", "==", 1).execute()
    assert len(result) == 1
    assert result[0]["emp_id"] == 1

def test_where_greater_than(test_db):
    result = test_db.select(table_name="employees", column_list=["emp_id", "name", "salary", "age"])
    result = result.where("salary", ">", 90000.00).execute()
    assert all(row["salary"] > 90000.00 for row in result)

def test_multiple_where_conditions(test_db):
    result = test_db.select(table_name="employees", column_list=["emp_id", "name", "salary", "age"])
    result = result.where("emp_id", "<", 20).where("salary", ">", 90000.00).execute()
    assert all(row["emp_id"] < 20 and row["salary"] > 90000.00 for row in result)

def test_where_unknown_column(test_db):
    with pytest.raises(UnknownColumnError):
        test_db.select(table_name="employees", column_list=["emp_id", "name", "salary", "age"]).where("unknown_column", "==", 1).execute()    

"""Test cases for projection and selection of columns"""
def test_select_specific_columns(test_db):
    result = test_db.select(table_name="employees", column_list=["emp_id", "name"]).execute()
    assert all(set(row.keys()) == {"emp_id", "name"} for row in result)

def test_select_all_columns(test_db):
    result = test_db.select(table_name="employees", column_list=["emp_id", "name", "salary", "age"]).execute()
    assert all(set(row.keys()) == {"emp_id", "name", "salary", "age"} for row in result)

"""Test cases for ordering and limiting results"""
def test_order_by_ascending(test_db):
    result = test_db.select(table_name="employees", column_list=["emp_id", "name"]).order_by("emp_id").execute()
    emp_ids = [row["emp_id"] for row in result]
    assert emp_ids == sorted(emp_ids)

def test_order_by_descending(test_db):
    result = test_db.select(table_name="employees", column_list=["emp_id", "name"]).order_by("emp_id", reversed=True).execute()
    emp_ids = [row["emp_id"] for row in result]
    assert emp_ids == sorted(emp_ids, reverse=True)

def test_limit_results(test_db):
    result = test_db.select(table_name="employees", column_list=["emp_id", "name"]).limit(5).execute()
    assert len(result) == 5

def test_order_by_and_limit(test_db):
    result = test_db.select(table_name="employees", column_list=["emp_id", "name"]).order_by("emp_id").limit(3).execute()
    emp_ids = [row["emp_id"] for row in result]
    assert emp_ids == sorted(emp_ids)[:3]

"""Test cases for group by and aggregation functions"""
def test_group_by_and_count(test_db):
    result = test_db.select(table_name="employees").group_by("department_id").count().execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "count" in row for row in result)

def test_group_by_and_avg(test_db):
    result = test_db.select(table_name="employees").group_by("department_id").avg("salary").execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "avg_salary" in row for row in result)

def test_group_by_and_sum(test_db):
    result = test_db.select(table_name="employees").group_by("department_id").sum("salary").execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "sum_salary" in row for row in result)

def test_group_by_and_max(test_db):
    result = test_db.select(table_name="employees").group_by("department_id").max("salary").execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "max_salary" in row for row in result)

def test_group_by_and_min(test_db):
    result = test_db.select(table_name="employees").group_by("department_id").min("salary").execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "min_salary" in row for row in result)

# def test_group_by_with_multiple_aggregations(test_db):
#     result = test_db.select(table_name="employees").group_by("department_id").count().avg("salary").execute()
#     assert isinstance(result, list)
#     assert all(isinstance(row, dict) for row in result)
#     assert all("department_id" in row and "count" in row and "avg_salary" in row for row in result)

def test_group_by_with_ordering(test_db):
    result = test_db.select(table_name="employees").group_by("department_id").count().order_by("department_id").execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "count" in row for row in result)
    department_ids = [row["department_id"] for row in result]
    assert department_ids == sorted(department_ids)

def test_group_by_with_limit(test_db):
    result = test_db.select(table_name="employees").group_by("department_id").count().limit(2).execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "count" in row for row in result)
    assert len(result) == 2

def test_group_by_with_ordering_and_limit(test_db):
    result = test_db.select(table_name="employees").group_by("department_id").count().order_by("department_id").limit(2).execute()
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    assert all("department_id" in row and "count" in row for row in result)
    department_ids = [row["department_id"] for row in result]
    assert department_ids == sorted(department_ids)[:2]

# def test_group_by_with_multiple_aggregations_and_ordering(test_db):
#     result = test_db.select(table_name="employees").group_by("department_id").count().avg("salary").order_by("department_id").execute()
#     assert isinstance(result, list)
#     assert all(isinstance(row, dict) for row in result)
#     assert all("department_id" in row and "count" in row and "avg_salary" in row for row in result)
#     department_ids = [row["department_id"] for row in result]
#     assert department_ids == sorted(department_ids)

# def test_group_by_with_multiple_aggregations_and_limit(test_db):
#     result = test_db.select(table_name="employees").group_by("department_id").count().avg("salary").limit(2).execute()
#     assert isinstance(result, list)
#     assert all(isinstance(row, dict) for row in result)
#     assert all("department_id" in row and "count" in row and "avg_salary" in row for row in result)
#     assert len(result) == 2

# def test_group_by_with_multiple_aggregations_ordering_and_limit(test_db):
#     result = test_db.select(table_name="employees").group_by("department_id").count().avg("salary").order_by("department_id").limit(2).execute()
#     assert isinstance(result, list)
#     assert all(isinstance(row, dict) for row in result)
#     assert all("department_id" in row and "count" in row and "avg_salary" in row for row in result)
#     department_ids = [row["department_id"] for row in result]
#     assert department_ids == sorted(department_ids)[:2]

def test_group_by_with_unknown_column(test_db):
    with pytest.raises(UnknownGroupbyColumn):
        test_db.select(table_name="employees").group_by("unknown_column").count().execute()

def test_group_by_with_unknown_aggregation(test_db):
    with pytest.raises(QueryInvalidAggregationError):
        test_db.select(table_name="employees").group_by("department_id").unknown_aggregation("salary").execute()

# def test_group_by_with_invalid_ordering_column(test_db):
#     with pytest.raises(ValueError):
#         test_db.select(table_name="employees").group_by("department_id").count().order_by("unknown_column").execute()

# def test_group_by_with_invalid_limit_value(test_db):
#     with pytest.raises(ValueError):
#         test_db.select(table_name="employees").group_by("department_id").count().limit(-1).execute()

# def test_group_by_with_no_aggregations(test_db):
#     with pytest.raises(ValueError):
#         test_db.select(table_name="employees").group_by("department_id").execute()


