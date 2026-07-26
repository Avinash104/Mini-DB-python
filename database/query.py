# from .database import Database
from typing import Any
import operator
from exceptions import QueryInvalidOperatorError, UnknownColumnError, QueryInvalidAggregationError

"""Query class for building and executing queries on tables."""
class Query:

    """Initialize the Query with a table and an empty list of conditions."""
    def __init__(self, database,
                 table_name: str, 
                 column_list: list[str] | None = None, 
                 ) -> None:

        self.table = database.get_table(table_name)
        self.conditions = []
        self.selected_columns= column_list
        self.group_column = None
        self.order_column = None
        self.order_desc = False
        self.limit_count = None
        self.groups = {}
        self.aggregation_types = ("COUNT", "SUM", "AVG", "MAX", "MIN")
        self.aggregation_type = None
        self.aggregation_column = None
        self.filtered_rows=[]
        self.query_type = None
        self.update_col_dict = {}

        self.operators_map = {
            '==': operator.eq,
            '!=': operator.ne,
            '>':  operator.gt,
            '<':  operator.lt,
            '>=': operator.ge,
            '<=': operator.le,
        }

    """
    The query chaining methods can only work if each of them return Query(self). Hnece, instead of doing any sort of row processing
    inside the chaining methods, we will use them to add properties to the Query class instead and perform the processing as a sort 
    pipeline all inside the .execute() method.
    """

    """Add a condition to the query based on a column, operator, and value."""
    def where(self, column: str, operator: str, value: Any) -> 'Query':

        if operator not in self.operators_map:
            raise QueryInvalidOperatorError(operator)
        
        if not self.table.get_column(column):
            raise UnknownColumnError(column, self.table.table_name)

        self.conditions.append((column, operator, value))

        return self

    """Update the order by column(order_column) and the type of order i.e. ascending or descending(order_desc)."""
    def order_by(self, column: str, reversed: bool | None = None):

        if not self.table.get_column(column):
            raise UnknownColumnError(column, self.table.table_name)

        self.order_column = column

        self.order_desc = reversed if reversed is not None else False

        return self

    """Set the limit_count property."""
    def limit(self, limit: int):
        
        self.limit_count = limit
        return self

    """Set the group_column property."""
    def group_by(self, column: str):
        print("---group by---")
        self.group_column = column
        return self

    """Execute the query and return the results that match the conditions."""
    def execute(self):
        print("---execute method---")

        rows = self.table.get_rows()

        rows = self._apply_where(rows)

        if self.query_type == "UPDATE":
            self._apply_update(rows)
            return

        if self.group_column is not None:
            print("inside group by apply")
            self._apply_group_by(rows)

        if self.aggregation_type is not None:
            print("---aggregation type---", self.aggregation_type)
            match self.aggregation_type:
                case "COUNT":
                    rows = self._apply_count(rows)
                case "SUM":
                    rows = self._apply_sum(rows)
                case "AVG":
                    rows = self._apply_avg(rows)
                case "MAX":
                    rows = self._apply_max(rows)
                case "MIN":
                    rows = self._apply_min(rows)
                case _:
                    raise QueryInvalidAggregationError(self.aggregation_type)

        if self.order_column is not None:
            rows = self._apply_order_by(rows)

        if self.limit_count is not None:
            rows = self._apply_limit(rows)

        # Check if a selected column list is provided, if so return only the projected column instead of entire rows
        if self.selected_columns is None:
            return rows
        else: 
            return self._projected_cols(rows)

    def _apply_where(self, rows):

        filtered_rows =[]
        for row in rows:
            if self._matches_condition(row):
                filtered_rows.append(row)
                
        return filtered_rows

    def _apply_group_by(self,rows):
        print("---group by---")
        if len(rows) == 0:
            rows = self.table.get_rows()

        for row in rows:
            key = row[self.group_column]
            if key not in self.groups:
                self.groups[key] = []

            self.groups[key].append(row)

    def _apply_order_by(self, rows):

        return sorted(rows, key=lambda row: row[self.order_column], reverse=self.order_desc)

    def _apply_limit(self, rows):

        return rows[:self.limit_count]

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

    def _projected_cols(self, rows):

        projected_results = []
        if self.selected_columns is None:
            return rows
        
        for row in rows:

            projected_row = {
                        col: row[col]
                        for col in self.selected_columns
                        }
            projected_results.append(projected_row)

        return projected_results
        
    def set(self, col_val: dict):

        self.query_type = "UPDATE"
        self.update_col_dict = col_val

        return self

    def _apply_update(self, rows):

        for row in rows:
            for col, val in self.update_col_dict.items():
                row[col] = val 

        return 

    """ 
    Aggregate funtions COUNT, SUM, AVG, MAX & MIN.
    """
    def count(self):

        self.aggregation_type = self.aggregation_types[0]
        return self

    def _apply_count(self, rows):

        if self.group_column is None:

            return len(rows)
        else: 
            result=[]

            for key, group in self.groups.items():
                dict_entry = {
                    self.group_column: key,
                    "count": len(group)
                }

                result.append(dict_entry)

            return result

    def sum(self, sum_column:str):
        print("---sum method---")
        self.aggregation_type = self.aggregation_types[1]
        self.aggregation_column = sum_column
        print("agg method: ", self.aggregation_type)
        return self

    def _apply_sum(self, rows: list | None = None):
        print("---apply sum---")
        if self.group_column is None:
            sum_val = 0
            if rows is None:
                return 0
            
            for row in rows:
                sum_val += row[self.aggregation_column]

            return sum_val
        else:
            print("---group apply sum---")

            result=[]
            for key, group in self.groups.items():
                sum_val = 0
                for row in group:
                    sum_val += row[self.aggregation_column]

                dict_entry = {
                    self.group_column: key,
                    "sum": sum_val
                }

                result.append(dict_entry)

            return result

    def avg(self, avg_column: str):

        self.aggregation_type = self.aggregation_types[2]
        self.aggregation_column = avg_column
        return self

    def _apply_avg(self, rows: list | None = None):

        if self.group_column is None:
            count=0
            sum_val=0

            if rows is None:
                return 0
            
            for row in rows:
                count+=1
                sum_val += row[self.aggregation_column]

            if count == 0:
                return 0

            return sum_val / count

        else:
            result=[]

            for key, group in self.groups.items():
                sum_val = 0
                count = 0
                for row in group:
                    sum_val += row[self.aggregation_column]

                count = len(group)
                avg_val = 0 if count == 0 else sum_val / count

                dict_entry = {
                    self.group_column: key,
                    "avg": avg_val
                }
                
                result.append(dict_entry)

            return result

    def max(self, max_column: str):

        self.aggregation_type = self.aggregation_types[3]
        self.aggregation_column = max_column
        return self
    
    def _apply_max(self, rows):

        if self.group_column is None:

            if not rows:
                return None
            
            max_val = rows[0][self.aggregation_column]

            for row in rows:
                if row[self.aggregation_column] > max_val:
                    max_val = row[self.aggregation_column]

            return max_val
        else:
            result=[]

            for key, group in self.groups.items():
                max_val = group[0][self.aggregation_column]
                for row in group:
                    if row[self.aggregation_column] > max_val:
                        max_val = row[self.aggregation_column]
                    
                dict_entry = {
                    self.group_column: key,
                    "max": max_val
                }
                
                result.append(dict_entry)

            return result

    
    def min(self, min_column: str):

        self.aggregation_type = self.aggregation_types[4]
        self.aggregation_column = min_column
        return self
    
    def _apply_min(self, rows):

        if self.group_column is None:

            if not rows:
                return None
            
            min_val = rows[0][self.aggregation_column]

            for row in rows:
                if row[self.aggregation_column] > min_val:
                    min_val = row[self.aggregation_column]

            return min_val
        else:
            result=[]

            for key, group in self.groups.items():
                min_val = group[0][self.aggregation_column]
                for row in group:
                    if row[self.aggregation_column] < min_val:
                        min_val = row[self.aggregation_column]

                dict_entry = {
                    self.group_column: key,
                    "min": min_val
                }
                
                result.append(dict_entry)

            return result
