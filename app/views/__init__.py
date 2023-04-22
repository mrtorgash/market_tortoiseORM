from typing import List,TypeVar, Type
from pydantic import BaseModel
T = TypeVar(name= "T",bound=BaseModel)
def from_list_to_pydantic(list: List,model: Type[T]) -> List[T]:
    output = [model(**element) for element in list]
    return output