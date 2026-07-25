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
        self.group_column = None
        self.grouped_rows = {}
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

    def set_cols(self, col_val: dict):

        for row in self.results:
            for col, val in col_val.items():
                row[col] = val 

        return self

    # Aggregate funtions SUM, AVG, MAX, MIN, COUNT
    def count(self):

        count = 0;
        for _ in self.results:
            count+=1

        return count

    def sum(self, column: str):

        sum_val = 0
        for row in self.results:
            sum_val += row[column]

        return sum_val

    def avg(self, column:str):

        count=0
        sum_val=0
        for row in self.results:
            count+=1
            sum_val += row[column]

        if count == 0:
            return 0

        return sum_val / count

    def max(self, column: str):

        if not self.results:
            return None
        
        max_val = self.results[0][column]

        for row in self.results:
            if row[column] > max_val:
                max_val = row[column]

        return max_val
    
    def min(self, column: str):

        if not self.results:
            return None
        
        min_val = self.results[0][column]

        for row in self.results:
            if row[column] < min_val:
                min_val = row[column]

        return min_val

    def group_by(self, column: str):

        self.group_column = column
        return self
             



