from typing import Any

from exceptions import ColumnNotNullableError, ColumnTypeMismatchError

"""Column class for defining the structure of a table column."""
class Column:

    """Initialize the Column with its name, data type, and constraints."""
    def __init__(self, column_name:str, 
                 data_type:type, 
                 is_nullable:bool=True, 
                 is_Required:bool=True,
                 default_value:Any=None, 
                 is_Primary:bool=False):
        self.column_name = column_name
        self.data_type = data_type
        self.is_nullable = is_nullable
        self.is_Required = is_Required
        self.default_value = default_value
        self.is_Primary = is_Primary

    """Get a string representation of the column, including its name and data type."""
    def __repr__(self):
        return f"Column(name={self.column_name}, data_type={self.data_type}, is_nullable={self.is_nullable}, default_value={self.default_value})"  

    """Validate a value against the column's data type and constraints."""
    def validate_value(self, value):
        if value is None and not self.is_nullable:
            raise ColumnNotNullableError(self.column_name)
        if value is not None and not isinstance(value, self.data_type):
            raise ColumnTypeMismatchError(self.column_name, self.data_type, type(value))
        return True

    """Get the default value of the column."""
    def get_default_value(self):
        return self.default_value
    
    
