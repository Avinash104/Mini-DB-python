from database import Database, Column
from datasets import load_sample_data

db = Database()

"""Load the sample data to initialize the mini-DB."""
load_sample_data(db)

# print(db.get_table_rows("employees"))
print(db.select(table_name="employees", column_list=["emp_id", "name", "salary", "age"]).
        where("emp_id", "<", 20).
        where("salary", ">", 90000.00).
        avg("salary"))
# print(db.select(table_name="employees", column_list=["emp_id", "name", "salary"]).
#         where("salary", ">", 90000.00).execute())
# print(db.select(table_name="employees", column_list=["name", "salary"]).
#         where("salary", "<", 82000.00).
#         order_by(column="id", reversed=True).
#         limit(1).
#         execute())

print(db.update(table_name="employees").
        where("emp_id", "==", 1).
        set_cols({"salary": 90000.00, "age": 19}).
        execute())
print(db.select(table_name="employees", column_list=["emp_id", "name", "salary", "age"]).
      where("emp_id", "==", 1).
      execute())

print(db.select(table_name="employees", column_list=["emp_id", "name", "salary", "age"]).
        where("emp_id", "<", 20).
        where("salary", ">", 90000.00).
        execute())

print(db.select(table_name="employees", column_list=["city"]).group_by("city").avg("salary"))

# print(db.update(table_name="employees").
#         where("id", "==", 1).
#         set_cols({"name": "Kira"}).
#         execute())
# print(db.get_table_rows("employees"))