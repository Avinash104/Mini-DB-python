"""
employee_data.py

Sample employee dataset for MiniDB.
The loader assumes you've already created the 'employees' table.
"""

EMPLOYEES = [
    [1, "Alice Johnson", 1, None, 95000.00, 42, 18, "Delhi", 101],
    [2, "Bob Smith", 2, 1, 52000.00, 27, 4, "Mumbai", 102],
    [3, "Charlie Brown", 1, 1, 73000.00, 33, 9, "Delhi", 101],
    [4, "David Wilson", 4, 1, 48000.00, 25, 2, "Hyderabad", 104],
    [5, "Eva Thomas", 5, 1, 68000.00, 31, 7, "Chennai", 105],
    [6, "Frank Miller", 2, 1, 89000.00, 38, 14, "Mumbai", 102],
    [7, "Grace Lee", 3, 1, 62000.00, 29, 6, "Pune", 103],
    [8, "Henry Walker", 1, 1, 81000.00, 35, 11, "Delhi", 106],
    [9, "Irene Hall", 5, 5, 56000.00, 28, 5, "Chennai", 108],
    [10, "Jack White", 4, 4, 45000.00, 24, 1, "Hyderabad", 104],
    [11, "Karen Young", 3, 7, 74000.00, 34, 10, "Pune", 103],
    [12, "Leo Harris", 2, 6, 60000.00, 30, 6, "Mumbai", 107],
    [13, "Mona Scott", 1, 8, 77000.00, 32, 8, "Delhi", 106],
    [14, "Nathan King", 4, 4, 51000.00, 27, 3, "Hyderabad", 109],
    [15, "Olivia Green", 5, 5, 92000.00, 40, 16, "Chennai", 110],
    [16, "Peter Adams", 2, 6, 65000.00, 31, 7, "Mumbai", 102],
    [17, "Quinn Baker", 3, 11, 54000.00, 26, 3, "Pune", 103],
    [18, "Rachel Carter", 1, 8, 70000.00, 33, 9, "Delhi", 101],
    [19, "Steve Davis", 4, 14, 47000.00, 25, 2, "Hyderabad", 104],
    [20, "Tina Evans", 5, 15, 61000.00, 29, 5, "Chennai", 105],
    [21, "Uma Foster", 2, 6, 83000.00, 36, 12, "Mumbai", 107],
    [22, "Victor Gray", 1, 8, 76000.00, 34, 10, "Delhi", 106],
    [23, "Wendy Hill", 3, 11, 59000.00, 28, 4, "Pune", 103],
    [24, "Xavier Irving", 5, 15, 64000.00, 30, 6, "Chennai", 108],
    [25, "Yara James", 4, 14, 53000.00, 27, 4, "Hyderabad", 109],
    [26, "Zack Kelly", 2, 21, 72000.00, 33, 8, "Mumbai", 107],
    [27, "Aaron Lewis", 1, 22, 84000.00, 37, 13, "Delhi", 101],
    [28, "Bella Moore", 3, 11, 57000.00, 29, 5, "Pune", 103],
    [29, "Cody Nelson", 5, 15, 69000.00, 32, 7, "Chennai", 110],
    [30, "Diana Owens", 4, 14, 49500.00, 26, 3, "Hyderabad", 104],
    [31, "Ethan Parker", 2, 21, 91000.00, 39, 15, "Mumbai", 102],
    [32, "Fiona Reed", 1, 22, 78000.00, 34, 10, "Delhi", 106],
    [33, "George Stewart", 3, 11, 61000.00, 30, 6, "Pune", 103],
    [34, "Hannah Turner", 5, 15, 66000.00, 31, 7, "Chennai", 108],
    [35, "Ian Underwood", 4, 14, 52000.00, 28, 4, "Hyderabad", 109],
    [36, "Julia Vincent", 2, 21, 74000.00, 34, 9, "Mumbai", 107],
    [37, "Kevin Wright", 1, 22, 87000.00, 38, 14, "Delhi", 101],
    [38, "Lily Xu", 3, 11, 56000.00, 27, 4, "Pune", 103],
    [39, "Mike Young", 5, 15, 71000.00, 33, 8, "Chennai", 110],
    [40, "Nina Zimmerman", 4, 14, 50000.00, 26, 2, "Hyderabad", 104],
    [41, "Oscar Allen", 2, 21, 94000.00, 41, 17, "Mumbai", 102],
    [42, "Paula Brooks", 1, 22, 82000.00, 36, 11, "Delhi", 106],
    [43, "Ryan Cooper", 3, 11, 63000.00, 31, 7, "Pune", 103],
    [44, "Sara Diaz", 5, 15, 67000.00, 30, 6, "Chennai", 108],
    [45, "Tom Edwards", 4, 14, 51500.00, 27, 3, "Hyderabad", 109],
    [46, "Usha Fernandez", 2, 21, 76000.00, 35, 10, "Mumbai", 107],
    [47, "Vikram Gupta", 1, 22, 88000.00, 39, 15, "Delhi", 101],
    [48, "Will Howard", 3, 11, 60000.00, 29, 5, "Pune", 103],
    [49, "Xena Iyer", 5, 15, 73500.00, 34, 9, "Chennai", 110],
    [50, "Yusuf Khan", 4, 14, 54000.00, 28, 4, "Hyderabad", 104],
    [51, "Zara Malik", 2, 21, 80000.00, 36, 12, "Mumbai", 102],
    [52, "Aditya Nair", 1, 22, 86000.00, 38, 14, "Delhi", 106],
    [53, "Bhavna Patel", 3, 11, 58500.00, 28, 5, "Pune", 103],
    [54, "Chirag Rao", 5, 15, 70000.00, 32, 8, "Chennai", 105],
    [55, "Deepa Sharma", 4, 14, 50500.00, 26, 2, "Hyderabad", 109],
    [56, "Farhan Siddiqui", 2, 21, 79000.00, 35, 11, "Mumbai", 107],
    [57, "Gauri Verma", 1, 22, 90000.00, 40, 16, "Delhi", 101],
    [58, "Harish Yadav", 3, 11, 61500.00, 30, 6, "Pune", 103],
    [59, "Ishita Mehta", 5, 15, 72000.00, 33, 9, "Chennai", 108],
    [60, "Jatin Kapoor", 4, 14, 52500.00, 27, 3, "Hyderabad", 104],
]


def load_employees(db):
    for row in EMPLOYEES:
        db.insert_table_row("employees", row)