from .column import Column
from typing import Union, Dict, List, Any 
from .row import Row
from exceptions import RequiredColumnMissing, UnkownColumnInsert, MissingColumnsInRowInsert

RowData = Union[Dict[str, Any], List[Any]]

"""Table class for managing columns and rows."""
class Table:

    """Initialize the Table with a name, columns, and an empty list of rows."""
    def __init__(self, table_name:str, columns: list[Column]):
        self.table_name = table_name
        self.columns = columns
        self.rows: List[Row] = []
        self.column_map = {col.column_name: col for col in columns}
        self.required_columns = [col.column_name for col in columns if col.required or col.primary_key]

        if not isinstance(columns, list):
            raise TypeError("columns must be a list of Column objects")

        for col in columns:
            if not isinstance(col, Column):
                raise TypeError(
                    f"Expected Column object, got {type(col).__name__}"
                )

    """Insert a row into the table after validating it against the column definitions."""
    def insert_row(self, row : RowData):
        # 1. Normalize input: Convert the list into dict of rows
        data_dict: Dict[str,Any] ={}

        if isinstance(row, list):

            # Check if all values are proivded or not
            if len(self.columns) != len(row):
                raise MissingColumnsInRowInsert()
            # Map list values to column names by position
            for i,col in enumerate(self.columns):
                data_dict[col.column_name] = row[i]
        
        elif isinstance(row, dict):
            data_dict = row
        
        else:
            raise TypeError("Row must be a list or a dictionary.")

        # 2. Validate the row data provided with the columns definition
        self._validate_row(data_dict)

        # 3. Append row to rows of the table
        self.rows.append(Row(data_dict))

    def delete_rows(self, rows_to_delete: list[RowData]):
        print("deleteting rows")
        self.rows = [row 
                     for row in self.rows 
                     if row not in rows_to_delete]

    """Validate the row data against the column definitions."""
    def _validate_row(self, data_dict:Dict):

        self._required_columns_check(data_dict)

        # Check for unknown columns
        extra_keys = set(data_dict.keys()) - {col.column_name for col in self.columns}
        if extra_keys:
            raise UnkownColumnInsert(extra_keys)
            
    '''Check if any reuired column is missing, if so check if a default value can be substituted.'''
    def _required_columns_check(self, data_dict):

        for col in self.columns:
            if col.required and col.column_name not in data_dict:
                if col.default_value is not None:
                    data_dict[col.column_name] = col.default_value
                else:
                    raise RequiredColumnMissing(col.column_name)

            if col.primary_key:
                self._primary_key_check()

            value = data_dict.get(col.column_name)

            # Skip validation if value is None and column is not required
            if value is None and not col.required:
                continue

            # Use column's validate method
            col.validate_value(value)

    def _primary_key_check(self):
        pass

    """Get a string representation of the table, including its name, columns, and rows."""
    def __repr__(self):
        return f"Table(name={self.table_name}, columns={self.columns}, rows={self.rows})"

    """Get all rows from the table."""
    def get_rows(self):
        return self.rows

    """Get a string representation of the table, including its name and rows."""
    def __str__(self):
        output = f"Table: {self.table_name}\n"
        for row in self.rows:
            output += f"  {row}\n"
        return output

    """Get a column by name from the table."""
    def get_column(self, column_name: str):
        return self.column_map.get(column_name)
