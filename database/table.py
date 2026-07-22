from .column import Column
from typing import Union, Dict, List, Any 
from .row import Row

RowData = Union[Dict[str, Any], List[Any]]

class Table:
    def __init__(self, name:str, columns: list[Column]):
        self.name = name
        if not isinstance(columns, list):
            raise TypeError("columns must be a list of Column objects")

        for col in columns:
            if not isinstance(col, Column):
                raise TypeError(
                    f"Expected Column object, got {type(col).__name__}"
                )
        self.columns = columns
        self.rows: List[Row] = []

    # Insert a new row into the table
    def insert_row(self, row : RowData):
        # 1. Normalize input: Convert the list into dict of rows
        data_dict: Dict[str,Any] ={}

        if isinstance(row, list):
            # Check if all required columns were supplied or not
            if len(row) != len(self.columns):
                raise ValueError("Row length does not match number of columns.")
            
            # Map list values to column names by position
            for i,col in enumerate(self.columns):
                data_dict[col.name] = row[i]
        
        elif isinstance(row, dict):
            data_dict = row

            # Check if any reuired column is missing, if so check if a default value can be substituted.
            for col in self.columns:
                if col.is_Required and col.name not in data_dict:
                    if col.default_value:
                        data_dict[col.name] = col.default_value
                    else:
                        raise ValueError(f"Missing required column: '{col.name}'.")
            
            # Check for unknown columns
            extra_keys = set(data_dict.keys()) - {col.name for col in self.columns}
            if extra_keys:
                raise ValueError(f"Unknown columns in row: {extra_keys}")
        
        else:
            raise TypeError("Row must be a list or a dictionary.")

        # 2. Validate the row data provided with the columns definition
        self.validate_row(data_dict)

        # 3. Append row to rows of the table
        self.rows.append(Row(data_dict))

    def validate_row(self, data_dict:Dict):
        for col in self.columns:
            value = data_dict.get(col.name)

            # Skip validation if value is None and column is not required
            if value is None and not col.is_Required:
                continue

            # Use column's validate method
            col.validate_value(value)

    def __repr__(self):
        return f"Table(name={self.name}, columns={self.columns}, rows={self.rows})"
    
    def get_rows(self):
        return self.rows
    
    def __str__(self):
        output = f"Table: {self.name}\n"
        for row in self.rows:
            output += f"  {row}\n"
        return output
