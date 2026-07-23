from .column import Column
from typing import Union, Dict, List, Any 
from .row import Row

RowData = Union[Dict[str, Any], List[Any]]

"""Table class for managing columns and rows."""
class Table:

    """Initialize the Table with a name, columns, and an empty list of rows."""
    def __init__(self, table_name:str, columns: list[Column]):
        self.table_name = table_name
        self.columns = columns
        self.rows: List[Row] = []
        self.column_map = {col.column_name: col for col in columns}

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
            # Check if all required columns were supplied or not
            if len(row) != len(self.columns):
                raise ValueError("Row length does not match number of columns.")
            
            # Map list values to column names by position
            for i,col in enumerate(self.columns):
                data_dict[col.column_name] = row[i]
        
        elif isinstance(row, dict):
            data_dict = row

            # Check if any reuired column is missing, if so check if a default value can be substituted.
            for col in self.columns:
                if col.is_Required and col.column_name not in data_dict:
                    if col.default_value:
                        data_dict[col.column_name] = col.default_value
                    else:
                        raise ValueError(f"Missing required column: '{col.column_name}'.")
            
            # Check for unknown columns
            extra_keys = set(data_dict.keys()) - {col.column_name for col in self.columns}
            if extra_keys:
                raise ValueError(f"Unknown columns in row: {extra_keys}")
        
        else:
            raise TypeError("Row must be a list or a dictionary.")

        # 2. Validate the row data provided with the columns definition
        self.validate_row(data_dict)

        # 3. Append row to rows of the table
        self.rows.append(Row(data_dict))

    """Validate the row data against the column definitions."""
    def validate_row(self, data_dict:Dict):
        for col in self.columns:
            value = data_dict.get(col.column_name)

            # Skip validation if value is None and column is not required
            if value is None and not col.is_Required:
                continue

            # Use column's validate method
            col.validate_value(value)

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
