from typing import Any, Dict, Iterable, Tuple

"""Row class for representing a single row in a table."""
class Row:

    """Initialize the Row with a dictionary of column-value pairs."""
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    """Get a string representation of the row."""
    def __str__(self) -> str:
        return str(self._data)

    """Get a detailed string representation of the row."""
    def __repr__(self) -> str:
        return f"Row({self._data})"

    """Get the value of a column in the row."""
    def __getitem__(self, key: str):
        return self._data[key]

    """Set the value of a column in the row."""
    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    """Get the number of columns in the row."""
    def __len__(self) -> int:
        return len(self._data)

    """Get an iterator over the column-value pairs in the row."""
    def __iter__(self) -> Iterable[Tuple[str, Any]]:
        return iter(self._data.items())

    """Check if a column exists in the row."""
    def __contains__(self, key:str):
        return key in self._data
    
    def items(self):
        return self._data.items()

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def get(self, key: str):
        return self._data[key]

    
