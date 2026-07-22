from typing import Any

class Column:
    def __init__(self, name:str, data_type:type, is_nullable:bool=True, is_Required:bool=True,default_value:Any=None):
        self.name = name
        self.data_type = data_type
        self.is_nullable = is_nullable
        self.is_Required = is_Required
        self.default_value = default_value

    def __repr__(self):
        return f"Column(name={self.name}, data_type={self.data_type}, is_nullable={self.is_nullable}, default_value={self.default_value})"  
    
    def validate_value(self, value):
        if value is None and not self.is_nullable:
            raise ValueError(f"Column '{self.name}' cannot be null.")
        if value is not None and not isinstance(value, self.data_type):
            raise TypeError(f"Column '{self.name}' expects a value of type {self.data_type.__name__}.")
        return True
    
    def get_default_value(self):
        return self.default_value
    
    
