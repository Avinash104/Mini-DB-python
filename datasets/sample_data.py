from .employee_data import load_employees
from .department_data import load_departments
from .project_data import load_projects
from .salary_grade_data import load_salary_grades

from database import Column

def load_sample_data(db):

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

    db.create_table(
        "salary_grades",
        [
            Column("grade", str, primary_key=True),
            Column("min_salary", float),
            Column("max_salary", float),
            Column("bonus_percent", int),
        ],
    )

    load_departments(db)
    load_projects(db)
    load_salary_grades(db)
    load_employees(db)