"""
department_data.py

department_id, department_name, location, budget
"""

DEPARTMENTS = [
    [1, "Engineering", "Delhi", 5000000.00],
    [2, "Finance", "Mumbai", 2500000.00],
    [3, "Human Resources", "Pune", 1500000.00],
    [4, "Customer Support", "Hyderabad", 2000000.00],
    [5, "Sales", "Chennai", 4000000.00],
]


def load_departments(db):
    for row in DEPARTMENTS:
        db.insert_table_row("departments", row)