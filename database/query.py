# from .database import Database
from typing import Any
import operator
from exceptions import QueryInvalidOperatorError, UnknownColumnError

"""Query class for building and executing queries on tables."""
class Query:
    """Initialize the Query with a table and an empty list of conditions."""
    def __init__(self, table_name: str, database) -> None:
        self.table = database.tables[table_name]
        self.conditions = []
        self.operators_map = {
            '==': operator.eq,
            '!=': operator.ne,
            '>':  operator.gt,
            '<':  operator.lt,
            '>=': operator.ge,
            '<=': operator.le,
        }

    """Add a condition to the query based on a column, operator, and value."""
    def where(self, column: str, operator: str, value: Any) -> 'Query':
        if operator not in ['==','!=','>','<','>=','<=']:
            raise QueryInvalidOperatorError(operator)
        
        if not self.table.get_column(column):
            raise UnknownColumnError(column, self.table.table_name)

        self.conditions.append((column, operator, value))
        return self

    """Execute the query and return the results that match the conditions."""
    def execute(self):
        results =[]

        for row in self.table.rows:
            if self._matches_condition(row):
                results.append(row)

        return results

    """Helper method to check if a row matches all the conditions in the query."""
    def _matches_condition(self, row) -> bool:

        # This helper method checks if the row matches the set of condition
        for col, op, val in self.conditions:
            row_val = row[col]

            op_func = self.operators_map.get(op)

            if op_func is None:
                raise QueryInvalidOperatorError(op)

            if not op_func(row_val, val):
                return False

        return True
             



