from database import Column

"""
employee_data.py
"""

EMPLOYEES = [
    [1, "Alice Johnson", 1, None, 1000.00, 42, 18, "Delhi", 101],
    [2, "Bob Smith", 2, 1, 2000.00, 27, 4, "Mumbai", 102],
    [3, "Charlie Brown", 1, 1, 3000.00, 33, 9, "Delhi", 101],
    [4, "David Wilson", 4, 1, 8000.00, 25, 2, "Hyderabad", 104],
    [5, "Eva Thomas", 5, 1, 8000.00, 31, 7, "Chennai", 105],
    [6, "Frank Miller", 2, 1, 9000.00, 38, 14, "Mumbai", 102],
    [7, "Grace Lee", 3, 1, 2000.00, 29, 6, "Pune", 103],
    [8, "Henry Walker", 1, 1, 1000.00, 35, 11, "Delhi", 106],
    [9, "Irene Hall", 5, 5, 1000.00, 28, 5, "Chennai", 108],
    [10, "Jack White", 4, 4, 1000.00, 24, 1, "Hyderabad", 104]
]

"""
department_data.py
"""

DEPARTMENTS = [
    [1, "Engineering", "Delhi", 5000000.00],
    [2, "Finance", "Mumbai", 2500000.00],
    [3, "Human Resources", "Pune", 1500000.00],
    [4, "Customer Support", "Hyderabad", 2000000.00],
    [5, "Sales", "Chennai", 4000000.00],
]
"""
project_data.py
"""

PROJECTS = [
    [101, "Phoenix", 1, 1200000.00, "Microsoft"],
    [102, "Mercury", 2, 850000.00, "JP Morgan"],
    [103, "Atlas", 3, 500000.00, "Infosys"],
    [104, "Nova", 4, 650000.00, "Amazon"],
    [105, "Titan", 5, 1750000.00, "Google"],
    [106, "Orion", 1, 2100000.00, "Adobe"],
    [107, "Zenith", 2, 950000.00, "Deloitte"],
    [108, "Vertex", 5, 1850000.00, "Apple"],
    [109, "Nimbus", 4, 700000.00, "IBM"],
    [110, "Apollo", 5, 1600000.00, "Oracle"],
]

def load_employees(db):
    for row in EMPLOYEES:
        db.insert_table_row("employees", row)

def load_departments(db):
    for row in DEPARTMENTS:
        db.insert_table_row("departments", row)

def load_projects(db):
    for row in PROJECTS:
        db.insert_table_row("projects", row)

def load_test_data(db):

    db.create_table(
        "employees",
        [
            Column("emp_id", int, primary_key=True),
            Column("name", str),
            Column("department_id", int),
            Column("manager_id", int),
            Column("salary", float),
            Column("age", int),
            Column("experience", int),
            Column("city", str),
            Column("project_id", int),
        ],
    )

    db.create_table(
        "departments",
        [
            Column("department_id", int, primary_key=True),
            Column("department_name", str),
            Column("location", str),
            Column("budget", float),
        ],
    )

    db.create_table(
        "projects",
        [
            Column("project_id", int, primary_key=True),
            Column("project_name", str),
            Column("department_id", int),
            Column("budget", float),
            Column("client", str),
        ],
    )

    load_departments(db)
    load_projects(db)
    load_employees(db)