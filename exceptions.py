# Base exception for your entire library
class MiniDBError(Exception):
    """Base exception for all MiniDB errors."""
    pass

# Domain-specific base errors
class DatabaseError(MiniDBError):
    """Base for database-level errors."""
    pass

class TableError(DatabaseError):
    """Base for table-related errors."""
    pass

class TableAlreadyExistsError(TableError):
    """Raised when creating a table that already exists."""
    def __init__(self, table_name: str):
        self.table_name = table_name
        
        message = f"Table '{table_name}' already exists. Choose a different name."

        super().__init__(message)

class TableDoesNotExistError(TableError):
    """Raised when creating a table that already exists."""
    def __init__(self, table_name: str):
        self.table_name = table_name
        
        message = f"Table '{table_name}' does not exist."
        super().__init__(message)

class TableNotFoundError(TableError):
    """Raised when accessing a non-existent table."""
    def __init__(self, table_name: str):
        self.table_name = table_name
        
        message = f"Table '{table_name}' does not exist."

        super().__init__(message)

class TableNameError(TableError):
    """Raised when wrong table name is provided."""
    def __init__(self, table_name: str):
        self.table_name = table_name
        
        message = f"Table '{table_name}' isn't a string."

        super().__init__(message)

class TableCreationColumnError(TableError):
    """Raised when wrong Column list is provided during table creation."""
    def __init__(self, table_name: str, index: int):
        self.table_name = table_name
        
        message = f"Column definition at index {index} must be a tuple/list of (name, type) for table '{table_name}'."

        super().__init__(message)

# Column errors
class ColumnError(DatabaseError):
    """Base for column-related errors."""
    pass

class InvalidColumnTypeError(ColumnError):
    pass

class UnknownColumnError(ColumnError):
    pass

# Row errors
class RowError(DatabaseError):
    """Base for row-related errors."""
    pass

class RowValidationError(RowError):
    pass

class DuplicatePrimaryKeyError(RowError):
    pass   