# from .database import Database
from typing import Any
import operator
from exceptions import QueryInvalidOperatorError, UnknownColumnError

"""Query class for building and executing queries on tables."""
class Query:

    """Initialize the Query with a table and an empty list of conditions."""
    def __init__(self, database,
                 table_name: str, 
                 column_list: list[str] | None = None, 
                 ) -> None:

        self.table = database.get_table(table_name)
        self.column_list = column_list
        self.conditions = []
        self.results=[]
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

        if operator not in self.operators_map:
            raise QueryInvalidOperatorError(operator)
        
        if not self.table.get_column(column):
            raise UnknownColumnError(column, self.table.table_name)

        self.conditions.append((column, operator, value))

        self.results = self._filter_rows()
        return self

    """Execute the query and return the results that match the conditions."""
    def execute(self):

        # Check if a selected column list is provided, if so return only the projected column instead of entire rows
        if self.column_list is None:
            return self.results
        else: 
            return self._projected_cols()

    """Helper method to check if a row matches all the conditions in the query."""
    def _matches_condition(self, row) -> bool:

        for col, op, val in self.conditions:
            row_val = row[col]

            op_func = self.operators_map.get(op)

            if op_func is None:
                raise QueryInvalidOperatorError(op)

            if not op_func(row_val, val):
                return False

        return True

    def _filter_rows(self):

        filtered_rows =[]
        for row in self.table.get_rows():
            if self._matches_condition(row):
                filtered_rows.append(row)
                
        return filtered_rows

    def _projected_cols(self):

        projected_results = []
        if self.column_list is None:
            return self.results
        
        for row in self.results:
            projected_row = {
                        col: row[col]
                        for col in self.column_list
                        }
            projected_results.append(projected_row)
        return projected_results
        

    def order_by(self, column: str, reversed: bool | None = None):

        if not self.table.get_column(column):
            raise UnknownColumnError(column, self.table.table_name)

        is_descending = reversed if reversed is not None else False
        self.results = sorted(self.results, key=lambda row: row[column], reverse=is_descending)
        return self

    def limit(self, limit: int):
        self.results = self.results[:limit]
        return self

                    
             



