from .table import Table
from .column import Column
from .querybuilder import QueryBuilder
from exceptions import (TableAlreadyExistsError, 
                        TableNotFoundError, 
                        TableNameError, 
                        TableDoesNotExistError, 
                        TableCreationColumnError)

"""
Database class for managing tables and rows.
"""
class Database:

    """Initialize the Database with an empty dictionary of tables."""
    def __init__(self):
        self.tables = {}

    """Create a new table in the database."""
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

    """Get a table by name."""
    def get_table(self, table_name: str):
        if table_name not in self.tables:
            raise TableNotFoundError(table_name)
        return self.tables[table_name]

    """Insert a row into a table."""
    def insert_table_row(self, table_name: str, row: dict | list):

        if not isinstance(table_name,str):
            raise TableNameError(table_name)
        
        if table_name not in self.tables:
            raise TableNotFoundError(table_name)
        
        target_table: Table = self.tables[table_name]
        target_table.insert_row(row)

    """Get all rows from a table."""
    def get_table_rows(self,  table_name: str):
        if not isinstance(table_name,str):
            raise TableNameError(table_name)
        
        if table_name not in self.tables:
            raise TableDoesNotExistError(table_name)
        
        target_table: Table = self.tables[table_name]
        return target_table.get_rows()

    """Select rows from a table based on conditions."""
    def select(self, table_name: str, column_list: list[str] | None = None):
        if table_name not in self.tables:
            raise TableDoesNotExistError(table_name)

        return QueryBuilder(self,table_name,column_list)       
     
    """Update the selected rows based on conditions."""
    def update(self, table_name: str):
        if table_name not in self.tables:
            raise TableDoesNotExistError(table_name)

        return QueryBuilder(self,table_name)        
     
    """Select rows from a table based on conditions."""
    def delete_from(self, table_name: str):
        print("delete from called")
        if table_name not in self.tables:
            raise TableDoesNotExistError(table_name)

        return QueryBuilder(self,table_name, query_type="DELETE")        