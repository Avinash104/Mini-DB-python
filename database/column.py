from typing import Any

from .exceptions import ColumnNotNullableError, ColumnTypeMismatchError

"""Column class for defining the structure of a table column."""
class Column:

    """Initialize the Column with its name, data type, and constraints."""
    def __init__(self, column_name:str, 
                 data_type:type, 
                 nullable:bool=True, 
                 required:bool=False,
                 default_value:Any=None, 
                 primary_key:bool=False):
        self.column_name = column_name
        self.data_type = data_type
        self.nullable = nullable
        self.default_value = default_value
        self.primary_key = primary_key
        self.required = required if not self.primary_key else True

    """Get a string representation of the column, including its name and data type."""
    def __repr__(self):
        return f"Column(name={self.column_name}, data_type={self.data_type}, nullable={self.nullable}, default_value={self.default_value})"  

    """Validate a value against the column's data type and constraints."""
    def validate_value(self, value):
        if value is None and not self.nullable:
            raise ColumnNotNullableError(self.column_name)
        if value is not None and not isinstance(value, self.data_type):
            raise ColumnTypeMismatchError(self.column_name, self.data_type, type(value))
        return True

    """Get the default value of the column."""
    def get_default_value(self):
        return self.default_value
    
    
