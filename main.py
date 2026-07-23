from database import Database, Column

db = Database()

# db.create_table(
#     "employees",
#     [
#         Column("id", int),
#         Column("name", str),
#         Column("salary", float)
#     ]
# )
db.create_table(
    table_name= "employees",
    columns=[
        {"name": "id", "data_type": int},
        {"name": "name", "data_type": str},
        {"name": "salary", "data_type": float}
    ]
)   

db.insert_table_row(
    "employees",
    {
        "id": 1,
        "name": "Alice",
        "salary": 50000.00
    }
)
db.insert_table_row(
    "employees",
    {
        "id": 2,
        "name": "Anna",
        "salary": 56000.00
    }
)

print(db.get_table_rows("employees"))
print(db.select("employees").where("salary", "<", 52000.00).execute())