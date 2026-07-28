# from .database import Database
from typing import Any
import operator
from exceptions import QueryInvalidOperatorError, UnknownColumnError, QueryInvalidAggregationError
from enum import Enum

class AggregationType(Enum):
    COUNT = "COUNT"
    SUM = "SUM"
    AVG = "AVG"
    MAX = "MAX"
    MIN = "MIN"

"""Query class for building and executing queries on tables."""
class QueryBuilder:

    """Initialize the Query with a table and an empty list of conditions."""
    def __init__(self, database,
                 table_name: str, 
                 column_list: list[str] | None = None, 
                 query_type: str | None = None
                 ) -> None:
        
        self.database = database
        self.table = database.get_table(table_name)
        self.conditions = []
        self.selected_columns= column_list
        self.group_column = None
        self.order_column = None
        self.order_desc = False
        self.limit_count = None
        self.aggregation_type = None
        self.aggregation_column = None
        self.filtered_rows=[]
        self.query_type = query_type
        self.update_col_dict = {}
        self.joins = []

        self.operators_map = {
            '==': operator.eq,
            '!=': operator.ne,
            '>':  operator.gt,
            '<':  operator.lt,
            '>=': operator.ge,
            '<=': operator.le,
        }

        # Mapping of aggregation type enum members to their corresponding methods
        self.AGGREGATION_MAP = {
            AggregationType.COUNT: self._apply_count,
            AggregationType.SUM: self._apply_sum,
            AggregationType.AVG: self._apply_avg,
            AggregationType.MAX: self._apply_max,
            AggregationType.MIN: self._apply_min
        }

    """
    The query chaining methods can only work if each of them return Query(self). Hnece, instead of doing any sort of row processing
    inside the chaining methods, we will use them to add properties to the Query class instead and perform the processing as a sort 
    pipeline all inside the .execute() method.
    """

    """Add a condition to the query based on a column, operator, and value."""
    def where(self, column: str, operator: str, value: Any) -> 'QueryBuilder':

        # print("Inside where method")

        if operator not in self.operators_map:
            raise QueryInvalidOperatorError(operator)

        self._validate_column_reference(column)
        
        self.conditions.append((column, operator, value))

        return self

    """Update the order by column(order_column) and the type of order i.e. ascending or descending(order_desc)."""
    def order_by(self, column: str, reversed: bool | None = None):

        self._validate_column_reference(column)

        self.order_column = column

        self.order_desc = reversed if reversed is not None else False

        return self

    """Set the limit_count property."""
    def limit(self, limit: int):
        
        self.limit_count = limit
        return self

    """Set the group_column property."""
    def group_by(self, column: str):
        # print("---group by---")
        self.group_column = column
        return self

    def join(self, table: str, left_key: str, right_key: str, join_type: str = "INNER"):

        # print("inside join")

        join_entry ={
            "table": table,
            "left_key": left_key,
            "right_key": right_key,
            "join_type": join_type
        }

        self.joins.append(join_entry)

        return self

    """Execute the query and return the results that match the conditions."""
    def execute(self):
        # print("---execute method---")

        if self.query_type == "UPDATE":
            self._execute_update()
            return

        if self.query_type == "DELETE":
            self._execute_delete()
            return

        if len(self.joins) > 0:
            # print("join details: ", self.joins)
            rows = self._apply_joins()
        else:
            rows = self.table.get_rows()

        # print("rows after join: ", rows)

        rows = self._apply_where(rows)

        groups = {}

        if self.group_column is not None:
            # print("inside group by apply")
            groups : dict = self._apply_group_by(rows)

        if self.aggregation_type is not None:
            try:
                agg_enum = AggregationType(self.aggregation_type)

                handler = self.AGGREGATION_MAP[agg_enum]
                rows = handler(rows, groups)
                
            except ValueError:
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

    def _execute_update(self):

        rows = self.table.get_rows()
        rows = self._apply_where(rows)

        self._apply_update(rows)

        return

    def _execute_delete(self):

        rows = self.table.get_rows()
        rows = self._apply_where(rows)

        self._apply_delete(rows)

        return

    def _apply_joins(self):
        # Prefixed the left table and stored it in the result set for the first time to join with the right table
        base_table = self.table.table_name
        result_rows = [
            self._prefix_row(row, base_table)
            for row in self.table.get_rows()
        ]


        for join in self.joins:
            # Got the right join table rows prefixed as well
            # print("Join details inside _apply_join", join)
            right_table_rows = self.database.get_table(join["table"]).get_rows()
            prefixed_right_rows = [
                self._prefix_row(row, join["table"])
                for row in right_table_rows
            ]

            # Below var will store the joined rows generated by the inner loop, to be later passed over to the outer loop
            # in cases where we need multiple table joins
            new_result_rows = []

            if not result_rows:
                return []

            for left_row in result_rows:
                for right_row in prefixed_right_rows:
                    if left_row.get(join["left_key"]) == right_row.get(join["right_key"]):
                        new_result_rows.append(self._merge_rows(left_row, right_row))

            result_rows = new_result_rows

        return result_rows

    def _merge_rows(self, left_row: dict, right_row: dict):

        return {**left_row, **right_row}

    """Adds 'table_name.' prefix to all keys in a row."""
    def _prefix_row(self, row: dict, table_name: str) -> dict:

        return {f"{table_name}.{key}": value for key, value in row.items()}

    """This helper methods check if the column name is qualified or not then checks its validity"""
    def _validate_column_reference(self, column: str):

        if "." not in column:
            table = self.table
            column_name = column
        else:

            table_name, column_name = column.split(".", 1)
            table = self.database.get_table(table_name)

        if not table.get_column(column_name):
            raise UnknownColumnError(column, self.table.table_name)

    def _apply_where(self, rows):

        filtered_rows =[]
        for row in rows:
            if self._matches_condition(row):
                filtered_rows.append(row)
                
        return filtered_rows

    def _apply_group_by(self,rows):
        # print("---group by---")
        groups: dict = {}
        if len(rows) == 0:
            rows = self.table.get_rows()

        for row in rows:
            key = row[self.group_column]
            if key not in groups:
                groups[key] = []

            groups[key].append(row)

        return groups

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

    def _apply_delete(self, rows):

        # print("Applying delete on ", rows)
        self.table.delete_rows(rows)
        return 

    """ 
    Aggregate funtions COUNT, SUM, AVG, MAX & MIN.
    """
    def count(self):

        self.aggregation_type = AggregationType.COUNT
        return self

    def _apply_count(self, rows: list | None = None, groups: dict | None = None):

        if self.group_column is None:
            if rows is None:
                return 0
            return len(rows)
        else: 
            result=[]

            if groups is None:
                return result

            for key, group in groups.items():
                dict_entry = {
                    self.group_column: key,
                    "count": len(group)
                }

                result.append(dict_entry)

            return result

    def sum(self, sum_column:str):
        # print("---sum method---")
        self.aggregation_type = AggregationType.SUM
        self.aggregation_column = sum_column
        # print("agg method: ", self.aggregation_type)
        return self

    def _apply_sum(self, rows: list | None = None, groups: dict |None = None):
        # print("---apply sum---")
        if self.group_column is None:
            sum_val = 0
            if rows is None:
                return 0
            
            for row in rows:
                sum_val += row[self.aggregation_column]

            return sum_val
        else:
            # print("---group apply sum---")

            result=[]

            if groups is None:
                return result
            
            for key, group in groups.items():
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

        self.aggregation_type = AggregationType.AVG
        self.aggregation_column = avg_column
        return self

    def _apply_avg(self, rows: list | None = None,  groups: dict |None = None) -> list | float:

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

            if groups is None:
                return result

            for key, group in groups.items():
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

    def max(self, max_column: str) -> 'QueryBuilder':

        self.aggregation_type = AggregationType.MAX
        self.aggregation_column = max_column
        return self
    
    def _apply_max(self, rows: list | None = None, groups: dict |None = None) -> list | int | float | str:

        result=[]
        if self.group_column is None:

            if not rows:
                return result
            
            max_val = rows[0][self.aggregation_column]

            for row in rows:
                if row[self.aggregation_column] > max_val:
                    max_val = row[self.aggregation_column]

            return max_val
        else:

            if groups is None:
                return result

            for key, group in groups.items():
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

    
    def min(self, min_column: str) -> 'QueryBuilder':

        self.aggregation_type = AggregationType.MIN
        self.aggregation_column = min_column
        return self
    
    def _apply_min(self, rows: list | None = None,  groups: dict |None = None) -> list:

        result=[]

        if self.group_column is None:

            if not rows:
                return result
            
            min_val = rows[0][self.aggregation_column]

            for row in rows:
                if row[self.aggregation_column] > min_val:
                    min_val = row[self.aggregation_column]

            return min_val
        else:
            if groups is None:
                return result
            
            for key, group in groups.items():
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
