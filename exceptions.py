"""Base exception for your entire library"""
class MiniDBError(Exception):
    """Base exception for all MiniDB errors."""
    pass

"""Base for database-level errors."""
class DatabaseError(MiniDBError):
    """Base for database-level errors."""
    pass

"""Base for table-related errors."""
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

"""Base for column-related errors."""
class ColumnError(DatabaseError):
    """Base for column-related errors."""
    pass

class InvalidColumnTypeError(ColumnError):
    pass

class ColumnTypeMismatchError(ColumnError):
    def __init__(self, column_name: str, expected_type: type, received_type: type):
        self.column_name = column_name
        self.expected_type = expected_type
        self.received_type = received_type

        message = f"Column '{column_name}' expects type '{expected_type.__name__}', but received type '{received_type.__name__}'."

        super().__init__(message)

class ColumnValueError(ColumnError):
    def __init__(self, column_name: str, message: str):
        self.column_name = column_name
        self.message = message

        full_message = f"Column '{column_name}': {message}"

        super().__init__(full_message)

class ColumnNotNullableError(ColumnError):
    def __init__(self, column_name: str):
        self.column_name = column_name

        message = f"Column '{column_name}' cannot be null."

        super().__init__(message)

class UnknownColumnError(ColumnError):
    def __init__(self, column_name: str, table_name: str):
        self.column_name = column_name
        self.table_name = table_name

        message = f"Column '{column_name}' does not exist in table '{table_name}'."

        super().__init__(message)

"""Base for row-related errors."""
class RowError(DatabaseError):
    """Base for row-related errors."""
    pass

class RowValidationError(RowError):
    pass

class DuplicatePrimaryKeyError(RowError):
    pass   

"""Base for query-related errors."""
class QueryError(DatabaseError):
    pass

class QueryInvalidOperatorError(QueryError):
    """Raised when invalid operator is provided in the where clause of the query."""
    def __init__(self, operator) -> None:
        self.operator = operator

        message = f"Invalid operator '{operator}' received in the query."
        
        super().__init__(message)

        