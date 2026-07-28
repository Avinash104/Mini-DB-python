from database import Database, Column
from datasets import load_sample_data

db = Database()

"""Load the sample data to initialize the mini-DB."""
load_sample_data(db)

"""where testing"""
# print(db.get_table_rows("employees"))
# print(db.select(table_name="employees", column_list=["emp_id", "name", "salary", "age"]).
#         where("emp_id", "<", 20).
#         where("salary", ">", 90000.00).
#         execute())
# print(db.select(table_name="employees", column_list=["emp_id", "name", "salary"]).
#         where("salary", ">", 90000.00).execute())
# print(db.select(table_name="employees", column_list=["name", "salary"]).
#         where("salary", "<", 82000.00).
#         order_by(column="id", reversed=True).
#         limit(1).
#         execute())

# print(db.update(table_name="employees").
#         where("emp_id", "==", 1).
#         set_cols({"salary": 90000.00, "age": 19}).
#         execute())
# print(db.select(table_name="employees", column_list=["emp_id", "name", "salary", "age"]).
#       where("emp_id", "==", 1).
#       execute())

# print(db.select(table_name="employees", column_list=["emp_id", "name", "salary", "age"]).
#         where("emp_id", "<", 20).
#         where("salary", ">", 90000.00).
#         execute())

# print(db.select(table_name="employees", column_list=["city"]).group_by("city").avg("salary"))

"""UPDATE"""
# print(db.update(table_name="employees").
#         where("emp_id", "==", 1).
#         set({"name": "Kira"}).
#         execute())

"""DELETE"""
# print(db.select(table_name="employees").where("emp_id", "==", 1).execute())
# print(db.delete_from(table_name="employees").
#         where("emp_id", "==", 1).
#         execute())
# print(db.select(table_name="employees").where("emp_id", "==", 1).execute())
# print(db.get_table_rows("employees"))

# print(db.get_table_rows("employees"))

"""Testing Group_by"""
# print(db.select(table_name="employees").
#       # where("age", "<", 28).
#       group_by("department_id").
#       avg("salary").
#       order_by("department_id").
#       execute())

# print(db.select(table_name="employees").
#       group_by("department_id").
#       order_by("department_id").execute())

"""Join testing"""
print(db.select("employees", column_list=["employees.emp_id", "employees.name", 
                                          "employees.salary","departments.department_name", 
                                          "projects.project_name"])
  .join(
      "departments",
      left_key="employees.department_id",
      right_key="departments.department_id"
  ) 
  .join(
      "projects",
      left_key="employees.project_id",
      right_key="projects.project_id"
  )
  .where("employees.salary", ">", 90000.00) 
  .order_by("employees.salary") 
  .execute())