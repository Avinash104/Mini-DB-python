"""
project_data.py

project_id, project_name, department_id, budget, client
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


def load_projects(db):
    for row in PROJECTS:
        db.insert_table_row("projects", row)