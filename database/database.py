from .table import Table

class Database:

    def __init__(self):
        self.tables = {}

    def create_table(self, name, columns):
        if name in self.tables:
            raise TypeError(f"{name} is already taken. Create a new table.")
        self.tables[name] = Table(name, columns)

        
    def insert_table_row(self, table_name: str, row: dict | list):

        if not isinstance(table_name,str):
            raise TypeError("Table name must be a string.")
        
        if table_name not in self.tables:
            raise TypeError(f"Table '{table_name}' does not exist.")
        
        target_table: Table = self.tables[table_name]
        target_table.insert_row(row)

    def get_table_rows(self,  table_name: str):
        if not isinstance(table_name,str):
            raise TypeError("Table name must be a string.")
        
        if table_name not in self.tables:
            raise TypeError(f"Table '{table_name}' does not exist.")
        
        target_table: Table = self.tables[table_name]
        return target_table.get_rows()
        