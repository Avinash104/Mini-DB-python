from .table import Table
from .column import Column
from exceptions import (TableAlreadyExistsError, 
                        TableNotFoundError, 
                        TableNameError, 
                        TableDoesNotExistError, 
                        TableCreationColumnError)

class Database:

    def __init__(self):
        self.tables = {}

    def create_table(self, table_name: str, columns: list):
        if table_name in self.tables:
            raise TableAlreadyExistsError(table_name)
        
        processed_columns = []

        for i,col in enumerate(columns):
            # User passed a Column object directly 
            if isinstance(col, Column):
                processed_columns.append(col)
            # User passed ("name", type)
            elif isinstance(col, (tuple, list)):
                if len(col) < 2:
                    raise TableCreationColumnError(table_name, index=i)
                col_name, col_type = col
                processed_columns.append(Column(column_name=col_name, data_type=col_type))
            # User passed {"name": "...", "data_type": ...}
            elif isinstance(col, dict):
                if "name" not in col or "data_type" not in col:
                    raise TableCreationColumnError(table_name, index=i)
                processed_columns.append(Column(column_name=col["name"], data_type=col["data_type"]))
            else:
                raise TableCreationColumnError(table_name, index=i)

        self.tables[table_name] = Table(table_name, columns=processed_columns)

        
    def insert_table_row(self, table_name: str, row: dict | list):

        if not isinstance(table_name,str):
            raise TableNameError(table_name)
        
        if table_name not in self.tables:
            raise TableNotFoundError(table_name)
        
        target_table: Table = self.tables[table_name]
        target_table.insert_row(row)

    def get_table_rows(self,  table_name: str):
        if not isinstance(table_name,str):
            raise TableNameError(table_name)
        
        if table_name not in self.tables:
            raise TableDoesNotExistError(table_name)
        
        target_table: Table = self.tables[table_name]
        return target_table.get_rows()
        