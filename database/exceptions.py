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

class DuplicatePrimaryKeyError(TableError):
    """Raised when duplicate primary key is provided during row insertion."""
    def __init__(self, pk, table_name):
        self.pk = pk
        self.table_name = table_name
        
        message = f"Duplicate primary key was provided for column '{pk}' in table '{table_name}'."

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

class RequiredColumnMissing(ColumnError):
    def __init__(self, column_name: str):
        self.column_name = column_name

        message = f"Required column '{column_name}' is missing."

        super().__init__(message)

class UnkownColumnInsert(ColumnError):
    def __init__(self, unkown_column_list: set):
        self.unkown_column_list = unkown_column_list

        message = f"Unkown columns '{unkown_column_list}' provided in insert operation column."

        super().__init__(message)

"""Base for row-related errors."""
class RowError(DatabaseError):
    """Base for row-related errors."""
    pass

class RowValidationError(RowError):
    pass

class MissingColumnsInRowInsert(RowError):
    def __init__(self):
        message = "All columms must be provided in list input for row insert. Use dictionary if you want to insert selectively."

        super().__init__(message)

"""Base for query-related errors."""
class QueryError(DatabaseError):
    pass

class QueryInvalidOperatorError(QueryError):
    """Raised when invalid operator is provided in the where clause of the query."""
    def __init__(self, operator) -> None:
        self.operator = operator

        message = f"Invalid operator '{operator}' received in the query."
        
        super().__init__(message)

class QueryInvalidAggregationError(QueryError):
    """Raised when invalid aggregation type is provided in the query."""
    def __init__(self, aggregation_type) -> None:
        self.aggregation_type = aggregation_type

        message = f"Invalid aggregation type '{aggregation_type}' received in the query."
        
        super().__init__(message)

class InvalidDataTypeInWhereClause(QueryError):
    """Raised when invalid aggregation type is provided in the query."""
    def __init__(self, expected_data_type, received_data_type) -> None:
        self.expected_data_type = expected_data_type
        self.received_data_type = received_data_type

        message = f"Invalid data type received in where clause. Expected '{expected_data_type}', received '{received_data_type}' in the query."
        
        super().__init__(message)

class RequiredColumnCannotBeNone(QueryError):
    """Raised when invalid aggregation type is provided in the query."""
    def __init__(self, column_name) -> None:
        self.column_name = column_name

        message = f"Required column '{column_name}' connot be set to none in update query."
        
        super().__init__(message)

class UpdateColumnTypeMismatch(QueryError):
    """Raised when invalid column type is provided in the update query."""
    def __init__(self, expected_data_type, received_data_type) -> None:
        self.expected_data_type = expected_data_type
        self.received_data_type = received_data_type

        message = f"Invalid data type received in update clause. Expected '{expected_data_type}', received '{received_data_type}' in the query."
        
        super().__init__(message)

class NoQualifiedRowsForDelete(QueryError):
    """No qualified rows found for delete query."""
    def __init__(self) -> None:

        message = "No qualified rows found for delete query."
        
        super().__init__(message)

class UnknownGroupbyColumn(QueryError):
    """Raised when unkown column passed in group by clause."""
    def __init__(self, unkown_column: str):
        self.unkown_column = unkown_column

        message = f"Unkown column '{unkown_column}' provided in group by operation."

        super().__init__(message)