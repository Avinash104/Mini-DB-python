from typing import Any, Dict, Iterable, Tuple

class Row:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def __str__(self) -> str:
        return str(self.data)
    
    def __repr__(self) -> str:
        return str(self.data)

    def __getitem__(self, key: str):
        return self.data[key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        self.data[key] = value

    def __len__(self) -> int:
        return len(self.data)
    
    def __iter__(self) -> Iterable[Tuple[str, Any]]:
        return iter(self.data.items())
    
    def __contains__(self, key:str):
        return key in self.data
    
