"""
salary_grade_data.py

grade, min_salary, max_salary, bonus_percent
"""

SALARY_GRADES = [
    ["A", 90000.00, 120000.00, 20],
    ["B", 80000.00, 89999.99, 15],
    ["C", 70000.00, 79999.99, 12],
    ["D", 60000.00, 69999.99, 10],
    ["E", 50000.00, 59999.99, 8],
    ["F", 0.00, 49999.99, 5],
]


def load_salary_grades(db):
    for row in SALARY_GRADES:
        db.insert_table_row("salary_grades", row)